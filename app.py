import os
import json
from dotenv import load_dotenv
from flask import Flask, render_template, request, jsonify
from groq import Groq
from duckduckgo_search import DDGS
import wikipedia

load_dotenv()

app = Flask(__name__)
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

# --- Tool functions ---
def web_search(query: str) -> str:
    try:
        with DDGS() as ddgs:
            results = list(ddgs.text(query, max_results=3))
        if not results:
            return "No results found."
        return "\n\n".join([f"**{r['title']}**\n{r['body']}" for r in results])
    except Exception as e:
        return f"Search error: {str(e)}"

def wikipedia_search(query: str) -> str:
    try:
        summary = wikipedia.summary(query, sentences=4)
        return summary
    except wikipedia.DisambiguationError as e:
        return wikipedia.summary(e.options[0], sentences=4)
    except Exception as e:
        return f"Wikipedia error: {str(e)}"

def calculator(expression: str) -> str:
    try:
        allowed = {k: v for k, v in __builtins__.items()
                   if k in ['abs', 'round', 'min', 'max', 'sum', 'pow']} if isinstance(__builtins__, dict) else {}
        result = eval(expression, {"__builtins__": allowed})
        return str(result)
    except Exception as e:
        return f"Calculation error: {str(e)}"

# --- Tool definitions for Groq ---
tools = [
    {
        "type": "function",
        "function": {
            "name": "web_search",
            "description": "Search the internet for current news, recent events, and real-time information.",
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {"type": "string", "description": "The search query"}
                },
                "required": ["query"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "wikipedia_search",
            "description": "Search Wikipedia for detailed background info on people, places, concepts, history.",
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {"type": "string", "description": "The topic to search on Wikipedia"}
                },
                "required": ["query"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "calculator",
            "description": "Evaluate mathematical expressions. E.g. '235 * 48' or '(100 + 50) / 3'.",
            "parameters": {
                "type": "object",
                "properties": {
                    "expression": {"type": "string", "description": "A valid math expression"}
                },
                "required": ["expression"]
            }
        }
    }
]

TOOL_MAP = {
    "web_search": web_search,
    "wikipedia_search": wikipedia_search,
    "calculator": calculator
}

def run_agent(question: str) -> str:
    messages = [
        {"role": "system", "content": "You are a helpful AI research assistant. Use tools to find accurate, up-to-date information. Always provide a clear, well-structured final answer."},
        {"role": "user", "content": question}
    ]

    for _ in range(5):
        response = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=messages,
            tools=tools,
            tool_choice="auto",
            max_tokens=1024
        )

        msg = response.choices[0].message
        messages.append({"role": "assistant", "content": msg.content or "", "tool_calls": [
            {"id": tc.id, "type": tc.type, "function": {"name": tc.function.name, "arguments": tc.function.arguments}}
            for tc in (msg.tool_calls or [])
        ] if msg.tool_calls else None})

        if not msg.tool_calls:
            return msg.content or "I could not find an answer."

        for tc in msg.tool_calls:
            fn_name = tc.function.name
            fn_args = json.loads(tc.function.arguments)
            result = TOOL_MAP[fn_name](**fn_args)
            messages.append({
                "role": "tool",
                "tool_call_id": tc.id,
                "content": result
            })

    return "I reached the maximum number of steps without a final answer."

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/ask', methods=['POST'])
def ask():
    data = request.get_json()
    question = data.get('question', '').strip()
    if not question:
        return jsonify({'error': 'No question provided'}), 400
    try:
        answer = run_agent(question)
        return jsonify({'answer': answer})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5001)
