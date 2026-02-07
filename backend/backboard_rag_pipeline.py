"""
Backboard.io RAG and MCP pipeline service.
Handles context enrichment for meal plan generation using RAG (Retrieval-Augmented Generation).
Integrates with Firebase user data to provide informed meal suggestions.
"""

from typing import List, Dict, Optional
from dataclasses import dataclass
from firebase_service import UserMealData


@dataclass
class ContextEnrichedData:
    """Data structure for context-enriched user information."""
    user_id: str
    dietary_restrictions: str
    nutrition_goals: str
    favorite_foods: str
    past_meals_summary: str
    meal_variety_needs: str
    meal_preferences: Dict
    raw_past_meals: List[str]


class BackboardRAGPipeline:
    """
    Backboard.io RAG (Retrieval-Augmented Generation) Pipeline.
    
    This service:
    1. Retrieves user data from Firebase via firebase_service
    2. Processes and enriches the data using RAG principles
    3. Generates context-aware prompts for Gemini API
    4. Tracks which meals have been suggested to avoid repetition
    """

    def __init__(self):
        """Initialize the RAG pipeline."""
        self.previous_meals_database = {}

    def retrieve_user_context(self, user_id: str, use_mock: bool = True) -> UserMealData:
        """
        Retrieve user context from Firebase.
        
        Args:
            user_id: Firebase user ID
            use_mock: Use mock data for development (default: True until Firebase is set up)
            
        Returns:
            UserMealData: User's dietary and preference information
            
        Raises:
            ValueError: If user not found
        """
        from firebase_service import FirebaseService, get_mock_user_meal_data

        if use_mock:
            # Use mock data for development
            return get_mock_user_meal_data(user_id)
        else:
            # Use actual Firebase connection
            firebase_service = FirebaseService()
            return firebase_service.get_user_meal_data(user_id)

    def augment_with_rag(self, user_meal_data: UserMealData) -> ContextEnrichedData:
        """
        Augment user data using RAG principles.
        
        This process:
        1. Analyzes past meal history for patterns and gaps
        2. Identifies cuisine variety needs
        3. Scores ingredient diversity
        4. Generates contextual summaries
        
        Args:
            user_meal_data: Raw user data from Firebase
            
        Returns:
            ContextEnrichedData: Enriched context with RAG analysis
        """
        # Analyze past meals for patterns
        past_meals_summary = self._analyze_past_meals(
            user_meal_data.past_meal_history
        )
        
        # Determine variety needs based on preferences and history
        meal_variety_needs = self._assess_variety_needs(
            user_meal_data.past_meal_history,
            user_meal_data.meal_plan_preferences.get("variety", "high")
        )
        
        return ContextEnrichedData(
            user_id=user_meal_data.user_id,
            dietary_restrictions=user_meal_data.dietary_restrictions,
            nutrition_goals=user_meal_data.nutrition_goals,
            favorite_foods=user_meal_data.favorite_foods,
            past_meals_summary=past_meals_summary,
            meal_variety_needs=meal_variety_needs,
            meal_preferences=user_meal_data.meal_plan_preferences,
            raw_past_meals=user_meal_data.past_meal_history
        )

    @staticmethod
    def _analyze_past_meals(past_meals: List[str]) -> str:
        """
        Analyze past meal history to identify patterns and themes.
        
        Args:
            past_meals: List of past meal names
            
        Returns:
            str: Summary of meal patterns and themes
        """
        if not past_meals:
            return "No previous meal history available."
        
        # Count cuisine patterns
        cuisine_keywords = {
            "mediterranean": 0,
            "asian": 0,
            "thai": 0,
            "indian": 0,
            "mexican": 0,
            "italian": 0
        }
        
        for meal in past_meals:
            meal_lower = meal.lower()
            for cuisine in cuisine_keywords:
                if cuisine in meal_lower:
                    cuisine_keywords[cuisine] += 1
        
        # Count ingredient patterns
        protein_patterns = {
            "tofu": sum(1 for m in past_meals if "tofu" in m.lower()),
            "chickpea": sum(1 for m in past_meals if "chickpea" in m.lower()),
            "lentil": sum(1 for m in past_meals if "lentil" in m.lower()),
            "tempeh": sum(1 for m in past_meals if "tempeh" in m.lower()),
        }
        
        summary = f"User has enjoyed {len(past_meals)} previous meals. "
        summary += f"Cuisine preferences: {', '.join([k for k, v in cuisine_keywords.items() if v > 0])}. "
        summary += f"Preferred proteins: {', '.join([k for k, v in protein_patterns.items() if v > 0])}."
        
        return summary

    @staticmethod
    def _assess_variety_needs(past_meals: List[str], variety_preference: str) -> str:
        """
        Assess how much variety is needed in the next meal generation.
        
        Args:
            past_meals: List of past meal names
            variety_preference: User's variety preference (low, medium, high)
            
        Returns:
            str: Description of variety needs
        """
        if not past_meals or len(past_meals) < 2:
            return "First meal generation for this user. High variety and exploration encouraged."
        
        # Check for repetition
        unique_meals = len(set(past_meals))
        total_meals = len(past_meals)
        repetition_rate = 1 - (unique_meals / total_meals)
        
        if variety_preference.lower() == "high":
            if repetition_rate > 0.3:
                return f"User prefers high variety. Detected {repetition_rate:.0%} meal repetition. Prioritize novel ingredients and cuisines."
            else:
                return "User prefers high variety and has good diversity in past meals. Introduce new cuisines or ingredient combinations."
        elif variety_preference.lower() == "medium":
            return "User prefers moderate variety. Balance between exploring new meals and returning to favorites."
        else:  # low
            return "User prefers consistency. Can repeat favorite meal themes with slight variations."

    def generate_rag_context_prompt(self, enriched_data: ContextEnrichedData) -> str:
        """
        Generate an ultra-concise RAG-informed context prompt for maximum token efficiency.
        Ensures enough tokens remain for full meal output.
        
        Args:
            enriched_data: RAG-augmented user context
            
        Returns:
            str: RAG-informed system context for Gemini
        """
        # Get only last 2 meals to save tokens
        recent_meals = enriched_data.raw_past_meals[-2:] if enriched_data.raw_past_meals else []
        meals_str = ", ".join(recent_meals) if recent_meals else "None"
        
        # Minimal prompt to preserve tokens for output
        context_prompt = f"""AI Meal Assistant Context - Generate ONE different meal:
Dietary Restrictions: {enriched_data.dietary_restrictions}
Nutrition Goals: {enriched_data.nutrition_goals}
Favorite Foods: {enriched_data.favorite_foods}
Previously Suggested: {meals_str}
Task: Create a meal different from the above. Introduce new cuisines or combinations."""
        return context_prompt.strip()

    @staticmethod
    def _format_past_meals_list(past_meals: List[str]) -> str:
        """Format past meals as a readable list."""
        if not past_meals:
            return "No previous meals to reference."
        return "\n".join([f"  • {meal}" for meal in past_meals[-5:]])  # Show last 5 meals
