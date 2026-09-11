from google.adk import Agent
from config.gemini_client import get_client

class ITAgent:
    def __init__(self):
        self.agent = Agent(
            name="it_agent",
            model="gemini-3.6-flash",
            description="IT department agent for hardware and infrastructure",
            instruction="""You are the IT agent. Handle hardware provisioning,
software setup, and infrastructure requests."""
        )
        self.client = get_client()
        self.hardware_catalog = {
            "macbook pro": {"price": 2499, "specs": "M3 Pro, 18GB RAM, 512GB SSD"},
            "macbook air": {"price": 1299, "specs": "M3, 8GB RAM, 256GB SSD"},
            "dell xps": {"price": 1799, "specs": "i7, 16GB RAM, 512GB SSD"},
            "Lenovo Thinkbook": {"price": 1822, "specs": "i7, 16GB RAM, 256GB SSD"}
        }
    
    def execute(self, action, params):
        """Execute IT action"""
        if action == "provision_hardware":
            return self.provision_hardware(params)
        elif action == "setup_software":
            return self.setup_software(params)
        return {"error": f"Unknown action: {action}"}
    
    def provision_hardware(self, params):
        """Provision hardware based on role"""
        device = params.get("device", "MacBook Pro").lower()
        
        if device in self.hardware_catalog:
            info = self.hardware_catalog[device]
            order_id = f"ORD-{hash(device) % 10000}"
            return {
                "status": "complete",
                "order_id": order_id,
                "device": device.title(),
                "specs": info["specs"],
                "price": info["price"]
            }
        else:
            return {
                "status": "complete",
                "order_id": "ORD-0001",
                "device": device.title(),
                "specs": "Standard configuration",
                "price": 1500
            }
    
    def setup_software(self, params):
        """Setup software access"""
        # TODO: Implement
        return {"status": "pending", "access_granted": False}
