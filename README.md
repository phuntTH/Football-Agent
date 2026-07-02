# Football Agent

An intelligent multi-agent football assistant built with **LangGraph**, **Google Gemini**, football data APIs, and **Tavily Search**.

Football Agent is designed to answer football-related questions by combining structured data sources with web search fallback. The system routes each question to the most appropriate specialized agent, executes relevant tools, and generates a structured final response.

The project currently focuses on local development, testing agent behavior, tool calling, fallback logic, and streamed responses.

---

# Features

## World Cup 2026 Assistant

Supports questions related to the FIFA World Cup 2026, including:

* Match schedules
* Match results
* Group standings
* Top scorers
* Participating teams
* Team performance
* Match details

Example:

```text
What matches will be played on June 15, 2026?
```

---

## Football Match Data Retrieval

Retrieves structured football information from external APIs.

Supported information includes:

* Match details
* Match results
* Goals and assists
* Match events
* Team information
* Player information
* Match statistics
* Starting lineups when available

Example:

```text
What was the score between Brazil and Morocco?
```

```text
Who scored in the Brazil vs Morocco match?
```

---

## IFAB Laws of the Game

Provides answers about football rules using IFAB law data.

Supported topics include:

* Offside
* Handball
* VAR
* Penalties
* Yellow cards
* Red cards
* Referee decisions

Example:

```text
Explain the offside rule.
```

---

## Football News Search

Uses Tavily Search to retrieve football news when structured football APIs do not contain enough information.

Typical use cases include:

* Latest football news
* Transfer rumors
* Player injuries
* Recent statements
* Expert analysis
* Match previews
* Recently announced lineups

Example:

```text
Latest news about Kylian Mbappé
```

---

## Fallback Search Mechanism

The system detects missing, incomplete, or unsupported football data from APIs.

When structured data is unavailable, the agent automatically switches to web search.

```text
Football API
      ↓
Missing or incomplete data
      ↓
Tavily Search
      ↓
Final summarized answer
```

This approach improves answer coverage while reducing unsupported or fabricated responses.

---

# Architecture

## Multi-Agent Workflow

```text
User Question
       │
       ▼
Intent Classifier
       │
 ┌─────┼─────────────────────────────┐
 │     │             │               │
 ▼     ▼             ▼               ▼
Law   Football    World Cup         News
Agent Agent       Agent             Agent
 │     │             │               │
 └─────┼─────────────┼───────────────┘
       │
       ▼
Fallback Search
       │
       ▼
Summarization Node
       │
       ▼
Final Answer
```

---

# Agent Routing

The system classifies user questions into several categories:

| Intent            | Example Question         | Target Agent         |
| ----------------- | ------------------------ | -------------------- |
| Football laws     | What is offside?         | Law Agent            |
| Match data        | Who scored for Brazil?   | Football Agent       |
| World Cup history | Who won World Cup 2014?  | World Cup Agent      |
| World Cup 2026    | Matches on June 15, 2026 | World Cup 2026 Agent |
| Football news     | Latest Mbappé update     | News Agent           |

The router also uses keyword-based rules for common requests such as lineups, match statistics, goals, World Cup schedules, and IFAB laws.

---

# Tool Execution Flow

A typical tool execution flow is shown below.

```text
User Question
      ↓
Intent Classification
      ↓
Selected Agent
      ↓
Tool Call
      ↓
Tool Result
      ↓
Data Validation
      ├── Valid Data → Generate Answer
      └── Missing Data → Tavily Search Fallback
```

Example tools used by the project:

```text
get_world_cup_matches
get_world_cup_standings
get_match_events
get_match_lineup
get_match_statistics
search_ifab_law
search_latest_news
```

---

# Streaming and Tool Tracing

The application supports Server-Sent Events (SSE) for streamed agent responses.

During execution, the frontend displays:

* Tool calls
* Tool completion events
* Agent response progress
* Final formatted Markdown response

Example tool trace:

```text
search_latest_news
tavily_search_results_json
```

This makes the agent workflow easier to inspect during local development and debugging.

---

# Technology Stack

## AI and Agent Framework

* LangGraph
* LangChain
* Google Gemini

## Football Data Sources

* Football-Data.org API
* API-Football
* Zafronix API
* FIFA World Cup data sources

## Search

* Tavily Search

## Backend

* FastAPI
* Uvicorn
* Python

## Frontend

* HTML
* CSS
* JavaScript
* Marked.js for Markdown rendering

---

# Project Structure

```text
Football-Agent/
│
├── src/
│   ├── agent/
│   │   ├── graph.py
│   │   ├── router.py
│   │   └── state.py
│   │
│   ├── prompts/
│   │   └── prompts.py
│   │
│   ├── services/
│   │   ├── football_service.py
│   │   ├── worldcup2026_service.py
│   │   └── news_service.py
│   │
│   └── tools/
│       ├── football_tools.py
│       ├── worldcup_tools.py
│       ├── law_tools.py
│       └── news_tools.py
│
├── ui/
│   ├── api/
│   │   └── chat.py
│   │
│   ├── services/
│   │   └── agent_service.py
│   │
│   ├── schemas/
│   │   └── chat_schema.py
│   │
│   ├── static/
│   │   ├── app.js
│   │   └── style.css
│   │
│   ├── templates/
│   │   └── index.html
│   │
│   └── app.py
│
├── main.py
├── requirements.txt
├── .env.example
└── README.md
```

---

# Running Locally

## Clone the Repository

```bash
git clone https://github.com/your-username/football-agent.git
cd football-agent
```

## Create a Virtual Environment

```bash
python -m venv .venv
```

Activate the environment.

Windows:

```bash
.venv\Scripts\activate
```

Linux or macOS:

```bash
source .venv/bin/activate
```

## Install Dependencies

```bash
pip install -r requirements.txt
```

## Configure Environment Variables

Create a `.env` file in the root directory.

```env
GOOGLE_API_KEY=YOUR_GEMINI_API_KEY
TAVILY_API_KEY=YOUR_TAVILY_API_KEY
FOOTBALL_DATA_API_KEY=YOUR_FOOTBALL_DATA_API_KEY
```

Depending on the enabled services, additional API keys may be required.

## Start the Application

```bash
python main.py
```

Open the application in your browser:

```text
http://localhost:8000
```

---

# Example Questions

## World Cup 2026

```text
Matches on June 15, 2026
```

```text
World Cup 2026 standings
```

```text
Who are the top scorers in World Cup 2026?
```

```text
Brazil vs Morocco score in World Cup 2026
```

## Football Match Data

```text
Who scored for Brazil?
```

```text
What happened in the Brazil vs Morocco match?
```

```text
Show match statistics for Argentina vs France
```

## IFAB Laws

```text
Explain the offside rule
```

```text
When is a handball penalty given?
```

```text
Can VAR review a yellow card?
```

## Football News

```text
Latest football transfer news
```

```text
Latest update about Kylian Mbappé
```

```text
Recent injury news about Brazil players
```

---

# Current Scope

The current version is designed for local development and agent testing.

The main goals are:

* Testing LangGraph agent workflows
* Validating routing logic
* Testing football API tool calls
* Testing fallback web search
* Inspecting tool traces
* Streaming agent responses to the frontend
* Improving Markdown response formatting

Deployment, authentication, persistent chat history, and production infrastructure are intentionally not included in the current scope.

---

# Future Improvements

* PostgreSQL integration for chat history
* User authentication
* Persistent conversation memory
* Docker support
* Cloud or VPS deployment
* Rate limiting
* Logging and monitoring
* Unit and integration tests
* Better match entity resolution
* Live match tracking
* Multi-language support
* Voice input and output
* More reliable lineup and formation data sources

---

# Author

Developed as a football-focused multi-agent AI assistant using LangGraph, Google Gemini, football APIs, and Tavily Search.
