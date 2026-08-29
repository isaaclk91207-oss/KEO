from google.adk import Agent
from config.gemini_client import get_client

class HRAgent:
    def __init__(self):
        self.agent = Agent(
            name="hr_agent",
            model="gemini-2.5-flash",
            description="HR department agent for job postings and candidate management",
            instruction="""You are the HR agent. Handle job postings, candidate screening,
and employee onboarding tasks."""
        )
        self.client = get_client()
    
    def execute(self, action, params):
        """Execute HR action"""
        if action == "create_job_posting":
            return self.create_job_posting(params)
        elif action == "screen_candidate":
            return self.screen_candidate(params)
        return {"error": f"Unknown action: {action}"}
    
    def create_job_posting(self, params):
        """Generate job posting using Gemini"""
        role = params.get("role", "Software Developer")
        requirements = params.get("requirements", "3+ years experience")
        
        prompt = f"""Create a professional job posting for:
Role: {role}
Requirements: {requirements}

Include:
1. Job title
2. Responsibilities (3-5 bullet points)
3. Requirements (3-5 bullet points)
4. Benefits

Return as formatted text."""
        
        posting = self.client.generate(prompt)
        return {"status": "complete", "posting": posting}
    
    def screen_candidate(self, params):
        """Screen candidate against requirements"""
        # TODO: Implement
        return {"status": "pending", "score": 0}
