from agents.hr_agent import HRAgent
from agents.finance_agent import FinanceAgent
from agents.it_agent import ITAgent

class AgentRegistry:
    def __init__(self):
        self.agents = {
            "hr": HRAgent(),
            "finance": FinanceAgent(),
            "it": ITAgent()
        }
    
    def get_agent(self, department):
        return self.agents.get(department)
    
    def list_agents(self):
        return list(self.agents.keys())

def create_registry():
    return AgentRegistry()
