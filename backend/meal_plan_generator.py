"""
Meal plan generator module.
Orchestrates the meal plan generation process using the Gemini API.
Uses Firebase user data and RAG enrichment for context-aware generation.
"""

from gemini_client import GeminiClient


class MealPlanGenerator:
    """Generates personalized meal plans based on Firebase user data."""

    def __init__(self):
        """Initialize the meal plan generator with a Gemini client."""
        self.client = GeminiClient()

    def generate_meal(self, user_id: str, use_mock: bool = True) -> str:
        """
        Generate a meal recommendation using RAG-enriched Firebase user data.
        
        This is the primary method for meal generation. It:
        - Retrieves user profile from Firebase (dietary restrictions, nutrition goals, favorites)
        - Analyzes past meal history to ensure variety
        - Uses RAG enrichment to understand user patterns
        - Generates a meal different from previous suggestions
        - Provides context-aware, personalized recommendations

        Args:
            user_id: Firebase user ID (e.g., "USER_001")
            use_mock: Use mock data for development (default: True until Firebase setup complete)
                     Set to False when Firebase is connected and credentials are configured

        Returns:
            str: Formatted meal plan text containing:
                - Recipe name
                - Comprehensive ingredients list with amounts
                - Step-by-step cooking instructions

        Raises:
            ValueError: If user ID is empty or user not found
            Exception: If API communication or Firebase retrieval fails
            
        Example:
            generator = MealPlanGenerator()
            # Using mock data (development)
            meal = generator.generate_meal("USER_001", use_mock=True)
            
            # Using Firebase (production)
            meal = generator.generate_meal("USER_001", use_mock=False)
        """
        if not user_id or not user_id.strip():
            raise ValueError("User ID cannot be empty")

        # Generate meal plan using Gemini API with RAG-enriched context
        meal_plan = self.client.generate_meal_plan(
            user_id=user_id,
            use_mock=use_mock
        )

        return meal_plan

    def generate_multiple_meals(
        self,
        user_id: str,
        count: int = 3,
        use_mock: bool = True,
    ) -> list:
        """
        Generate multiple unique meal recommendations for a user.
        
        This method generates multiple meals while:
        - Respecting the user's past meal history
        - Ensuring variety based on user preferences
        - Using the same Firebase profile for all meals
        - Following the user's meal plan length preference

        Args:
            user_id: Firebase user ID
            count: Number of meals to generate (default: 3)
            use_mock: Use mock data for development (default: True)

        Returns:
            list: List of meal plan strings

        Raises:
            ValueError: If user not found or count is invalid
            Exception: If API communication fails
            
        Example:
            generator = MealPlanGenerator()
            meals = generator.generate_multiple_meals("USER_001", count=5)
        """
        if count < 1:
            raise ValueError("Count must be at least 1")
        if not user_id or not user_id.strip():
            raise ValueError("User ID cannot be empty")

        meals = []
        for i in range(count):
            try:
                meal = self.generate_meal(
                    user_id=user_id,
                    use_mock=use_mock
                )
                meals.append(meal)
            except Exception as e:
                raise Exception(
                    f"Error generating meal {i + 1} for user {user_id}: {str(e)}"
                ) from e

        return meals
