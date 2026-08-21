import hashlib
import time
import json
import os

AGENTS_FILE = "logs/agent_keys.json"
COMM_FILE = "logs/communications.json"

def ensure_logs_dir():
    os.makedirs("logs", exist_ok=True)

def load_json(filepath):
    ensure_logs_dir()
    if os.path.exists(filepath):
        with open(filepath, "r") as f:
            return json.load(f)
    return {}

def save_json(filepath, data):
    ensure_logs_dir()
    with open(filepath, "w") as f:
        json.dump(data, f, indent=2)

class AgentGateway:
    def __init__(self, use_firestore=False):
        self.use_firestore = use_firestore
        self.agents = {}
        
        if use_firestore:
            from google.cloud import firestore
            self.db = firestore.Client(project="koala-fleet")
        else:
            self.agents = load_json(AGENTS_FILE)
        
        self._register_default_agents()
    
    def _register_default_agents(self):
        default_agents = {
            "koala_orchestrator": "orch_key_001",
            "hr_agent": "hr_key_001",
            "finance_agent": "finance_key_001",
            "it_agent": "it_key_001"
        }
        
        for agent_id, api_key in default_agents.items():
            if agent_id not in self.agents:
                self.agents[agent_id] = api_key
                
                if self.use_firestore:
                    self.db.collection("agent_keys").document(agent_id).set({
                        "api_key": api_key,
                        "registered_at": time.time()
                    })
            
        if not self.use_firestore:
            save_json(AGENTS_FILE, self.agents)
    
    def generate_agent_id(self, department):
        return f"{department}_agent"
    
    def sign_request(self, agent_id, payload):
        api_key = self.agents.get(agent_id)
        if not api_key:
            return None
        
        sign_string = f"{agent_id}:{json.dumps(payload, sort_keys=True)}:{api_key}"
        signature = hashlib.sha256(sign_string.encode()).hexdigest()
        
        return {
            "agent_id": agent_id,
            "signature": signature,
            "timestamp": time.time()
        }
    
    def verify_request(self, agent_id, payload, signature_data):
        if not signature_data:
            return False
        
        api_key = self.agents.get(agent_id)
        if not api_key:
            return False
        
        if time.time() - signature_data.get("timestamp", 0) > 300:
            return False
        
        sign_string = f"{agent_id}:{json.dumps(payload, sort_keys=True)}:{api_key}"
        expected = hashlib.sha256(sign_string.encode()).hexdigest()
        
        return signature_data.get("signature") == expected
    
    def log_communication(self, from_agent, to_agent, action, status):
        doc = {
            "from": from_agent,
            "to": to_agent,
            "action": action,
            "status": status,
            "timestamp": time.time()
        }
        
        if self.use_firestore:
            self.db.collection("agent_communications").add(doc)
        else:
            logs = load_json(COMM_FILE) if os.path.exists(COMM_FILE) else []
            if not isinstance(logs, list):
                logs = []
            logs.append(doc)
            save_json(COMM_FILE, logs)

def create_gateway(use_firestore=False):
    return AgentGateway(use_firestore=use_firestore)
