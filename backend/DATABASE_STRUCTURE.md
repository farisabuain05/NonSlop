# Firebase Realtime Database Structure

## Overview

This document outlines the expected Firebase Realtime Database structure for the NonSlop meal planning application. It includes the schema, relationships, data types, and example data.

---

## High-Level Architecture

```
Firebase Realtime Database
│
├── users/                          [Collection of all users]
│   ├── USER_001/                   [Individual user document]
│   │   ├── profile/
│   │   ├── dietary_restrictions
│   │   ├── nutrition_goals
│   │   ├── favorite_foods
│   │   ├── meal_plan_preferences
│   │   └── past_meal_history/
│   │
│   ├── USER_002/
│   │   └── [same structure]
│   │
│   └── USER_003/
│       └── [same structure]
│
└── meals/                          [Generated meals repository]
    ├── MEAL_001/
    ├── MEAL_002/
    └── MEAL_003/
```

---

## Detailed Database Schema

### 1. Users Collection: `/users/{user_id}`

```json
{
  "USER_001": {
    "profile": {
      "first_name": "John",
      "last_name": "Doe",
      "email": "john@example.com",
      "age": 28,
      "created_at": "2025-12-01T10:30:00Z",
      "updated_at": "2026-02-07T15:45:00Z"
    },
    
    "dietary_restrictions": "vegetarian, gluten-free, nut-free",
    
    "nutrition_goals": "high protein, weight loss, balanced macros",
    
    "favorite_foods": "Mediterranean cuisine, tofu-based dishes, quinoa, Asian fusion",
    
    "meal_plan_preferences": {
      "length": 5,
      "variety": "high",
      "cuisine_preferences": [
        "Mediterranean",
        "Asian",
        "Thai",
        "Indian"
      ],
      "max_prep_time_minutes": 45,
      "dietary_priority": "strict",
      "budget_level": "moderate"
    },
    
    "past_meal_history": [
      {
        "meal_id": "MEAL_001",
        "recipe_name": "Mediterranean Tofu Kofta Power Bowls with Lemon-Herb Quinoa",
        "generated_at": "2026-02-06T14:22:00Z",
        "rating": 4.5,
        "notes": "Loved the quinoa salad!",
        "ingredients_count": 22,
        "instruction_count": 8,
        "cuisine": "Mediterranean",
        "prep_time": 35
      },
      {
        "meal_id": "MEAL_002",
        "recipe_name": "Aegean Spiced Tofu & Quinoa Harvest Bowl",
        "generated_at": "2026-02-05T10:15:00Z",
        "rating": 4.0,
        "notes": null,
        "ingredients_count": 20,
        "instruction_count": 7,
        "cuisine": "Mediterranean",
        "prep_time": 30
      },
      {
        "meal_id": "MEAL_003",
        "recipe_name": "Lemon-Herb Crusted Tofu with Mediterranean Quinoa Pilaf",
        "generated_at": "2026-02-04T19:00:00Z",
        "rating": null,
        "notes": "Haven't made this yet",
        "ingredients_count": 18,
        "instruction_count": 6,
        "cuisine": "Mediterranean",
        "prep_time": 40
      },
      {
        "meal_id": "MEAL_004",
        "recipe_name": "Thai-Inspired Tofu Stir-Fry with Brown Rice",
        "generated_at": "2026-02-01T12:30:00Z",
        "rating": 5.0,
        "notes": "Perfect! Made it twice",
        "ingredients_count": 16,
        "instruction_count": 5,
        "cuisine": "Thai",
        "prep_time": 25
      },
      {
        "meal_id": "MEAL_005",
        "recipe_name": "Roasted Vegetable & Quinoa Buddha Bowl with Tahini Dressing",
        "generated_at": "2026-01-28T08:45:00Z",
        "rating": 3.5,
        "notes": "Good but a bit bland",
        "ingredients_count": 19,
        "instruction_count": 7,
        "cuisine": "Mediterranean",
        "prep_time": 38
      }
    ]
  },
  
  "USER_002": {
    "profile": {
      "first_name": "Jane",
      "last_name": "Smith",
      "email": "jane@example.com",
      "age": 35,
      "created_at": "2025-11-15T08:00:00Z",
      "updated_at": "2026-02-07T12:00:00Z"
    },
    
    "dietary_restrictions": "vegan, gluten-free, soy-free",
    
    "nutrition_goals": "low carb, high fiber, muscle building",
    
    "favorite_foods": "Indian cuisine, legumes, cruciferous vegetables, nuts",
    
    "meal_plan_preferences": {
      "length": 7,
      "variety": "medium",
      "cuisine_preferences": [
        "Indian",
        "Mediterranean",
        "Mexican"
      ],
      "max_prep_time_minutes": 50,
      "dietary_priority": "strict",
      "budget_level": "high"
    },
    
    "past_meal_history": [
      {
        "meal_id": "MEAL_006",
        "recipe_name": "Chickpea Tikka Masala with Cauliflower Rice",
        "generated_at": "2026-02-06T18:00:00Z",
        "rating": 4.8,
        "notes": "Amazing flavor profile",
        "ingredients_count": 20,
        "instruction_count": 8,
        "cuisine": "Indian",
        "prep_time": 40
      },
      {
        "meal_id": "MEAL_007",
        "recipe_name": "Spiced Lentil & Vegetable Curry",
        "generated_at": "2026-02-03T16:30:00Z",
        "rating": 4.2,
        "notes": null,
        "ingredients_count": 18,
        "instruction_count": 7,
        "cuisine": "Indian",
        "prep_time": 45
      },
      {
        "meal_id": "MEAL_008",
        "recipe_name": "Roasted Chickpea & Kale Salad with Tahini Vinaigrette",
        "generated_at": "2026-01-30T12:15:00Z",
        "rating": 3.8,
        "notes": null,
        "ingredients_count": 15,
        "instruction_count": 5,
        "cuisine": "Mediterranean",
        "prep_time": 20
      }
    ]
  }
}
```

---

## Meals Collection: `/meals/{meal_id}`

Optional: Store generated meals separately for quick lookup and analytics.

```json
{
  "MEAL_001": {
    "recipe_name": "Mediterranean Tofu Kofta Power Bowls with Lemon-Herb Quinoa",
    
    "ingredients": [
      {
        "name": "Extra-firm tofu",
        "amount": 1,
        "unit": "block (14 oz)"
      },
      {
        "name": "Olive oil",
        "amount": 2,
        "unit": "tablespoons"
      },
      {
        "name": "Lemon juice",
        "amount": 3,
        "unit": "tablespoons"
      }
    ],
    
    "instructions": [
      "Press the extra-firm tofu for at least 30 minutes to remove excess water.",
      "Cut pressed tofu into 1-inch cubes.",
      "In a shallow dish, whisk together 1 tablespoon of olive oil, 2 tablespoons of lemon juice..."
    ],
    
    "cuisine": "Mediterranean",
    "prep_time": 35,
    "difficulty": "medium",
    "servings": 2,
    
    "dietary_tags": [
      "vegetarian",
      "gluten-free",
      "nut-free",
      "vegan"
    ],
    
    "nutrition_estimate": {
      "calories_per_serving": 420,
      "protein_grams": 18,
      "carbs_grams": 45,
      "fat_grams": 14,
      "fiber_grams": 8
    },
    
    "generated_at": "2026-02-06T14:22:00Z",
    "gemini_model": "gemini-2.5-flash"
  }
}
```

---

## Data Types & Constraints

### User ID (STRING)
- Format: `USER_001`, `USER_002`, etc.
- Required: Yes
- Unique: Yes
- Index: Yes

### Profile Fields
| Field | Type | Required | Notes |
|-------|------|----------|-------|
| first_name | String | No | User's first name |
| last_name | String | No | User's last name |
| email | String | No | User's email address |
| age | Number | No | User's age in years |
| created_at | Timestamp | Yes | Account creation timestamp |
| updated_at | Timestamp | Yes | Last profile update timestamp |

### Dietary Restrictions (STRING)
- Format: Comma-separated values
- Example: `"vegetarian, gluten-free, nut-free"`
- Required: Yes
- Can be indexed for filtering

### Nutrition Goals (STRING)
- Format: Comma-separated values
- Example: `"high protein, weight loss, balanced macros"`
- Required: Yes

### Favorite Foods (STRING)
- Format: Comma-separated values
- Example: `"Mediterranean cuisine, tofu-based dishes, quinoa"`
- Required: Yes

### Meal Plan Preferences (OBJECT)
| Field | Type | Required | Notes |
|-------|------|----------|-------|
| length | Number | Yes | Days (1-7) |
| variety | String | Yes | "low", "medium", "high" |
| cuisine_preferences | Array[String] | No | List of cuisines |
| max_prep_time_minutes | Number | No | Maximum prep time |
| dietary_priority | String | No | "strict", "flexible" |
| budget_level | String | No | "low", "moderate", "high" |

### Past Meal History (ARRAY)
Each meal entry:
| Field | Type | Required | Notes |
|-------|------|----------|-------|
| meal_id | String | Yes | Unique meal identifier |
| recipe_name | String | Yes | Name of the recipe |
| generated_at | Timestamp | Yes | When meal was generated |
| rating | Number | No | 1-5 star rating |
| notes | String | No | User's notes about the meal |
| ingredients_count | Number | Yes | Total ingredients |
| instruction_count | Number | Yes | Total steps |
| cuisine | String | No | Cuisine type |
| prep_time | Number | No | Prep time in minutes |

---

## Database Rules (Firebase Security Rules)

```json
{
  "rules": {
    "users": {
      "$uid": {
        ".read": "auth.uid == $uid",
        ".write": "auth.uid == $uid",
        ".validate": "newData.hasChildren(['dietary_restrictions', 'nutrition_goals', 'favorite_foods'])"
      }
    },
    "meals": {
      ".read": true,
      ".write": "root.child('admins').child(auth.uid).exists()"
    }
  }
}
```

---

## Indexing Strategy

Recommended indexes for optimal query performance:

```javascript
// Index 1: Users by created_at (for user analytics)
Collection: users
Fields: profile.created_at (Ascending)

// Index 2: Meal history by generated_at (for recent meals)
Collection: users/{uid}/past_meal_history
Fields: generated_at (Descending)

// Index 3: Meals by cuisine (for meal filtering)
Collection: meals
Fields: cuisine (Ascending), generated_at (Descending)
```

---

## Example Queries

### Get user's dietary restrictions
```python
user_ref = db.reference(f"users/{user_id}")
dietary = user_ref.child("dietary_restrictions").get().val()
```

### Get user's past 5 meals
```python
meals_ref = db.reference(f"users/{user_id}/past_meal_history")
all_meals = meals_ref.get().val()
recent_meals = all_meals[-5:] if all_meals else []
```

### Add a new meal to history
```python
meal_entry = {
    "meal_id": "MEAL_009",
    "recipe_name": "New Recipe",
    "generated_at": datetime.now().isoformat(),
    "rating": None,
    "notes": None,
    "ingredients_count": 15,
    "instruction_count": 6
}
history_ref = db.reference(f"users/{user_id}/past_meal_history")
history_ref.push(meal_entry)
```

---

## Data Validation

- **Dietary Restrictions**: Must be non-empty string
- **Nutrition Goals**: Must be non-empty string
- **Favorite Foods**: Must be non-empty string
- **Meal Plan Length**: 1-7 (days)
- **Variety Level**: Must be "low", "medium", or "high"
- **Rating**: 1-5 or null
- **Timestamps**: ISO 8601 format

---

## Size & Cost Estimation

For 1,000 users with 5 meals each:

| Data | Size | Cost Factor |
|------|------|------------|
| User Profile | ~500 bytes | Low |
| Meal History | ~15 KB per user | Medium |
| Meal Metadata | ~2 KB per meal | Low |
| **Total** | **~15 MB** | **Free tier+** |

Firebase free tier includes:
- 100 simultaneous connections
- 1 GB stored data
- 10 GB/month downloaded
- Perfect for MVP

---

## Migration Path

1. **Phase 1**: Use mock data (current state)
2. **Phase 2**: Create Firebase project with empty collections
3. **Phase 3**: Populate sample users (USER_001, USER_002)
4. **Phase 4**: Start collecting real user data
5. **Phase 5**: Add authentication layer

---

## Next Steps

1. Create Firebase project: https://console.firebase.google.com/
2. Enable Realtime Database
3. Create users collection with this structure
4. Add sample data (provided in mock_data.json)
5. Update config.py with database URL
6. Test with `python3 firebase_rag_example.py`

