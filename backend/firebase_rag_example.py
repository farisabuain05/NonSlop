"""
Complete example demonstrating the Firebase → Backboard RAG → Gemini pipeline.

This example shows:
1. Retrieving user data from Firebase (or mock data for development)
2. Using Backboard.io RAG pipeline to enrich context
3. Generating meals informed by user history
4. Parsing and displaying the results

MVP Status: Uses mock Firebase data (no real Firebase connection yet)
Future: Will connect to actual Firebase when credentials are configured
"""

from meal_plan_generator import MealPlanGenerator
from parse_meal_example import parse_meal_output, format_meal_as_json
import json


def main():
    """
    Demonstrate the complete Firebase → RAG → Gemini → Parsing pipeline.
    """
    
    print("=" * 80)
    print("FIREBASE → BACKBOARD RAG → GEMINI MEAL GENERATION PIPELINE")
    print("AI MEAL ASSISTANT - MVP DEMONSTRATION")
    print("=" * 80)
    
    # Initialize generator
    generator = MealPlanGenerator()
    
    # Example: Generate meal for USER_001 using Firebase data
    user_id = "USER_001"
    
    print(f"\n[STEP 1] RETRIEVING USER DATA FROM FIREBASE")
    print(f"User ID: {user_id}")
    print(f"Status: Using mock data (Firebase not yet connected)")
    print(f"Note: When Firebase is connected, set use_mock=False")
    
    try:
        print(f"\n[STEP 2] RETRIEVING USER PROFILE")
        # This will use mock data for now
        from firebase_service import get_mock_user_meal_data
        user_data = get_mock_user_meal_data(user_id)
        
        print(f"✓ User profile loaded successfully")
        print(f"  - Dietary Restrictions: {user_data.dietary_restrictions}")
        print(f"  - Nutrition Goals: {user_data.nutrition_goals}")
        print(f"  - Favorite Foods: {user_data.favorite_foods}")
        print(f"  - Past Meals: {len(user_data.past_meal_history)} recipes")
        print(f"  - Meal Preferences: {user_data.meal_plan_preferences}")
        
        print(f"\n[STEP 3] ENRICHING CONTEXT WITH BACKBOARD RAG PIPELINE")
        from backboard_rag_pipeline import BackboardRAGPipeline
        rag_pipeline = BackboardRAGPipeline()
        enriched_data = rag_pipeline.augment_with_rag(user_data)
        
        print(f"✓ RAG pipeline enrichment complete")
        print(f"  Analysis Summary:")
        print(f"    {enriched_data.past_meals_summary}")
        print(f"\n  Variety Requirements:")
        print(f"    {enriched_data.meal_variety_needs}")
        
        print(f"\n[STEP 4] GENERATING MEAL WITH AI MEAL ASSISTANT")
        print(f"Status: Sending RAG-enriched context to Gemini API...")
        
        # Generate meal using RAG-enriched context (User ID is the only argument)
        meal_text = generator.generate_meal(
            user_id=user_id,
            use_mock=True
        )
        
        print(f"✓ Meal generated successfully by AI Meal Assistant")
        
        print(f"\n[STEP 5] PARSING MEAL STRUCTURE")
        parsed_meal = parse_meal_output(meal_text)
        
        print(f"✓ Meal parsed successfully")
        print(f"\n  Generated Meal Details:")
        print(f"    Recipe Name: {parsed_meal['recipe_name']}")
        print(f"    Ingredients: {len(parsed_meal['ingredients'])} items")
        print(f"    Instructions: {len(parsed_meal['instructions'])} steps")
        
        # Display meal preview
        print(f"\n[STEP 6] MEAL PREVIEW")
        print(f"-" * 80)
        print(f"Recipe Name: {parsed_meal['recipe_name']}")
        print(f"\nIngredients (first 8):")
        for ingredient in parsed_meal['ingredients'][:8]:
            print(f"  • {ingredient}")
        if len(parsed_meal['ingredients']) > 8:
            print(f"  ... and {len(parsed_meal['ingredients']) - 8} more")
        
        print(f"\nInstructions (first 5 steps):")
        for i, instruction in enumerate(parsed_meal['instructions'][:5], 1):
            print(f"  {i}. {instruction[:70]}{'...' if len(instruction) > 70 else ''}")
        if len(parsed_meal['instructions']) > 5:
            print(f"  ... and {len(parsed_meal['instructions']) - 5} more steps")
        
        # Convert to JSON format
        print(f"\n[STEP 7] CONVERTING TO JSON FORMAT")
        json_output = format_meal_as_json(parsed_meal)
        
        print(f"✓ Converted to JSON successfully")
        print(f"\nJSON Output (for downstream injection):")
        print(f"-" * 80)
        print(json_output)
        
        # Save to file
        print(f"\n[STEP 8] SAVING RESULTS")
        with open('user_meal_output.json', 'w') as f:
            json.dump(parsed_meal, f, indent=2)
        
        print(f"✓ Saved to 'user_meal_output.json'")
        
        print(f"\n" + "=" * 80)
        print(f"PIPELINE EXECUTION COMPLETE")
        print(f"=" * 80)
        print(f"\nNext Steps:")
        print(f"  1. Verify the generated meal is different from past meals")
        print(f"  2. When Firebase is ready, update credentials and set use_mock=False")
        print(f"  3. Integrate the JSON output with your meal database")
        print(f"  4. Add the meal to user's past_meal_history in Firebase")
        
    except ValueError as e:
        print(f"\n✗ Input Error: {str(e)}")
    except Exception as e:
        print(f"\n✗ Error: {str(e)}")


def generate_multiple_user_meals(user_id: str, count: int = 3):
    """
    Generate multiple meals for a user respecting past meal history.
    
    Args:
        user_id: Firebase user ID
        count: Number of meals to generate
    """
    print(f"\n{'=' * 80}")
    print(f"GENERATING {count} MEALS FOR USER {user_id}")
    print(f"{'=' * 80}")
    
    generator = MealPlanGenerator()
    
    try:
        # User ID is the only argument needed
        meals = generator.generate_multiple_meals(
            user_id=user_id,
            count=count,
            use_mock=True
        )
        
        for i, meal_text in enumerate(meals, 1):
            parsed_meal = parse_meal_output(meal_text)
            
            print(f"\n[MEAL {i}]")
            print(f"  Recipe: {parsed_meal['recipe_name']}")
            print(f"  Ingredients: {len(parsed_meal['ingredients'])}")
            print(f"  Instructions: {len(parsed_meal['instructions'])} steps")
        
        print(f"\n✓ Generated {count} unique meals successfully")
        
    except Exception as e:
        print(f"✗ Error: {str(e)}")


def test_firebase_connection():
    """
    Test Firebase connection and mock data availability.
    """
    print(f"\n{'=' * 80}")
    print(f"TESTING FIREBASE DATA AVAILABILITY")
    print(f"{'=' * 80}")
    
    from firebase_service import get_mock_user_meal_data
    
    test_users = ["USER_001", "USER_002"]
    
    for user_id in test_users:
        try:
            user_data = get_mock_user_meal_data(user_id)
            print(f"\n✓ {user_id} data loaded:")
            print(f"    Restrictions: {user_data.dietary_restrictions}")
            print(f"    Goals: {user_data.nutrition_goals}")
            print(f"    Past meals: {len(user_data.past_meal_history)}")
        except ValueError as e:
            print(f"\n✗ {user_id}: {str(e)}")


if __name__ == "__main__":
    # Run the main pipeline demonstration
    main()
    
    # Optional: Generate multiple meals
    # generate_multiple_user_meals("USER_001", count=2)
    
    # Optional: Test Firebase connection
    # test_firebase_connection()
