"""
Gemini API client for meal plan generation.
Handles communication with Google's Generative AI API.
"""

import google.generativeai as genai
from config import GEMINI_API_KEY, GEMINI_MODEL, MEAL_PLAN_TEMPERATURE, MEAL_PLAN_MAX_TOKENS


class GeminiClient:
    """Client for interacting with the Gemini API."""

    def __init__(self):
        """Initialize the Gemini client with API key."""
        genai.configure(api_key=GEMINI_API_KEY)
        self.model = GEMINI_MODEL
        self.temperature = MEAL_PLAN_TEMPERATURE
        self.max_tokens = MEAL_PLAN_MAX_TOKENS

    def generate_meal_plan(self, user_id: str, use_mock: bool = True) -> str:
        """
        Generate a unique meal plan using RAG-enriched context from Firebase user data.
        
        This is the primary method for meal generation. It:
        1. Retrieves user data from Firebase via firebase_service
        2. Enriches context using Backboard.io RAG pipeline
        3. Generates meal with full user history context
        4. Ensures the meal is different from past suggestions
        
        Args:
            user_id: Firebase user ID (e.g., "USER_001")
            use_mock: Use mock data for development (default: True until Firebase setup complete)
                     Set to False when Firebase is connected and credentials are configured

        Returns:
            str: Generated meal plan text from Gemini API

        Raises:
            ValueError: If user not found or inputs invalid
            Exception: For API communication or Firebase retrieval errors
        """
        if not user_id or not user_id.strip():
            raise ValueError("User ID cannot be empty")

        from backboard_rag_pipeline import BackboardRAGPipeline
        
        # Initialize RAG pipeline
        rag_pipeline = BackboardRAGPipeline()
        
        # Retrieve user context from Firebase (or mock data)
        user_meal_data = rag_pipeline.retrieve_user_context(user_id, use_mock=use_mock)
        
        # Augment with RAG analysis
        enriched_data = rag_pipeline.augment_with_rag(user_meal_data)
        
        # Generate RAG-informed context prompt
        rag_context_prompt = rag_pipeline.generate_rag_context_prompt(enriched_data)
        
        # Build the full meal generation prompt with RAG context
        prompt = self._build_rag_informed_prompt(rag_context_prompt)
        
        return self._call_gemini_api(prompt)

    def _call_gemini_api(self, prompt: str) -> str:
        """
        Make the actual API call to Gemini.
        
        Args:
            prompt: The complete prompt for Gemini
            
        Returns:
            str: Generated meal plan text
            
        Raises:
            ValueError: If API returns empty response
            Exception: For API communication errors
        """
        try:
            model = genai.GenerativeModel(
                model_name=self.model,
                generation_config=genai.types.GenerationConfig(
                    temperature=self.temperature,
                    max_output_tokens=self.max_tokens,
                ),
            )

            response = model.generate_content(prompt)

            if not response.text:
                raise ValueError("API returned empty response")

            return response.text

        except Exception as e:
            raise Exception(f"Error communicating with Gemini API: {str(e)}") from e

    @staticmethod
    def _build_rag_informed_prompt(rag_context: str) -> str:
        """
        Build a RAG-informed prompt that includes Firebase user context.
        
        This prompt integrates:
        - RAG-analyzed user profile
        - Past meal history analysis
        - Diversity and novelty requirements
        - Firebase user preferences
        
        Args:
            rag_context: RAG-generated context from BackboardRAGPipeline
            
        Returns:
            str: Complete RAG-informed prompt for Gemini API
        """
        prompt = f"""{rag_context}

MEAL GENERATION INSTRUCTIONS:
Generate ONE unique and creative meal recipe that fulfills all the requirements above.

The meal MUST:
1. Respect all dietary restrictions absolutely
2. Align with the user's nutrition goals
3. Incorporate or build upon the user's favorite foods
4. Be DIFFERENT from previously suggested meals
5. Feel fresh, exciting, and novel to the user
6. Be practical and achievable

RETURN THE MEAL IN EXACTLY THIS FORMAT WITH NO MARKDOWN FORMATTING:

Recipe Name: [Creative and descriptive recipe name]

Ingredients: [List each ingredient on a new line with format: "- [ingredient name]: [amount with unit]". Be comprehensive and include all ingredients needed. Do not include any markdown formatting or asterisks.]

Instructions: [Provide clear, numbered step-by-step cooking instructions. Start each instruction on a new line with the format "1. ", "2. ", "3. " etc. Keep each instruction concise and on a single line. Do not use markdown formatting.]"""
        return prompt.strip()
