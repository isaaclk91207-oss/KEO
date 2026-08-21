from dataclasses import dataclass
from typing import Any
from enum import Enum

class Department(Enum):
    HR = "hr"
    FINANCE = "finance"
    IT = "it"

class TaskStatus(Enum):
    PENDING = "pending"
    RUNNING = "running"
    COMPLETE = "complete"
    FAILED = "failed"

@dataclass
class Task:
    department: Department
    action: str
    params: dict
    status: TaskStatus = TaskStatus.PENDING
    result: Any = None
    
    def to_dict(self):
        return {
            "department": self.department.value,
            "action": self.action,
            "params": self.params,
            "status": self.status.value,
            "result": self.result
        }

@dataclass
class Workflow:
    id: str
    user_input: str
    tasks: list
    status: str = "running"
    
    def to_dict(self):
        return {
            "id": self.id,
            "user_input": self.user_input,
            "tasks": [t.to_dict() for t in self.tasks],
            "status": self.status
        }
