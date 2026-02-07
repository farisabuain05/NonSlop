# Meal Plan Generator - Backend

A Python-based meal plan generator that uses Google's Gemini API to create unique, personalized meal recommendations based on dietary restrictions, nutrition goals, and favorite foods.

## Features

- **Personalized Meal Generation**: Creates unique meal recipes tailored to user preferences
- **Structured Output**: Generates meals with:
  - Recipe name
  - Complete ingredient list with amounts
  - Step-by-step cooking instructions
  - Nutritional information (calories, protein, carbs, fat, fiber)
  - Estimated cost per serving
- **Variety-Focused**: Emphasizes creativity and introduces new dishes while respecting preferences
- **Batch Generation**: Can generate multiple unique meals in one session
- **Easy Integration**: Output format ready for JSON parsing and injection

## Setup Instructions

### 1. Prerequisites
- Python 3.7+
- Gemini API key from Google AI Studio (free tier available)

### 2. Installation

1. **Clone or navigate to the project**:
   ```bash
   cd /path/to/backend
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Create a `.env` file** with your API key:
   ```bash
   cp .env.example .env
   ```

4. **Add your Gemini API key** to `.env`:
   - Get your free API key from: https://aistudio.google.com/
   - Open `.env` and replace `your_gemini_api_key_here` with your actual key

### 3. Get Your Gemini API Key

1. Go to [Google AI Studio](https://aistudio.google.com/)
2. Click "Get API Key" in the left panel
3. Create a new API key in your Google Cloud project
4. Copy the key and paste it into your `.env` file

## Usage

### Basic Usage

Run the example with default preferences:
```bash
python3 main.py
```

This generates:
- 1 unique meal based on example preferences
- 2 additional unique meals for variety

### Custom Usage

To use the library with your own preferences, create a script like:

```python
from meal_plan_generator import MealPlanGenerator

# Initialize generator
generator = MealPlanGenerator()

# Generate a single meal
meal = generator.generate_meal(
    dietary_restrictions="vegetarian, gluten-free, nut-free",
    nutrition_goals="high protein, low carb, weight loss",
    favorite_foods="Asian cuisine, pasta, Mediterranean"
)

print(meal)

# Generate multiple meals
meals = generator.generate_multiple_meals(
    dietary_restrictions="vegan, dairy-free",
    nutrition_goals="high fiber, balanced macros",
    favorite_foods="Indian cuisine, whole grains",
    count=5
)

for i, meal in enumerate(meals, 1):
    print(f"\nMeal {i}:")
    print(meal)
```

### List Available Models

To see all available Gemini models:
```bash
python3 list_models.py
```

## Project Structure

```
backend/
├── .env                          # Your API key (create this)
├── .env.example                  # Template for .env
├── requirements.txt              # Python dependencies
├── config.py                     # Configuration and API settings
├── gemini_client.py             # Low-level Gemini API client
├── meal_plan_generator.py       # High-level meal plan generator
├── main.py                       # Example usage script
├── list_models.py               # Utility to list available models
└── README.md                     # This file
```

## File Descriptions

### `config.py`
- Loads environment variables from `.env`
- Defines API model and generation parameters
- Validates API key presence

### `gemini_client.py`
- Handles direct communication with Gemini API
- Builds optimized prompts for meal generation
- Manages API configuration and response handling

### `meal_plan_generator.py`
- High-level interface for meal generation
- Validates user inputs
- Provides single and batch meal generation methods
- Returns properly formatted meal data ready for parsing

### `main.py`
- Example demonstrating library usage
- Shows how to generate single and multiple meals
- Can be modified for different preferences

## Output Format

Each generated meal follows this structured format:

```
**RECIPE NAME:** [Creative recipe name]

**INGREDIENTS:**
- [Ingredient 1]: [Amount with unit]
- [Ingredient 2]: [Amount with unit]
(... full ingredient list)

**INSTRUCTIONS:**
1. [Cooking step 1]
2. [Cooking step 2]
(... full instructions)

**NUTRITIONAL INFORMATION:**
- Calories: [number] per serving
- Protein: [number]g
- Carbohydrates: [number]g
- Fat: [number]g
- Fiber: [number]g

**ESTIMATED COST:** $[number] per serving
```

This structured format is designed for easy parsing and JSON injection by downstream processes.

## Configuration

Edit `config.py` to customize:

- **GEMINI_MODEL**: Change the AI model (default: `gemini-2.5-flash`)
- **MEAL_PLAN_TEMPERATURE**: Controls creativity (0.0 = deterministic, 1.0 = creative)
- **MEAL_PLAN_MAX_TOKENS**: Maximum response length (default: 2048)

## Error Handling

The library provides clear error messages for:
- Missing API key
- Empty user inputs
- API communication failures
- Invalid preferences

Example error handling:
```python
try:
    meal = generator.generate_meal(
        dietary_restrictions="vegetarian",
        nutrition_goals="high protein",
        favorite_foods="Mediterranean"
    )
except ValueError as e:
    print(f"Input Error: {e}")
except Exception as e:
    print(f"API Error: {e}")
```

## API Model Information

The current configuration uses **Gemini 2.5 Flash**:
- Fast and efficient
- Supports 1,048,576 token input limit
- Excellent for text generation
- Suitable for meal plan creation

Other available models:
- `gemini-2.5-pro`: More powerful, slower
- `gemini-pro-latest`: Latest stable version
- `gemini-flash-lite-latest`: Lightweight option

## Integration Notes

The output is structured for easy integration with downstream JSON parsing:

1. **Extract Key Data**: Parse recipe name, ingredients, instructions, etc.
2. **Validate Fields**: Ensure all required sections are present
3. **Inject to JSON**: Convert to your desired JSON schema
4. **Database Storage**: Ready for storage in your persistence layer

## Troubleshooting

### "ModuleNotFoundError: No module named 'google.generativeai'"
- Run: `pip install -r requirements.txt`

### "GEMINI_API_KEY not found"
- Create `.env` file with valid API key
- Don't commit `.env` to version control

### "404 model not found"
- Run `python3 list_models.py` to see available models
- Update `GEMINI_MODEL` in `config.py`

### API Rate Limiting
- Gemini API has usage limits on free tier
- Consider adding delays between requests for batch generation
- Check your API quota at https://aistudio.google.com/

## Requirements

- `google-generativeai==0.3.0`: Official Google Generative AI library
- `python-dotenv==1.0.0`: Environment variable management

## License

See LICENSE file in the repository.

## Support

For issues with:
- **Gemini API**: https://aistudio.google.com/
- **Python Library**: https://github.com/google/generative-ai-python
- **This Project**: Create an issue in the repository

## Future Enhancements

Potential features:
- Caching generated meals to avoid API calls
- Weekly meal plan scheduling
- Nutritional goal optimization
- Recipe difficulty rating
- Prep time estimation
- Ingredient cost tracking
- Dietary certification validation
