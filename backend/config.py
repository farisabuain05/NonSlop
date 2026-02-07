"""
Configuration module for loading environment variables and API settings.
"""

import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# API Configuration
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

if not GEMINI_API_KEY:
    raise ValueError(
        "GEMINI_API_KEY not found in environment variables. "
        "Please create a .env file with your API key."
    )

# API Model Configuration
GEMINI_MODEL = "gemini-2.5-flash"

# Meal Plan Generation Settings
MEAL_PLAN_TEMPERATURE = 0.9  # Higher temperature for more creative variety
MEAL_PLAN_MAX_TOKENS = 4096  # Increased to ensure complete meal output with instructions
