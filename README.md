# 🚀 AI Agent with Tool Calling Backend

A production-ready **FastAPI AI Agent** that supports **tool calling**, allowing an LLM to interact with external services such as **GitHub**, **Gmail**, **Notion**, and a **PostgreSQL database**.

The agent receives a user prompt, decides whether a tool is needed, executes the tool, and returns a natural language response to the user.

---

# ✨ Features

* 🤖 AI-powered assistant with tool calling
* ⚡ FastAPI + Async architecture
* 🐘 PostgreSQL database
* 🔐 JWT Authentication
* 🔑 OAuth2 integrations
* 📧 Gmail email sending
* 📚 Notion integration
* 🐙 GitHub repository search
* 🗄️ Database event extraction
* 📝 Conversation history
* 📊 Structured tool execution
* 🧠 Function Calling compatible
* 🐳 Docker support
* 🔄 Alembic migrations
* 📜 OpenAPI (Swagger) documentation
* ⚙️ Environment-based configuration

---

# Architecture

```
                    User
                      │
                      ▼
              FastAPI Endpoint
                      │
                      ▼
              AI Agent Service
                      │
        ┌─────────────┼──────────────┐
        │             │              │
        ▼             ▼              ▼
      LLM        Tool Selector    Memory (still morking on it)
        │
        ▼
 ┌────────────────────────────────────────┐
 │                Tools                   │
 │                                        │
 │  • GitHub Search                       │
 │  • Gmail Send Email                    │
 │  • Notion Database                     │
 │  • PostgreSQL Events                   │
 └────────────────────────────────────────┘
        │
        ▼
   Tool Response
        │
        ▼
      Final Answer
```

---

# Tech Stack

## Backend

* FastAPI
* Python 3.12+
* SQLAlchemy (Async)
* AsyncPG
* Alembic
* PostgreSQL

## AI

* OpenAI Function Calling compatible
* Tool Calling
* JSON Schema Functions

## Authentication

* JWT Access Token
* JWT Refresh Token
* OAuth2

## External APIs

* GitHub REST API
* Gmail API
* Notion API

---

# Project Structure

```text
app/
│
├── api/
│   └── v1/
│
├── core/
│
├── database/
│
├── middleware/
│
├── models/
│
├── repositories/
│
├── schemas/
│
├── services/
│   ├── ai/
│   ├── github/
│   ├── gmail/
│   ├── notion/
│   └── webhook/
│
├── tools/
│
├── utils/
│
└── main.py
```

---

# Authentication

The project uses JWT authentication.

## Endpoints

* Register
* Verify Account
* Login
* Refresh Token
* Logout
* Logout All Devices
* Current User
* Sessions
* Delete Session

Access Tokens are short-lived.

Refresh Tokens are securely stored in the database.

---

# AI Agent Workflow

```text
User Prompt
      │
      ▼
Send to LLM
      │
      ▼
Does it require a tool?
      │
 ┌────┴────┐
 │         │
No        Yes
 │         │
 ▼         ▼
Respond   Execute Tool
               │
               ▼
      Return Tool Result
               │
               ▼
       LLM Generates Answer
               │
               ▼
            Response
```

---

# Supported Tools

---

## 1. GitHub Tool

Search repositories using the GitHub Search API.

### Features

* Search code
* Search repositories
* Search issues
* Search pull requests
* Search users
* Search commits (optional)

Example:

```
User:
Find the authentication middleware.

↓

GitHub Tool

↓

Returns matching files

↓

LLM summarizes results
```

---

## 2. Gmail Tool

Send emails through the user's Gmail account.

Uses OAuth2 authentication.

### Features

* OAuth Login
* Refresh expired tokens
* Send emails
* HTML emails
* Plain text emails

Example

```
User:
Email John that today's meeting is cancelled.

↓

Gmail Tool

↓

Email sent

↓

Agent confirms success.
```

---

## 3. Notion Tool

Interact with Notion databases.

### Features

* OAuth Authentication
* List databases
* Read database schema
* Add rows
* Retrieve properties

Example

```
User:
Create a task called
"Finish Backend"

↓

Notion Tool

↓

Task inserted into database.
```

---

## 4. Database Tool

Query business events stored inside PostgreSQL.

Useful for analytics.

Example:

```
User:
How much revenue was generated this week?

↓

Database Tool

↓

SELECT ...

↓

Result

↓

AI summarizes.
```

---

# OAuth Flow

## Gmail

```
User

↓

Authorize

↓

Google OAuth

↓

Access Token

↓

Refresh Token

↓

Database

↓

Ready
```

## Notion

```
User

↓

Authorize

↓

Notion OAuth

↓

Access Token

↓

Database

↓

Ready
```

---

# API Documentation

After starting the server:

```
Swagger

http://localhost:8000/docs
```

```
ReDoc

http://localhost:8000/redoc
```

---

# Installation

## Clone

```bash
git clone ...

cd your-repository
```

---

## Create Virtual Environment

Linux

```bash
python -m venv venv

source venv/bin/activate
```

Windows

```bash
venv\Scripts\activate
```

---

## Install Dependencies

```bash
pip install -r requirements.txt
```

---

## Configure Environment

Create

```
.env
```

Example

```env
DATABASE_URL=

SECRET_KEY=

ACCESS_TOKEN_EXPIRE_MINUTES=

REFRESH_TOKEN_EXPIRE_DAYS=

OPENAI_API_KEY=

GITHUB_CLIENT_ID=
GITHUB_CLIENT_SECRET=

GOOGLE_CLIENT_ID=
GOOGLE_CLIENT_SECRET=

NOTION_CLIENT_ID=
NOTION_CLIENT_SECRET=
```

---

## Run Migrations

```bash
alembic upgrade head
```

---

## Start Server

```bash
uvicorn app.main:app --reload
```

---

# Docker

Build

```bash
docker compose build
```

Run

```bash
docker compose up
```

---

# Example Requests

## Send Email

```
Send an email to john@example.com

Subject:
Meeting

Body:
Hello John,
The meeting has been moved to tomorrow.
```

---

## GitHub Search

```
Find where JWT verification happens.
```

---

## Notion

```
Add a new task called

Deploy backend.
```

---

## Database

```
Show total revenue from last month.
```

---

# Security

* JWT Authentication
* OAuth2 Authorization
* Password hashing
* Token expiration
* Refresh token rotation
* SQL Injection protection through SQLAlchemy
* Async database sessions
* Environment variables
* Request validation with Pydantic

---

# Future Improvements

* Slack Tool
* Telegram Tool
* Discord Tool
* Google Calendar
* Google Drive
* Google Sheets
* GitLab Integration
* Jira Integration
* Redis caching
* Streaming responses
* Multi-agent architecture
* Vector database memory
* Long-term memory
* RAG support
* MCP integration
* Background task queue
* WebSocket support

---

# Performance

* Fully asynchronous
* Connection pooling
* Repository pattern
* Service layer architecture
* Modular design
* Scalable tool system
* Easy to extend

---

# Contributing

1. Fork the repository.
2. Create a feature branch.
3. Commit your changes.
4. Push your branch.
5. Open a Pull Request.

---

# License

This project is licensed under the MIT License.

---

# Author

Developed by **Yassine**.

If you found this project useful, consider giving it a ⭐ on GitHub!
