# AI Research Agent

## Live Demo

**https://ai-research-agent-3z77.onrender.com**

An autonomous AI agent powered by **LLaMA 3.1** and **Groq** that can search the web, look up Wikipedia, and perform calculations in real time to answer any question.

## Demo

Ask anything — the agent decides which tools to use and returns a well-structured answer.

**Example queries:**
- "What is the latest news about AI?"
- "Who is Sundar Pichai and what is his net worth?"
- "What is 235 multiplied by 48 divided by 3?"

## How It Works

```
User Question
      |
      v
LLaMA 3.1 (via Groq) decides which tool to use
      |
   ┌──┴──────────────┐
   |                 |                 |
Web Search     Wikipedia         Calculator
(DuckDuckGo)   (Background)      (Math)
   |                 |                 |
   └──────────────────────────────────┘
                     |
                     v
           Final Answer to User
```

## Tech Stack

| Category | Tools |
|---|---|
| LLM | LLaMA 3.1 8B via Groq |
| Agent Framework | Groq Native Tool Calling |
| Web Search | DuckDuckGo Search |
| Knowledge Base | Wikipedia API |
| Web Framework | Flask |
| Frontend | HTML, CSS, JavaScript |

## Project Structure

```
ai-research-agent/
├── app.py              # Agent logic + Flask API
├── requirements.txt    # Dependencies
├── .env                # API keys (not committed)
├── .gitignore
└── templates/
    └── index.html      # Chat UI
```

## Getting Started

**1. Clone the repository**
```bash
git clone https://github.com/Shrutiraj26/ai-research-agent.git
cd ai-research-agent
```

**2. Install dependencies**
```bash
pip install -r requirements.txt
```

**3. Set up environment**
```bash
cp .env.example .env
# Add your Groq API key to .env
```

**4. Run the app**
```bash
python app.py
```

**5. Open in browser**
```
http://localhost:5001
```

## Tools Available

| Tool | Description |
|---|---|
| Web Search | Searches DuckDuckGo for real-time information |
| Wikipedia | Fetches detailed background on any topic |
| Calculator | Evaluates mathematical expressions |

## Get a Free Groq API Key

Sign up at **https://console.groq.com** — no credit card required.
