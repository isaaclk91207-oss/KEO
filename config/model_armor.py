from config.gemini_client import get_client
import json
import re

class ModelArmor:
    def __init__(self):
        self.client = get_client()
        self.pii_patterns = {
            "ssn": r"\b\d{3}-\d{2}-\d{4}\b",
            "email": r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b",
            "phone": r"\b\d{3}[-.\s]?\d{3}[-.\s]?\d{4}\b",
            "salary": r"\$[\d,]+(?:\.\d{2})?"
        }
    
    def scan_pii(self, text):
        """Scan text for PII using regex patterns"""
        detected = []
        
        for pii_type, pattern in self.pii_patterns.items():
            matches = re.findall(pattern, text)
            if matches:
                detected.append({
                    "type": pii_type,
                    "values": matches,
                    "action": "block" if pii_type in ["ssn"] else "redact"
                })
        
        return {
            "safe": len(detected) == 0,
            "detected": detected
        }
    
    def scan_with_gemini(self, text):
        """Use Gemini for advanced PII detection"""
        prompt = f"""Analyze this text for sensitive data (PII).
Return JSON with format:
{{"safe": true/false, "pii_found": ["type1", "type2"], "action": "block/redact/allow"}}

Text: "{text}"

Return ONLY the JSON, no explanation."""
        
        response = self.client.generate_json(prompt)
        try:
            return json.loads(response)
        except:
            return {"safe": True, "pii_found": [], "action": "allow"}
    
    def redact_pii(self, text):
        """Replace PII with [REDACTED]"""
        redacted = text
        
        for pii_type, pattern in self.pii_patterns.items():
            redacted = re.sub(pattern, f"[{pii_type.upper()}_REDACTED]", redacted)
        
        return redacted
    
    def protect(self, text, use_gemini=False):
        """Main protection function"""
        if use_gemini:
            result = self.scan_with_gemini(text)
        else:
            result = self.scan_pii(text)
        
        if not result["safe"]:
            if any(p.get("action") == "block" for p in result.get("detected", [])):
                return {"allowed": False, "reason": "PII blocked", "details": result}
            else:
                redacted = self.redact_pii(text)
                return {"allowed": True, "text": redacted, "details": result}
        
        return {"allowed": True, "text": text, "details": result}

def create_model_armor():
    return ModelArmor()
