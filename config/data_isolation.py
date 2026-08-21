import json
import os

DATA_DIR = "logs/department_data"

def ensure_data_dir():
    os.makedirs(DATA_DIR, exist_ok=True)

def load_data(filepath):
    ensure_data_dir()
    if os.path.exists(filepath):
        with open(filepath, "r") as f:
            return json.load(f)
    return {}

def save_data(filepath, data):
    ensure_data_dir()
    with open(filepath, "w") as f:
        json.dump(data, f, indent=2)

class DataIsolation:
    def __init__(self, use_firestore=False):
        self.use_firestore = use_firestore
        self.departments = ["hr", "finance", "it"]
        
        if use_firestore:
            from google.cloud import firestore
            self.db = firestore.Client(project="koala-fleet")
        
        self.cross_access_requests = {}
    
    def store_department_data(self, department, key, value):
        if department not in self.departments:
            return {"error": f"Unknown department: {department}"}
        
        if self.use_firestore:
            self.db.collection(f"{department}_data").document(key).set({
                "value": value,
                "department": department,
                "key": key
            })
        else:
            filepath = f"{DATA_DIR}/{department}.json"
            data = load_data(filepath)
            data[key] = {"value": value, "department": department, "key": key}
            save_data(filepath, data)
        
        return {"status": "stored", "department": department, "key": key}
    
    def get_department_data(self, department, key):
        if department not in self.departments:
            return {"error": f"Unknown department: {department}"}
        
        if self.use_firestore:
            doc_ref = self.db.collection(f"{department}_data").document(key)
            doc = doc_ref.get()
            if doc.exists:
                return doc.to_dict()
            return {"error": "Not found"}
        else:
            filepath = f"{DATA_DIR}/{department}.json"
            data = load_data(filepath)
            return data.get(key, {"error": "Not found"})
    
    def request_cross_access(self, from_dept, to_dept, key):
        request_id = f"{from_dept}_{to_dept}_{key}"
        
        self.cross_access_requests[request_id] = {
            "from": from_dept,
            "to": to_dept,
            "key": key,
            "status": "pending"
        }
        
        if self.use_firestore:
            self.db.collection("cross_access_requests").document(request_id).set({
                "from_dept": from_dept,
                "to_dept": to_dept,
                "key": key,
                "status": "pending"
            })
        else:
            filepath = f"{DATA_DIR}/cross_access.json"
            data = load_data(filepath)
            data[request_id] = self.cross_access_requests[request_id]
            save_data(filepath, data)
        
        return {"request_id": request_id, "status": "pending"}
    
    def approve_cross_access(self, request_id):
        if request_id in self.cross_access_requests:
            self.cross_access_requests[request_id]["status"] = "approved"
            
            if self.use_firestore:
                self.db.collection("cross_access_requests").document(request_id).update({
                    "status": "approved"
                })
            else:
                filepath = f"{DATA_DIR}/cross_access.json"
                data = load_data(filepath)
                if request_id in data:
                    data[request_id]["status"] = "approved"
                    save_data(filepath, data)
            
            return {"status": "approved", "request_id": request_id}
        
        return {"error": "Request not found"}
    
    def get_cross_access_data(self, request_id):
        if request_id not in self.cross_access_requests:
            return {"error": "Request not found"}
        
        req = self.cross_access_requests[request_id]
        
        if req["status"] != "approved":
            return {"error": "Access not approved"}
        
        return self.get_department_data(req["to"], req["key"])

def create_data_isolation(use_firestore=False):
    return DataIsolation(use_firestore=use_firestore)
