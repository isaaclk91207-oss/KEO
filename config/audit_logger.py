import json
import time
import os
from datetime import datetime

AUDIT_FILE = "logs/audit_logs.json"
PII_FILE = "logs/pii_logs.json"
WORKFLOW_FILE = "logs/workflow_logs.json"

def ensure_logs_dir():
    os.makedirs("logs", exist_ok=True)

def load_logs(filepath):
    ensure_logs_dir()
    if os.path.exists(filepath):
        with open(filepath, "r") as f:
            return json.load(f)
    return []

def save_logs(filepath, logs):
    ensure_logs_dir()
    with open(filepath, "w") as f:
        json.dump(logs, f, indent=2)

class AuditLogger:
    def __init__(self, use_firestore=False):
        self.use_firestore = use_firestore
        if use_firestore:
            from google.cloud import firestore
            self.db = firestore.Client(project="koala-fleet")
    
    def log_action(self, agent, action, input_text, result, status="success"):
        doc = {
            "agent": agent,
            "action": action,
            "input": str(input_text)[:500],
            "result": str(result)[:500],
            "status": status,
            "timestamp": time.time(),
            "datetime": datetime.now().isoformat()
        }
        
        if self.use_firestore:
            self.db.collection("audit_logs").add(doc)
        else:
            logs = load_logs(AUDIT_FILE)
            logs.append(doc)
            save_logs(AUDIT_FILE, logs)
        
        return doc
    
    def log_pii_scan(self, text, pii_found, action_taken):
        doc = {
            "text_preview": text[:100],
            "pii_found": pii_found,
            "action_taken": action_taken,
            "timestamp": time.time(),
            "datetime": datetime.now().isoformat()
        }
        
        if self.use_firestore:
            self.db.collection("pii_logs").add(doc)
        else:
            logs = load_logs(PII_FILE)
            logs.append(doc)
            save_logs(PII_FILE, logs)
        
        return doc
    
    def log_workflow(self, workflow_id, user_input, tasks, status):
        doc = {
            "workflow_id": workflow_id,
            "user_input": user_input,
            "tasks": tasks,
            "status": status,
            "timestamp": time.time(),
            "datetime": datetime.now().isoformat()
        }
        
        if self.use_firestore:
            self.db.collection("workflow_logs").add(doc)
        else:
            logs = load_logs(WORKFLOW_FILE)
            logs.append(doc)
            save_logs(WORKFLOW_FILE, logs)
        
        return doc
    
    def get_logs(self, collection="audit_logs", agent=None, limit=100):
        if self.use_firestore:
            query = self.db.collection(collection)
            if agent:
                query = query.where("agent", "==", agent)
            docs = query.order_by("timestamp", direction="DESCENDING").limit(limit).stream()
            return [doc.to_dict() for doc in docs]
        else:
            filepath = f"logs/{collection}.json"
            logs = load_logs(filepath)
            if agent:
                logs = [l for l in logs if l.get("agent") == agent]
            return logs[-limit:]
    
    def get_stats(self):
        logs = self.get_logs(limit=1000)
        stats = {
            "total_actions": len(logs),
            "by_agent": {},
            "by_status": {}
        }
        for log in logs:
            agent = log.get("agent", "unknown")
            status = log.get("status", "unknown")
            stats["by_agent"][agent] = stats["by_agent"].get(agent, 0) + 1
            stats["by_status"][status] = stats["by_status"].get(status, 0) + 1
        return stats

def create_audit_logger(use_firestore=False):
    return AuditLogger(use_firestore=use_firestore)
