import json
from google.adk import Agent
from config.gemini_client import get_client
from config.task_schema import Task, Department, TaskStatus

class Orchestrator:
    def __init__(self):
        self.agent = Agent(
            name="koala_orchestrator",
            model="gemini-3.6-pro",
            description="Central orchestrator for cross-department coordination",
            instruction="""You are the Koala Fleet orchestrator.
Parse user requests, decompose into sub-tasks, and route to department agents."""
        )
        self.client = get_client()
    
    def parse_intent(self, user_input):
        """Parse user input into structured tasks using Gemini"""
        prompt = f"""Parse this request into tasks. Return JSON array.

User: "{user_input}"

Return format:
[
  {{"department": "hr", "action": "create_job_posting", "params": {{"role": "role name", "requirements": "requirements"}}}},
  {{"department": "finance", "action": "check_budget", "params": {{"amount": 150000}}}},
  {{"department": "it", "action": "provision_hardware", "params": {{"device": "MacBook Pro"}}}}
]

Departments: hr, finance, it
Actions: create_job_posting, check_budget, provision_hardware, screen_candidate, approve_expense, setup_software

Return ONLY the JSON array, no explanation."""
        
        response = self.client.generate_json(prompt)
        
        try:
            tasks_data = json.loads(response)
            tasks = []
            for t in tasks_data:
                task = Task(
                    department=Department(t["department"]),
                    action=t["action"],
                    params=t.get("params", {})
                )
                tasks.append(task)
            return tasks
        except Exception as e:
            print(f"Parse error: {e}")
            return []
    
    def route_tasks(self, tasks, registry):
        """Route tasks to appropriate agents"""
        results = []
        for task in tasks:
            agent = registry.get_agent(task.department.value)
            if agent:
                task.status = TaskStatus.RUNNING
                result = agent.execute(task.action, task.params)
                task.result = result
                task.status = TaskStatus.COMPLETE
                results.append(task)
        return results

def create_orchestrator():
    return Orchestrator()
