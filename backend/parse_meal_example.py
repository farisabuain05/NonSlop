"""
Example script showing how to parse the structured meal output.
This demonstrates how to extract and work with the meal data for JSON injection.
"""

from meal_plan_generator import MealPlanGenerator


def parse_meal_output(meal_text: str) -> dict:
    """
    Parse the structured meal output into a dictionary.
    Handles cases where instructions may span multiple lines.
    
    Args:
        meal_text: The raw meal text from the generator
        
    Returns:
        dict: Structured meal data with recipe_name, ingredients, and instructions
    """
    meal_data = {
        "recipe_name": "",
        "ingredients": [],
        "instructions": []
    }
    
    lines = meal_text.strip().split('\n')
    current_section = None
    current_instruction = ""
    
    for line in lines:
        line_stripped = line.strip()
        
        # Detect section headers
        if line_stripped.startswith("Recipe Name:"):
            meal_data["recipe_name"] = line_stripped.replace("Recipe Name:", "").strip()
            current_section = None
        elif line_stripped.startswith("Ingredients:"):
            current_section = "ingredients"
        elif line_stripped.startswith("Instructions:"):
            # Save any pending instruction
            if current_instruction:
                meal_data["instructions"].append(current_instruction)
                current_instruction = ""
            current_section = "instructions"
        elif line_stripped and current_section:
            # Process ingredients
            if current_section == "ingredients":
                if line_stripped.startswith("-"):
                    ingredient = line_stripped.lstrip("-").strip()
                    # Remove markdown formatting
                    ingredient = ingredient.replace("**", "").replace("*", "")
                    if ingredient:
                        meal_data["ingredients"].append(ingredient)
            
            # Process instructions
            elif current_section == "instructions":
                # Check if line starts with a number (new instruction)
                import re
                if re.match(r'^\d+[\.\)]\s', line_stripped):
                    # Save previous instruction if exists
                    if current_instruction:
                        meal_data["instructions"].append(current_instruction)
                    # Start new instruction
                    current_instruction = re.sub(r'^\d+[\.\)]\s*', '', line_stripped)
                elif current_instruction and line_stripped:
                    # Continuation of previous instruction
                    current_instruction += " " + line_stripped
    
    # Save any remaining instruction
    if current_instruction:
        meal_data["instructions"].append(current_instruction)
    
    return meal_data


def format_meal_as_json(meal_data: dict) -> str:
    """
    Format parsed meal data as JSON-ready string.
    
    Args:
        meal_data: Dictionary with recipe_name, ingredients, instructions
        
    Returns:
        str: JSON representation of the meal
    """
    import json
    return json.dumps(meal_data, indent=2)


def main():
    """Demonstrate parsing and formatting meal data."""
    
    # Generate a meal
    generator = MealPlanGenerator()
    
    print("=" * 70)
    print("MEAL PARSING DEMONSTRATION")
    print("=" * 70)
    
    # Generate a single meal
    print("\nGenerating meal...")
    meal_text = generator.generate_meal(
        dietary_restrictions="vegetarian, gluten-free",
        nutrition_goals="high protein, weight loss",
        favorite_foods="Mediterranean cuisine, tofu-based dishes, quinoa"
    )
    
    print("\n" + "=" * 70)
    print("RAW OUTPUT FROM GEMINI API:")
    print("=" * 70)
    print(meal_text[:500] + "..." if len(meal_text) > 500 else meal_text)
    
    # Parse the meal
    print("\n" + "=" * 70)
    print("PARSED MEAL DATA:")
    print("=" * 70)
    parsed_meal = parse_meal_output(meal_text)
    
    print(f"\nRecipe Name: {parsed_meal['recipe_name']}")
    print(f"\nNumber of Ingredients: {len(parsed_meal['ingredients'])}")
    print("First 5 Ingredients:")
    for ingredient in parsed_meal['ingredients'][:5]:
        print(f"  • {ingredient}")
    if len(parsed_meal['ingredients']) > 5:
        print(f"  ... and {len(parsed_meal['ingredients']) - 5} more")
    
    print(f"\nNumber of Instructions: {len(parsed_meal['instructions'])}")
    print("First 3 Instructions:")
    for i, instruction in enumerate(parsed_meal['instructions'][:3], 1):
        print(f"  {i}. {instruction}")
    if len(parsed_meal['instructions']) > 3:
        print(f"  ... and {len(parsed_meal['instructions']) - 3} more")
    
    # Show JSON format
    print("\n" + "=" * 70)
    print("JSON FORMAT (Ready for Injection):")
    print("=" * 70)
    json_output = format_meal_as_json(parsed_meal)
    print(json_output)
    
    # Save to file example
    print("\n" + "=" * 70)
    print("SAVING TO JSON FILE:")
    print("=" * 70)
    import json
    with open('generated_meal.json', 'w') as f:
        json.dump(parsed_meal, f, indent=2)
    print("✓ Saved to 'generated_meal.json'")


if __name__ == "__main__":
    main()
