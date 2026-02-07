"""
Main entry point for the meal plan generator.
Demonstrates how to use the MealPlanGenerator class with Firebase user data.
"""

from meal_plan_generator import MealPlanGenerator


def main():
    """
    Main function demonstrating meal plan generation using Firebase user data.
    
    This example shows how to:
    1. Initialize the meal plan generator
    2. Generate a meal using only a User ID (Firebase retrieval via RAG)
    3. Display the generated meal plan
    """
    # Initialize the generator
    generator = MealPlanGenerator()

    # Example: Generate a meal for a Firebase user
    user_id = "USER_001"

    print("=" * 60)
    print("MEAL PLAN GENERATOR - USER ID BASED")
    print("=" * 60)
    print(f"\nUser ID: {user_id}")
    print("Status: Using Firebase + RAG enrichment")
    print("Note: use_mock=True for development, use_mock=False for production")
    print("\n" + "=" * 60)
    print("Generating meal plan...\n")

    try:
        # Generate a single meal using only User ID
        # Firebase data retrieval and RAG enrichment happen automatically
        meal_plan = generator.generate_meal(
            user_id=user_id,
            use_mock=True  # Use mock data for development
        )

        print("GENERATED MEAL PLAN:")
        print("-" * 60)
        print(meal_plan)
        print("-" * 60)

        # Optional: Generate multiple meals
        print("\n" + "=" * 60)
        print("Generating multiple unique meals for this user...\n")

        meals = generator.generate_multiple_meals(
            user_id=user_id,
            count=2,
            use_mock=True
        )

        for idx, meal in enumerate(meals, 1):
            print(f"\nMEAL {idx}:")
            print("-" * 60)
            print(meal)
            print("-" * 60)

    except ValueError as e:
        print(f"Input Error: {str(e)}")
    except Exception as e:
        print(f"Error: {str(e)}")


if __name__ == "__main__":
    main()
