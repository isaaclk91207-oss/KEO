# koala Fleet 🐨

> Cross-Department AI Agent Orchestration for Enterprise

[![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)](https://python.org)
[![Gemini](https://img.shields.io/badge/Gemini-3.6-FF6B35.svg)](https://ai.google.dev)
[![Google Cloud](https://img.shields.io/badge/Google%20Cloud-4285F4.svg)](https://cloud.google.com)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

---

## The Problem

Enterprise AI agents work in **silos**. An HR bot can't talk to Finance. Finance can't coordinate with IT. Complex workflows like employee onboarding require **manual human intervention** across 3-4 departments.

## The Solution

**Koala Fleet** is a central orchestrator that autonomously coordinates operations across siloed departmental agents with **zero-trust security** and **end-to-end execution**.

```
User: "Hire a Senior Developer, budget $150K, need MacBook Pro"

    ┌─────────────────────────────────────────────┐
    │           KOALA ORCHESTRATOR                │
    │   (Gemini 3.6 Pro - Complex Reasoning)      │
    └──────────────────┬──────────────────────────┘
                       │
         ┌─────────────┼─────────────┐
         ▼             ▼             ▼
    ┌─────────┐   ┌─────────┐   ┌─────────┐
    │   HR    │   │FINANCE  │   │   IT    │
    │  Agent  │   │  Agent  │   │  Agent  │
    │         │   │         │   │         │
    │ • Jobs  │   │ • Budget│   │ • Order │
    │ • Hire  │   │ • Approve│  │ • Setup │
    └─────────┘   └─────────┘   └─────────┘
         │             │             │
         └─────────────┴─────────────┘
                       │
              ┌────────────────┐
              │  SECURITY      │
              │  • Model Armor │
              │  • Gateway     │
              │  • Audit Log   │
              └────────────────┘
```

---

## Features

| Feature | Description |
|---------|-------------|
| **Multi-Agent Orchestration** | Coordinates HR, Finance, and IT agents automatically |
| **PII Detection** | Blocks sensitive data (SSN, salary) from leaking |
| **Zero-Trust Auth** | Every agent-to-agent call is signed and verified |
| **Audit Logging** | Complete trail of all actions for compliance |
| **Streamlit Dashboard** | Beautiful UI to run workflows and view results |

---

## Tech Stack

- **Model:** Gemini 3.6 Flash / Pro
- **Framework:** Google Agent Development Kit (ADK)
- **Frontend:** Streamlit
- **Storage:** Local JSON (Firestore-ready)
- **Security:** Custom Model Armor + Agent Gateway

---

## Quick Start

### Prerequisites

- Python 3.10+
- Google Gemini API Key ([Get one here](https://aistudio.google.com/apikey))

### Installation

```bash
# Clone the repo
git clone https://github.com/isaaclk91207-oss/KEO.git
cd KEO

# Create virtual environment
python -m venv venv
.\venv\Scripts\activate  # Windows
# source venv/bin/activate  # Mac/Linux

# Install dependencies
pip install -r requirements.txt
```

### Configuration

```bash
# Copy example env file
cp .env.example .env

# Edit .env and add your API key
GOOGLE_API_KEY=your_api_key_here
GOOGLE_CLOUD_PROJECT=your_project_id
GOOGLE_CLOUD_LOCATION=us-central1
```

### Run

```bash
# Run the Streamlit dashboard
streamlit run app.py

# Or run the CLI version
python main.py
```

---

## Project Structure

```
KEO/
├── app.py                  # Streamlit frontend
├── main.py                 # Backend workflow engine
├── agents/
│   ├── orchestrator.py     # Central coordinator
│   ├── registry.py         # Agent registry
│   ├── hr_agent/           # HR department
│   ├── finance_agent/      # Finance department
│   └── it_agent/           # IT department
├── config/
│   ├── gemini_client.py    # Gemini API wrapper
│   ├── model_armor.py      # PII detection
│   ├── agent_gateway.py    # Authentication
│   ├── audit_logger.py     # Action logging
│   ├── data_isolation.py   # Department isolation
│   └── task_schema.py      # Task definitions
├── requirements.txt
├── .env.example
└── koala-fleet-technical-plan.md
```

---

## Security

### Model Armor
- Detects and blocks PII (SSN, emails, salaries)
- Prevents prompt injection attacks
- Screens all inputs and outputs

### Agent Gateway
- Zero-trust authentication
- Request signing with SHA-256
- 5-minute token expiry

### Audit Logger
- Logs every action
- Tracks agent communications
- Stores for compliance

---

## Example Usage

**Input:**
```
Hire a Senior Developer, budget $150K, need MacBook Pro
```

**Output:**
```
✅ HR Agent: Job posting created (1932 chars)
✅ Finance Agent: Budget approved ($150K < $200K limit)
✅ IT Agent: MacBook Pro ordered (ORD-6698, $2,499)
```

**Security:**
```
🔍 PII Scan: SAFE
🔐 Gateway: Verified
📝 Audit: Logged
```

---

## Hackathon Track

**The Fortified Enterprise Fleet**

Building enterprise-scale multi-agent orchestration with security and observability using the Gemini Enterprise Agent Platform (GEAP).

---

## License

MIT License - see [LICENSE](LICENSE) for details.

---

## Built With

- [Google Gemini](https://ai.google.dev) - AI Models
- [Google ADK](https://github.com/google/adk-python) - Agent Framework
- [Streamlit](https://streamlit.io) - Frontend UI

---

<p align="center">
  Built for the <b>All Things Agentic Hackathon 2026</b> 🐨
</p>
