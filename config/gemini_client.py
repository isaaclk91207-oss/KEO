import os
import time
from google import genai
from google.genai import types

class GeminiClient:
    def __init__(self):
        api_key = os.getenv("GOOGLE_API_KEY")
        if not api_key:
            try:
                import streamlit as st
                api_key = st.secrets.get("GOOGLE_API_KEY", "")
                if api_key:
                    os.environ["GOOGLE_API_KEY"] = api_key
            except Exception as e:
                print(f"[Secrets Error] {e}")
        if not api_key:
            raise ValueError(
                "GOOGLE_API_KEY not set. "
                "Add it to Streamlit secrets as: GOOGLE_API_KEY = \"your_key\" "
                "(with quotes!) or set it in .env"
            )
        self.client = genai.Client(api_key=api_key)
    
    def generate(self, prompt, model="gemini-3.6-flash", retries=3):
        """Generate response from Gemini with retry"""
        for attempt in range(retries):
            try:
                response = self.client.models.generate_content(
                    model=model,
                    contents=prompt
                )
                return response.text
            except Exception as e:
                if "503" in str(e) and attempt < retries - 1:
                    print(f"    [Retry {attempt + 1}/{retries}] API busy, waiting...")
                    time.sleep(2 ** attempt)
                else:
                    raise
    
    def generate_json(self, prompt, model="gemini-3.6-flash", retries=3):
        """Generate response and parse as JSON"""
        for attempt in range(retries):
            try:
                response = self.client.models.generate_content(
                    model=model,
                    contents=prompt
                )
                return response.text
            except Exception as e:
                print(f"    [Gemini Error] {type(e).__name__}: {e}")
                if "503" in str(e) and attempt < retries - 1:
                    print(f"    [Retry {attempt + 1}/{retries}] API busy, waiting...")
                    time.sleep(2 ** attempt)
                else:
                    raise

_client = None

def get_client():
    global _client
    if _client is None:
        _client = GeminiClient()
    return _client
