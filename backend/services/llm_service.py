from dotenv import load_dotenv
from langchain_groq import ChatGroq
import os
from typing import Dict, Any

load_dotenv()


class LLMService:
    def __init__(self):
        self.llm_models = {
            "llama-3.3-70b-versatile": {
                "api_key": os.getenv("GROQ_API_KEY"),
                "model_name": "llama-3.3-70b-versatile"
            },
            "llama-3.1-8b-instant": {
                "api_key": os.getenv("GROQ_API_KEY"),
                "model_name": "llama-3.1-8b-instant"
            },
            "deepseek-r1-distill-llama-70b": {
                "api_key": os.getenv("GROQ_API_KEY"),
                "model_name": "deepseek-r1-distill-llama-70b"
            }
        }

    def initialize_llm(self, model_name: str):
        """Initialize a language model with the specified name."""
        if model_name in self.llm_models:
            api_key = self.llm_models[model_name]["api_key"]
            model_name = self.llm_models[model_name]["model_name"]
            return ChatGroq(groq_api_key=api_key, model_name=model_name)
        else:
            raise ValueError(f"Invalid model name: {model_name}")

    def generate_response(self, prompt: str, model_name: str) -> str:
        """Generate a response from the LLM based on the prompt."""
        llm = self.initialize_llm(model_name)
        response = llm.invoke(prompt)
        return response.content