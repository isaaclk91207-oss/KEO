from google.adk import Agent  # Import the Agent class from google.adk framework (for creating software agents)
from config.gemini_client import get_client  # Import function to get Gemini API client

class FinanceAgent:
    def __init__(self):
        # Initialize the agent with name, model, description, and instruction prompt
        self.agent = Agent(
            name="finance_agent",
            model="gemini-2.5-flash",
            description="Finance department agent for budget and procurement",
            instruction="""You are the Finance agent. Handle budget validation,
cost approvals, and financial operations."""
        )
        self.client = get_client()  # Create a Gemini client instance for model API access
        self.budget_limit = 200000  # Set the maximum budget limit for approval

    def execute(self, action, params):
        """
        Execute Finance action based on the given action name and parameters.
        Dispatches to the appropriate method depending on the action.
        """
        if action == "check_budget":
            # Route to budget checking logic
            return self.check_budget(params)
        elif action == "approve_expense":
            # Route to expense approval logic
            return self.approve_expense(params)
        # If action unknown, return an error response
        return {"error": f"Unknown action: {action}"}
    
    def check_budget(self, params):
        """
        Check if the requested amount is within the budget limit.
        Returns status, approval flag, and message.
        """
        amount = params.get("amount") or 0  # Get the requested amount from parameters (default to 0)
        if isinstance(amount, str):
            # Remove PII redaction markers and non-numeric chars
            import re
            amount = re.sub(r'\[.*?_REDACTED\]', '0', amount)
            amount = re.sub(r'[^0-9.]', '', amount) or 0
            amount = int(float(amount))
        approved = amount <= self.budget_limit  # Check if amount is less than or equal to budget limit
        
        # Build and return a structured response indicating approval result
        return {
            "status": "complete",
            "approved": approved,
            "amount": amount,
            "limit": self.budget_limit,
            "message": f"Budget {'approved' if approved else 'exceeded'}"
        }
    
    def approve_expense(self, params):
        """
        Approve the expense request.
        TODO: Implement actual approval logic in future.
        """
        # For now, always return pending/false since implementation is not done
        return {"status": "pending", "approved": False}
