# Koala Fleet: Cross-Department AI Agent

## The Journey

### Day 1: The Problem

It started with a simple question: **Why can't AI agents talk to each other?**

Enterprise teams use AI bots everywhere — HR has a chatbot, Finance has an assistant, IT has a helpdesk bot. But they all work in **silos**. When you need to onboard a new employee, you still have to:

1. Email HR to create the profile
2. Call Finance to set up payroll
3. Submit a ticket to IT for laptop
4. Follow up with each department

**The irony?** We have AI in every department, but humans still coordinate between them.

### Day 2: The Vision

What if there was a **central brain** that could:

- Understand a complex request
- Break it into department-specific tasks
- Coordinate all agents simultaneously
- Ensure security across all communications

That's when **Koala Fleet** was born — a cross-department AI orchestrator that unites siloed agents into a unified ecosystem.

### Day 3-5: Building the Brain

We started with the orchestrator using **Gemini 3.6 Pro**. The challenge was making it understand complex intent:

> "Hire a Senior Developer, budget $150K, need MacBook Pro"

This single sentence needs to trigger **three separate workflows**:
- HR: Create job posting
- Finance: Validate budget
- IT: Order hardware

Using **Google ADK**, we built the task decomposition engine that parses intent and routes to the right agents.

### Day 6-7: The Agents

Each department agent runs on **Gemini 3.6 Flash** for cost efficiency:

| Agent | Responsibility | Output |
|-------|---------------|--------|
| HR | Job postings, screening | Generated job description |
| Finance | Budget validation | Approval with amount check |
| IT | Hardware provisioning | Order confirmation |

### Day 8: The Security Layer

The Fortified Enterprise Fleet track demands **enterprise-grade security**. We built:

**Model Armor:**
- Scans all text for PII (SSN, emails, salaries)
- Blocks sensitive data before it reaches agents
- Prevents prompt injection attacks

**Agent Gateway:**
- Zero-trust authentication
- SHA-256 request signing
- 5-minute token expiry
- All communications logged

**Audit Logger:**
- Every action recorded
- Complete compliance trail
- Queryable logs

### Day 9: The Dashboard

We built a **Streamlit dashboard** that shows:
- Real-time workflow execution
- Agent status cards
- PII detection tests
- Audit log viewer

### Day 10: Demo Day

The final demo workflow:

```
Input: "Hire a Senior Developer, budget $150K, need MacBook Pro"

[Security] PII Scan: SAFE
[Orchestrator] Parsing intent... 3 tasks found
[Gateway] Signing & routing...
[HR] Job posting created (1932 chars)
[Finance] Budget approved ($150K < $200K limit)
[IT] MacBook Pro ordered (ORD-6698, $2,499)
[Audit] Workflow logged
```

---

## What We Learned

1. **Multi-agent coordination is hard** — But Gemini's reasoning makes it possible
2. **Security can't be an afterthought** — Model Armor catches PII before it leaks
3. **Simple APIs win** — Simple API key auth was enough for the demo
4. **Visual feedback matters** — The dashboard makes the abstract tangible

---

## Impact

**For Enterprises:**
- Onboarding time: Days → Minutes
- Manual coordination: Eliminated
- Security: Zero-trust by default
- Compliance: Automatic audit trail

**For the Future:**
- Extend to more departments (Legal, Marketing)
- Add human-in-the-loop approvals
- Integrate with real HRIS/ERP systems
- Scale with Google Cloud Run

---

## Tech Stack

- **AI:** Gemini 3.6 Flash/Pro
- **Framework:** Google ADK
- **Frontend:** Streamlit
- **Security:** Custom Model Armor + Gateway
- **Storage:** Firestore-ready (local JSON for demo)

---

## Team

Built solo for the All Things Agentic Hackathon 2026

---

## Links

- **GitHub:** https://github.com/isaaclk91207-oss/KEO
- **Demo:** Run `streamlit run app.py`
- **Track:** The Fortified Enterprise Fleet
