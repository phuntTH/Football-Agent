# ⚽ Football Agent

An intelligent multi-agent football assistant powered by **LangGraph**, **Google Gemini**, **Football APIs**, and **Tavily Search**.

Football Agent can answer questions about:

* FIFA World Cup 2026
* Match results and statistics
* Starting lineups and formations
* Teams and players
* IFAB Laws of the Game
* Historical World Cup data
* Latest football news

The system combines structured football databases with real-time web search to provide accurate and up-to-date answers.

---

# Features

## 🌍 World Cup 2026 Assistant

Query World Cup 2026 information such as:

* Match schedules
* Match results
* Group standings
* Top scorers
* Team performance
* Starting lineups

Example:

> What matches will be played on June 15, 2026?

---

## 📊 Football Data Retrieval

Retrieve football-related information from structured APIs:

* Match details
* Team information
* Player statistics
* Goals and assists
* Formations
* Match events

Example:

> Starting lineup between Brazil and Morocco at World Cup 2026

---

## 📖 IFAB Laws of the Game

Specialized legal football assistant for:

* Offside
* Handball
* VAR
* Penalties
* Red cards
* Yellow cards
* Referee decisions

Example:

> Explain the offside rule.

---

## 📰 Latest Football News

When information is not available in football databases, the agent automatically falls back to web search using Tavily.

Example:

> Latest news about Kylian Mbappé

---

## 🔄 Intelligent Fallback Mechanism

The system automatically detects missing or incomplete football data.

Workflow:

Football API → World Cup API → Tavily Search → Final Answer

This ensures users still receive useful answers even when structured databases lack information.

---

# Architecture

## Multi-Agent Workflow

```text
User Question
       │
       ▼
Route Classifier
       │
 ┌─────┼───────────────┐
 │     │               │
 ▼     ▼               ▼
Law  Football      World Cup
Agent Agent        Agent
 │     │               │
 └─────┼───────────────┘
       ▼
Fallback News Agent
       ▼
Summarizer
       ▼
Final Answer
```

---

# Technology Stack

## AI

* LangGraph
* LangChain
* Google Gemini

## Football Data

* Football-Data.org - API
* Zafronix - API
* api-football - API
* FIFA World Cup Data

## Search

* Tavily Search

## Backend

* FastAPI
* Uvicorn

## Frontend

* HTML
* CSS
* JavaScript

---

# Project Structure

```text
Football-Agent/
│
├── src/
│   ├── agent/
│   ├── tools/
│   ├── services/
│   ├── prompts/
│   └── graph.py
│
├── ui/
│   ├── api/
│   ├── services/
│   ├── schemas/
│   ├── static/
│   ├── templates/
│   └── app.py
│
├── main.py
├── requirements.txt
└── README.md
```

---

# How It Works

## Step 1: User asks a question

Example:

```text
What was the score between Brazil and Morocco in World Cup 2026?
```

---

## Step 2: Route Classification

The classifier determines the best agent:

* Football Agent
* World Cup Agent
* Law Agent
* News Agent

---

## Step 3: Tool Execution

The selected agent calls one or more tools.

Example:

```text
get_wc2026_matches
get_wc2026_match_detail
search_latest_news
```

---

## Step 4: Fallback Search

If football data is unavailable:

```text
Football API
      ↓
No Data
      ↓
Tavily Search
      ↓
Answer Generated
```

---

## Step 5: Final Response

The summarization node produces a clean Markdown answer.

---

# Running Locally

## Clone Repository

```bash
git clone https://github.com/your-username/football-agent.git

cd football-agent
```

## Create Virtual Environment

```bash
python -m venv .venv
```

Activate:

Windows

```bash
.venv\Scripts\activate
```

Linux / Mac

```bash
source .venv/bin/activate
```

---

## Install Dependencies

```bash
pip install -r requirements.txt
```

---

## Configure Environment Variables

Create `.env`

```env
GOOGLE_API_KEY=YOUR_GEMINI_KEY

TAVILY_API_KEY=YOUR_TAVILY_KEY

FOOTBALL_DATA_API_KEY=YOUR_FOOTBALL_DATA_KEY
```

---

## Start Application

```bash
python main.py
```

Open:

```text
http://localhost:8000
```

---

# Example Questions

## World Cup

```text
Matches on June 15, 2026
```

```text
Brazil vs Morocco score
```

```text
World Cup 2026 standings
```

---

## Football Data

```text
Starting lineup between USA and Paraguay
```

```text
Who scored for Brazil?
```

---

## IFAB Laws

```text
Explain offside
```

```text
When is a handball given?
```

---

## News

```text
Latest football transfer news
```

```text
Mbappé latest update
```

---

# Future Improvements

* PostgreSQL support
* User authentication
* Chat history
* Docker deployment
* VPS deployment
* Multi-language support
* Live match tracking
* Streaming token responses
* Voice interface

---

# Author

Developed as a football-focused AI assistant using LangGraph, Gemini, football databases, and web search technologies.
