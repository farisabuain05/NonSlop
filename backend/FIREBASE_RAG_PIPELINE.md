# Firebase → Backboard RAG → Gemini Pipeline Documentation

## Overview

This implementation creates a complete pipeline for context-aware meal generation:

```
Firebase Database 
    ↓
Firebase Service (retrieves user data)
    ↓
Backboard RAG Pipeline (enriches context using RAG)
    ↓
Gemini API (generates informed meals)
    ↓
Parser (extracts structured data)
    ↓
JSON Output (ready for downstream injection)
```

## Architecture

### 1. Firebase Service (`firebase_service.py`)

**Current Status:** MVP with mock data
**Future:** Will connect to actual Firebase Realtime Database

#### UserMealData Structure
```python
{
    "user_id": "USER_001",
    "dietary_restrictions": "vegetarian, gluten-free, nut-free",
    "nutrition_goals": "high protein, weight loss, balanced macros",
    "favorite_foods": "Mediterranean cuisine, tofu-based dishes, quinoa",
    "past_meal_history": [
        "Mediterranean Tofu Kofta Power Bowls",
        "Aegean Spiced Tofu & Quinoa Harvest Bowl",
        ...
    ],
    "meal_plan_preferences": {
        "length": 5,      # 5 or 7 day meal plans
        "variety": "high" # low, medium, or high
    }
}
```

#### Functions
- `get_user_meal_data(user_id)` - Retrieve user data from Firebase
- `save_generated_meal(user_id, meal_data)` - Save meal to user's history
- `get_mock_user_meal_data(user_id)` - Get mock data for development

#### Usage
```python
from firebase_service import FirebaseService

# Production (requires Firebase setup)
firebase = FirebaseService(credentials_path="/path/to/credentials.json")
user_data = firebase.get_user_meal_data("USER_001")

# Development (mock data)
from firebase_service import get_mock_user_meal_data
user_data = get_mock_user_meal_data("USER_001")
```

### 2. Backboard RAG Pipeline (`backboard_rag_pipeline.py`)

**Purpose:** Enrich user context with RAG (Retrieval-Augmented Generation) analysis

#### What RAG Does
1. **Retrieval:** Fetches user data from Firebase
2. **Analysis:** Analyzes past meal patterns
   - Cuisine preferences
   - Protein patterns  
   - Repetition rates
   - Ingredient diversity
3. **Augmentation:** Enriches data with insights
   - Meal summary analysis
   - Variety needs assessment
   - Past meals list for exclusion
4. **Context Generation:** Creates detailed prompt context

#### Key Methods
```python
rag = BackboardRAGPipeline()

# Retrieve user context
user_data = rag.retrieve_user_context("USER_001", use_mock=True)

# Augment with RAG analysis
enriched = rag.augment_with_rag(user_data)

# Generate context prompt
context_prompt = rag.generate_rag_context_prompt(enriched)
```

#### RAG-Informed Context Example
```
AI Meal Assistant Context - Generate ONE different meal:
Dietary Restrictions: vegetarian, gluten-free, nut-free
Nutrition Goals: high protein, weight loss, balanced macros
Favorite Foods: Mediterranean cuisine, tofu-based dishes, quinoa, Asian fusion
Previously Suggested: Thai-Inspired Tofu Stir-Fry, Roasted Vegetable & Quinoa Buddha Bowl
Task: Create a meal different from the above. Introduce new cuisines or combinations.
```

### 3. Updated Gemini Client (`gemini_client.py`)

**New Methods:**

#### `generate_meal_plan_from_user_id(user_id, use_mock=True)`
Generates a meal using Firebase user data and RAG enrichment.

```python
from gemini_client import GeminiClient

client = GeminiClient()

# Development (mock data)
meal = client.generate_meal_plan_from_user_id("USER_001", use_mock=True)

# Production (Firebase)
meal = client.generate_meal_plan_from_user_id("USER_001", use_mock=False)
```

**Output Format:**
```
Recipe Name: Japanese Miso-Glazed Tofu with Ginger-Scallion Quinoa

Ingredients:
- Extra-firm tofu: 1 block (14 oz)
- White miso paste: 2 tablespoons
- Tamari: 2 tablespoons
- Maple syrup: 1 tablespoon
...

Instructions:
1. Press tofu for 20 minutes to remove excess water
2. Cut pressed tofu into cubes
3. In a bowl, mix miso, tamari, maple syrup, rice vinegar
...
```

### 4. Updated Meal Plan Generator (`meal_plan_generator.py`)

**New Methods:**

#### `generate_meal_for_user(user_id, use_mock=True)`
High-level interface for generating meals with Firebase integration.

```python
from meal_plan_generator import MealPlanGenerator

gen = MealPlanGenerator()

# Generate single meal
meal = gen.generate_meal_for_user("USER_001", use_mock=True)

# Generate multiple meals
meals = gen.generate_multiple_meals_for_user("USER_001", count=5, use_mock=True)
```

## Complete Pipeline Example

See `firebase_rag_example.py` for a full working example:

```bash
python3 firebase_rag_example.py
```

### Step-by-Step Flow
1. **Retrieve** - Get user data from Firebase (or mock)
2. **Enrich** - RAG pipeline analyzes past meals and preferences
3. **Generate** - Gemini API creates meal with full context
4. **Parse** - Extract recipe name, ingredients, instructions
5. **Format** - Convert to JSON for downstream processing

## Firebase Setup Instructions

### When Ready to Connect Real Firebase

1. **Create Firebase Project:**
   - Go to https://firebase.google.com/
   - Create new project
   - Set up Realtime Database

2. **Get Credentials:**
   - Go to Project Settings
   - Service Accounts
   - Generate new private key (JSON)
   - Save as `firebase-credentials.json`

3. **Install SDK:**
   ```bash
   pip install firebase-admin
   ```

4. **Update Code:**
   ```python
   from firebase_service import FirebaseService
   
   firebase = FirebaseService(
       credentials_path="/path/to/firebase-credentials.json"
   )
   user_data = firebase.get_user_meal_data("USER_001")
   ```

5. **Switch from Mock to Real Data:**
   ```python
   # Change this:
   meal = generator.generate_meal_for_user("USER_001", use_mock=True)
   
   # To this:
   meal = generator.generate_meal_for_user("USER_001", use_mock=False)
   ```

### Firebase Database Structure (Recommended)

```
{
  "users": {
    "USER_001": {
      "dietary_restrictions": "vegetarian, gluten-free",
      "nutrition_goals": "high protein, weight loss",
      "favorite_foods": "Mediterranean, tofu, quinoa",
      "meal_plan_preferences": {
        "length": 5,
        "variety": "high"
      },
      "past_meal_history": [
        {
          "recipe_name": "Mediterranean Tofu Kofta",
          "generated_at": "2025-02-07T10:30:00",
          "ingredients_count": 12,
          "instruction_count": 8
        }
      ]
    }
  }
}
```

## API Quotas & Rate Limiting

### Gemini Free Tier Limits
- **Requests:** 20 requests per day per model
- **RPM (Requests Per Minute):** Variable by model
- **TPM (Tokens Per Minute):** Limited

### Handling Rate Limits
When you hit quota limits:
1. Wait for the retry delay indicated in the error message
2. Consider upgrading to paid API for higher limits
3. Implement request queuing for batch generation

## Configuration

Edit `config.py` to customize:

```python
# API Model
GEMINI_MODEL = "gemini-2.5-flash"  # Or gemini-2.5-pro for quality

# Generation Settings
MEAL_PLAN_TEMPERATURE = 0.9  # Higher = more creative
MEAL_PLAN_MAX_TOKENS = 4096  # Ensure enough space for full meal

# RAG Pipeline Settings
# (Can add more detailed RAG config here)
```

## Parsing Output

The generated meal is structured for easy parsing:

```python
from parse_meal_example import parse_meal_output, format_meal_as_json

meal_text = generator.generate_meal_for_user("USER_001")
parsed = parse_meal_output(meal_text)

# Access data
recipe_name = parsed["recipe_name"]
ingredients = parsed["ingredients"]  # List of strings
instructions = parsed["instructions"]  # List of strings

# Convert to JSON
json_output = format_meal_as_json(parsed)
```

## Mock Data Available

### USER_001
- **Dietary:** vegetarian, gluten-free, nut-free
- **Goals:** high protein, weight loss, balanced macros
- **Favorites:** Mediterranean, tofu, quinoa, Asian fusion
- **Past Meals:** 5 recipes
- **Preferences:** 5-day plans, high variety

### USER_002
- **Dietary:** vegan, gluten-free, soy-free
- **Goals:** low carb, high fiber, muscle building
- **Favorites:** Indian, legumes, cruciferous veg, nuts
- **Past Meals:** 3 recipes
- **Preferences:** 7-day plans, medium variety

## Testing

```bash
# Test the complete pipeline
python3 firebase_rag_example.py

# Test meal parsing
python3 parse_meal_example.py

# Test basic generation (no Firebase)
python3 main.py
```

## Common Issues

### "Firebase not initialized"
- Install firebase-admin: `pip install firebase-admin`
- Provide valid credentials path
- Check Firebase project URL is correct

### "User not found"
- Verify user_id exists in Firebase
- Check Firebase security rules allow read access
- Try with mock user (USER_001 or USER_002)

### "API quota exceeded"
- Free tier limit of 20 requests/day
- Wait for reset or upgrade to paid plan
- Implement batch processing for efficiency

### Instructions not parsing
- Increase MEAL_PLAN_MAX_TOKENS in config.py
- Simplify RAG prompt if still issues
- Check output contains "Instructions:" header

## Future Enhancements

1. **MCP Server Integration** - Connect Backboard.io MCP protocols
2. **Caching** - Cache previous meals to avoid API calls
3. **Batch Generation** - Queue multiple meal requests
4. **Meal Scheduling** - Generate 7-day meal plans
5. **Cost Estimation** - Add ingredient cost tracking
6. **Nutritional Tracking** - Full nutritional analysis
7. **Difficulty Ratings** - Assess recipe difficulty
8. **Allergies** - Enhanced allergy detection

## Architecture Diagram

```
┌─────────────────────────────────────┐
│     Firebase Realtime DB            │
│  (User Profiles, Meal History)      │
└────────────┬────────────────────────┘
             │
             ▼
┌─────────────────────────────────────┐
│   Firebase Service (firebase_service.py)
│  - Retrieve user data               │
│  - Save generated meals             │
└────────────┬────────────────────────┘
             │
             ▼
┌─────────────────────────────────────┐
│ Backboard RAG Pipeline              │
│ (backboard_rag_pipeline.py)         │
│  - Analyze past meals               │
│  - Assess variety needs             │
│  - Enrich context                   │
└────────────┬────────────────────────┘
             │
             ▼
┌─────────────────────────────────────┐
│     Gemini API (gemini_client.py)   │
│  - Receives RAG-enriched context    │
│  - Generates unique meals           │
│  - Returns structured output        │
└────────────┬────────────────────────┘
             │
             ▼
┌─────────────────────────────────────┐
│  Parser (parse_meal_example.py)     │
│  - Extract recipe, ingredients      │
│  - Extract instructions             │
│  - Validate structure               │
└────────────┬────────────────────────┘
             │
             ▼
┌─────────────────────────────────────┐
│    JSON Output                      │
│  (Ready for downstream injection)   │
└─────────────────────────────────────┘
```
