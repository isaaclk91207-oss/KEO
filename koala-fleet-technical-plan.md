# Koala Fleet - Technical Plan

## Project Overview

**Name:** Koala Fleet: Cross-Department AI Agent  
**Track:** The Fortified Enterprise Fleet  
**Goal:** Build a central orchestrator agent that autonomously coordinates operations across siloed departmental agents with zero-trust security

---

## Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                        USER INPUT                          │
│  "We are hiring a Senior Developer. Arrange budget,        │
│   job posting, and hardware."                               │
└──────────────────────────┬──────────────────────────────────┘
                           │
                           ▼
┌─────────────────────────────────────────────────────────────┐
│                  KOALA ORCHESTRATOR                         │
│  • Intent Parsing (Gemini 3.5 Pro)                          │
│  • Task Decomposition                                       │
│  • Cross-Agent Coordination                                 │
└──────────────────────────┬──────────────────────────────────┘
                           │
              ┌────────────┼────────────┐
              ▼            ▼            ▼
┌──────────────┐  ┌──────────────┐  ┌──────────────┐
│   HR AGENT   │  │   IT AGENT   │  │FINANCE AGENT │
│ (Gemini Flash)│  │ (Gemini Flash)│  │(Gemini Flash) │
│ • Job posting │  │ • Hardware    │  │ • Budget      │
│ • Profiles    │  │   provisioning│  │   check       │
└──────┬───────┘  └──────┬───────┘  └──────┬───────┘
       │                 │                 │
       └────────────┬────┴─────────────────┘
                    ▼
┌─────────────────────────────────────────────────────────────┐
│                    GEAP SECURITY LAYER                      │
│  • Agent Gateway (Zero-Trust Auth)                          │
│  • Model Armor (PII/Injection Screening)                    │
│  • Memory Bank (State Persistence)                          │
└──────────────────────────┬──────────────────────────────────┘
                           │
                           ▼
┌─────────────────────────────────────────────────────────────┐
│                   GOOGLE CLOUD INFRA                        │
│  • Cloud Run (Serverless Hosting)                           │
│  • Firestore (State Management)                             │
│  • Vertex AI (Model Serving)                                │
└─────────────────────────────────────────────────────────────┘
```

---

## MVP Scope: Employee Onboarding Workflow

### Single Demo Scenario
**Input:** "Hire a Senior Developer in Engineering, budget $150K, need MacBook Pro"

**Automated Flow:**
1. Orchestrator parses intent → 3 sub-tasks
2. HR Agent → Creates job posting, initiates candidate pipeline
3. Finance Agent → Validates budget allocation, reserves funds
4. IT Agent → Pre-orders MacBook Pro based on role template
5. Orchestrator → Aggregates results, returns status summary

---

## Tech Stack

| Component | Technology | Purpose |
|-----------|------------|---------|
| **Orchestrator Model** | Gemini 3.5 Pro | Complex reasoning, task planning |
| **Sub-Agent Model** | Gemini 3.5 Flash | Low-cost task execution |
| **Framework** | Google ADK | Agent lifecycle, tooling |
| **Hosting** | Cloud Run | Serverless, scale-to-zero |
| **State** | Firestore | Session memory, workflow state |
| **Security** | Model Armor | PII screening, injection prevention |
| **Auth** | Agent Identity | Zero-trust agent-to-agent communication |

---

## Implementation Plan

### Phase 1: Foundation (Days 1-2)
- [ ] Set up Google Cloud project
- [ ] Enable Vertex AI, Cloud Run, Firestore
- [ ] Initialize ADK project structure
- [ ] Configure Gemini API access   

### Phase 2: Orchestrator Agent (Days 3-4)
- [ ] Implement intent parsing logic
- [ ] Build task decomposition engine
- [ ] Create agent routing mechanism
- [ ] Add basic error handling

### Phase 3: Department Agents (Days 5-7)
- [ ] HR Agent - Job posting generation
- [ ] Finance Agent - Budget validation logic
- [ ] IT Agent - Hardware provisioning workflow
- [ ] Each agent with isolated Firestore collections

### Phase 4: Security Layer (Days 8-9)
- [ ] Agent Gateway - Request/response authentication
- [ ] Model Armor - PII detection and masking
- [ ] Audit logging for compliance

### Phase 5: Integration & Demo (Days 10-12)
- [ ] End-to-end workflow testing
- [ ] Demo video recording
- [ ] GitHub repository cleanup
- [ ] Architecture diagram finalization

---

## Data Flow

```
User Request
    │
    ▼
Orchestrator (Gemini Pro)
    │
    ├─► HR Agent ──► Firestore (HR Collection)
    │
    ├─► Finance Agent ──► Firestore (Finance Collection)
    │
    └─► IT Agent ──► Firestore (IT Collection)
    
All requests pass through:
    • Agent Gateway (auth verification)
    • Model Armor (PII screening)
```

---

## Security Design

### Zero-Trust Model
1. **Agent Identity:** Each agent has unique credentials
2. **Request Signing:** All inter-agent calls are cryptographically signed
3. **Model Armor:** Screens all inputs/outputs for:
   - PII detection (SSN, salary, personal data)
   - Prompt injection attempts
   - Data leakage prevention

### Data Isolation
- Each department has isolated Firestore collections
- Cross-department queries require explicit authorization
- All access logged for audit trail

---

## Demo Script (4 Minutes)

| Time | Action | Screen |
|------|--------|--------|
| 0:00 | Intro + Problem Statement | Slides |
| 0:30 | Show user input prompt | Terminal |
| 0:45 | Orchestrator parses & routes | Dashboard |
| 1:15 | HR Agent executes | HR Agent UI |
| 1:45 | Finance Agent executes | Finance Agent UI |
| 2:15 | IT Agent executes | IT Agent UI |
| 2:45 | Results aggregated | Orchestrator View |
| 3:15 | Security layer demo | Model Armor logs |
| 3:45 | Wrap-up + call to action | Slides |

---

## Deliverables Checklist

- [ ] 4-minute demo video
- [ ] Public GitHub repository
- [ ] Architecture diagram
- [ ] Written pitch document
- [ ] Live working demo

---

## Risk Mitigation

| Risk | Mitigation |
|------|------------|
| GEAP limited availability | Build custom security layer as fallback |
| API rate limits | Implement retry logic, caching |
| Demo failures | Pre-record backup, test extensively |
| Scope creep | Stick to single workflow MVP |

---

## Success Metrics

1. **Cross-agent coordination:** Orchestrator successfully delegates to 3+ agents
2. **Security:** Model Armor catches PII in test cases
3. **State persistence:** Workflow resumes after interruption
4. **Demo quality:** Smooth 4-minute presentation
