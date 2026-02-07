"""
Utility script to list available Gemini models.
Run this to see which models are available for your API key.
"""

import google.generativeai as genai
from config import GEMINI_API_KEY

genai.configure(api_key=GEMINI_API_KEY)

print("Available Gemini Models:")
print("=" * 60)

try:
    for model in genai.list_models():
        print(f"Name: {model.name}")
        print(f"Display Name: {model.display_name}")
        print(f"Input Token Limit: {model.input_token_limit}")
        if hasattr(model, 'supported_generation_methods'):
            print(f"Supported Methods: {model.supported_generation_methods}")
        print("-" * 60)
except Exception as e:
    print(f"Error listing models: {str(e)}")
