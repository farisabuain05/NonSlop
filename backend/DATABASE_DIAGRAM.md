# Database Architecture Diagram

## System Architecture Overview

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                           NONSLOP MEAL PLANNING SYSTEM                       │
└─────────────────────────────────────────────────────────────────────────────┘

                                CLIENT/FRONTEND
                                      │
                                      ▼
                        ┌──────────────────────────────┐
                        │   Non-Slop Web/Mobile App    │
                        │   (User ID: USER_001, etc)   │
                        └──────────────────────────────┘
                                      │
                    ┌─────────────────┴─────────────────┐
                    │                                   │
                    ▼                                   ▼
        ┌─────────────────────────┐        ┌──────────────────────┐
        │   BACKEND (Python)      │        │   FRONTEND (React)   │
        │ ┌─────────────────────┐ │        └──────────────────────┘
        │ │ meal_plan_generator │ │
        │ │   gemini_client     │ │
        │ │ firebase_service    │ │
        │ │ backboard_rag       │ │
        │ └─────────────────────┘ │
        └─────────────────────────┘
                    │
        ┌───────────┼───────────┐
        │           │           │
        ▼           ▼           ▼
    ┌────────┐ ┌────────┐ ┌──────────┐
    │Firebase│ │ Gemini │ │Backboard │
    │  DB    │ │  API   │ │   (RAG)  │
    └────────┘ └────────┘ └──────────┘


```

---

## Firebase Realtime Database Structure

```
┌───────────────────────────────────────────────────────────────────────────┐
│                    FIREBASE REALTIME DATABASE                             │
│                                                                           │
│  {                                                                        │
│    "users": {                                                            │
│      "USER_001": {                              ◄─── Individual User     │
│        "profile": {                                                       │
│          "first_name": "John",                                           │
│          "email": "john@example.com",                                    │
│          "created_at": "2026-02-07T10:00:00Z"                          │
│        },                                                                │
│                                                                           │
│        "dietary_restrictions": "vegetarian, gluten-free",   ◄─── RAG Input
│        "nutrition_goals": "high protein, weight loss",      ◄─── RAG Input
│        "favorite_foods": "Mediterranean, tofu, quinoa",     ◄─── RAG Input
│                                                                           │
│        "meal_plan_preferences": {                            ◄─── User Prefs
│          "length": 5,                                                    │
│          "variety": "high",                                              │
│          "cuisine_preferences": ["Mediterranean", "Thai"],               │
│          "max_prep_time_minutes": 45,                                    │
│          "budget_level": "moderate"                                      │
│        },                                                                │
│                                                                           │
│        "past_meal_history": [              ◄─── CRITICAL FOR RAG & VARIETY│
│          {                                                                │
│            "meal_id": "MEAL_001",                                        │
│            "recipe_name": "Mediterranean Tofu Kofta...",    ◄─── Avoid Repeat
│            "generated_at": "2026-02-06T14:22:00Z",                     │
│            "rating": 4.5,                                               │
│            "cuisine": "Mediterranean",                       ◄─── Track Cuisines
│            "prep_time": 35,                                             │
│            "ingredients_count": 22,                                     │
│            "instruction_count": 8                                       │
│          },                                                              │
│          {                                                               │
│            "meal_id": "MEAL_002",                                       │
│            "recipe_name": "Aegean Spiced Tofu Harvest...",             │
│            "generated_at": "2026-02-05T10:15:00Z",                    │
│            "rating": 4.0,                                              │
│            "cuisine": "Mediterranean",                                  │
│            ...                                                           │
│          }                                                               │
│        ]                                                                 │
│      },                                                                  │
│                                                                           │
│      "USER_002": {                          ◄─── Another User            │
│        "profile": { ... },                                              │
│        "dietary_restrictions": "vegan, gluten-free",                    │
│        ...                                                               │
│      }                                                                   │
│    },                                                                    │
│                                                                           │
│    "meals": {                      ◄─── Optional: Meal Repository        │
│      "MEAL_001": {                                                       │
│        "recipe_name": "Mediterranean Tofu Kofta...",                    │
│        "cuisine": "Mediterranean",                                       │
│        "ingredients": [ ... ],                                          │
│        "instructions": [ ... ],                                         │
│        ...                                                               │
│      }                                                                   │
│    }                                                                     │
│  }                                                                       │
│                                                                           │
└───────────────────────────────────────────────────────────────────────────┘
```

---

## Data Flow: User → RAG → Gemini → Meal

```
STEP 1: USER REQUEST
┌─────────────────┐
│  User ID: "001" │
└────────┬────────┘
         │
         ▼
┌────────────────────────────────────┐
│ Firebase Service                   │
│ Retrieves: /users/USER_001         │
└────────────┬───────────────────────┘
             │
             ▼
┌──────────────────────────────────────────────────────┐
│ RETRIEVED USER DATA (JSON)                           │
│                                                      │
│ {                                                    │
│   "dietary_restrictions": "vegetarian, gluten-free" │
│   "nutrition_goals": "high protein, weight loss"    │
│   "favorite_foods": "Mediterranean, tofu, quinoa"   │
│   "past_meal_history": [MEAL_001, MEAL_002, ...]    │
│   "meal_plan_preferences": {...}                    │
│ }                                                    │
└────────────┬───────────────────────────────────────┘
             │
STEP 2: RAG ENRICHMENT
             ▼
┌───────────────────────────────────────────────────────┐
│ Backboard RAG Pipeline                                │
│                                                       │
│ ├─ Analyze Past Meals                               │
│ │  • Mediterranean: 3 meals                          │
│ │  • Thai: 1 meal                                    │
│ │  • Tofu: preferred protein                         │
│ │                                                     │
│ ├─ Assess Variety Needs                             │
│ │  • High variety preference                         │
│ │  • Good diversity already                          │
│ │  • Suggest: New cuisines or combinations           │
│ │                                                     │
│ └─ Generate RAG Context                             │
│    "AI Meal Assistant Context                       │
│     Dietary: vegetarian, gluten-free                │
│     Goals: high protein, weight loss                │
│     Likes: Mediterranean, tofu, quinoa              │
│     Avoid: MEAL_001, MEAL_002, MEAL_003, ...        │
│     Make it NEW and EXCITING"                       │
│                                                       │
└────────────┬───────────────────────────────────────┘
             │
STEP 3: GEMINI API CALL
             ▼
┌───────────────────────────────────────────────────────┐
│ Gemini 2.5 Flash API                                 │
│                                                       │
│ INPUT PROMPT:                                        │
│ ┌─────────────────────────────────────────────────┐ │
│ │ AI Meal Assistant Context                       │ │
│ │ Dietary: vegetarian, gluten-free                │ │
│ │ Goals: high protein, weight loss                │ │
│ │ Likes: Mediterranean, tofu, quinoa              │ │
│ │ Avoid: [5 previous meals]                       │ │
│ │ Make it NEW and EXCITING                        │ │
│ │                                                 │ │
│ │ RETURN THIS FORMAT:                             │ │
│ │ Recipe Name: [...]                              │ │
│ │ Ingredients: [...]                              │ │
│ │ Instructions: [...]                             │ │
│ └─────────────────────────────────────────────────┘ │
└────────────┬───────────────────────────────────────┘
             │
STEP 4: MEAL GENERATION
             ▼
┌─────────────────────────────────────────────────────┐
│ GENERATED MEAL OUTPUT                               │
│                                                     │
│ Recipe Name:                                        │
│ Japanese Miso-Glazed Tofu Steaks with...           │
│                                                     │
│ Ingredients:                                        │
│ - Extra-firm tofu: 1 block (14-16 oz)              │
│ - White miso paste: 2 tablespoons                  │
│ - Tamari: 1 tablespoon                             │
│ ... (20+ more ingredients)                         │
│                                                     │
│ Instructions:                                       │
│ 1. Press tofu for 30 minutes...                    │
│ 2. Whisk together miso, tamari...                  │
│ ... (8+ more steps)                                │
│                                                     │
└────────────┬────────────────────────────────────────┘
             │
STEP 5: PARSING & STORAGE
             ▼
┌──────────────────────────────────────────────────┐
│ Parse Meal → JSON                                │
│                                                  │
│ {                                                │
│   "recipe_name": "Japanese Miso-Glazed Tofu...",│
│   "ingredients": [                               │
│     "Extra-firm tofu: 1 block (14-16 oz)",      │
│     "White miso paste: 2 tablespoons",          │
│     ...                                          │
│   ],                                             │
│   "instructions": [                              │
│     "Press tofu for 30 minutes...",             │
│     "Whisk together miso, tamari...",           │
│     ...                                          │
│   ]                                              │
│ }                                                │
└────────────┬────────────────────────────────────┘
             │
STEP 6: SAVE TO FIREBASE (Optional)
             ▼
┌──────────────────────────────────────────────────┐
│ Update Firebase                                  │
│ /users/USER_001/past_meal_history                │
│                                                  │
│ Add new entry:                                   │
│ {                                                │
│   "meal_id": "MEAL_006",                        │
│   "recipe_name": "Japanese Miso-Glazed Tofu...",│
│   "generated_at": "2026-02-07T15:30:00Z",      │
│   "cuisine": "Japanese",                        │
│   ...                                            │
│ }                                                │
│                                                  │
│ Next meal will AVOID this meal!                 │
└──────────────────────────────────────────────────┘
```

---

## RAG Context Enrichment Process

```
┌─────────────────────────────────────────────────────────────────────┐
│                   RAG ENRICHMENT PIPELINE                           │
└─────────────────────────────────────────────────────────────────────┘

INPUT: Raw Firebase User Data
│
│  dietary_restrictions: "vegetarian, gluten-free, nut-free"
│  nutrition_goals: "high protein, weight loss, balanced macros"
│  favorite_foods: "Mediterranean, tofu, quinoa, Asian fusion"
│  past_meal_history: [MEAL_001, MEAL_002, MEAL_003, MEAL_004, MEAL_005]
│  meal_plan_preferences: {"length": 5, "variety": "high"}
│
▼

ANALYSIS STEP 1: Parse Past Meals
│
├─ Recipe 1: "Mediterranean Tofu Kofta..." → Mediterranean cuisine, Tofu
├─ Recipe 2: "Aegean Spiced Tofu..." → Mediterranean cuisine, Tofu
├─ Recipe 3: "Lemon-Herb Crusted Tofu..." → Mediterranean cuisine, Tofu
├─ Recipe 4: "Thai-Inspired Tofu Stir-Fry..." → Thai cuisine, Tofu
├─ Recipe 5: "Roasted Vegetable Buddha Bowl..." → Mediterranean cuisine, Tofu
│
└─ SUMMARY: User loves Mediterranean (4/5) and Thai (1/5), always uses Tofu
│
▼

ANALYSIS STEP 2: Detect Patterns
│
├─ Cuisine Distribution:
│  └─ Mediterranean: 80% (4 meals)
│  └─ Thai: 20% (1 meal)
│
├─ Protein Pattern:
│  └─ Tofu: 100% (5/5 meals)
│  └─ Other proteins: 0%
│
├─ Variety Assessment:
│  └─ Unique meals: 5 (no exact repetition)
│  └─ Variety preference: HIGH
│  └─ Repetition rate: 0%
│  └─ Conclusion: Good diversity, encourage NEW cuisines
│
└─ Meal Frequency: ~1 meal every 2 days
│
▼

ANALYSIS STEP 3: Identify Gaps
│
├─ Over-represented:
│  └─ Mediterranean (user has had it 4 times recently)
│  └─ Tofu (always used)
│
├─ Under-represented:
│  └─ Asian cuisine (only Thai)
│  └─ Indian cuisine (never had)
│  └─ Mexican cuisine (never had)
│  └─ Other proteins (chickpea, lentil, seitan)
│
└─ Opportunity: Suggest Asian/Indian fusion with alternative proteins
│
▼

OUTPUT: RAG Context Prompt
│
│ "AI Meal Assistant Context - Generate ONE different meal:
│  Dietary Restrictions: vegetarian, gluten-free, nut-free
│  Nutrition Goals: high protein, weight loss, balanced macros
│  Favorite Foods: Mediterranean, tofu, quinoa, Asian fusion
│  Previously Suggested: Mediterranean Tofu Kofta..., Aegean Spiced Tofu...
│  Task: Create a meal different from the above. Introduce new cuisines..."
│
└─ Ready to send to Gemini API with full context!
```

---

## Database Relationships

```
                    ┌─────────────────────┐
                    │      USERS          │
                    │  (Firebase Path)    │
                    └──────────┬──────────┘
                               │
                    ┌──────────┴──────────┐
                    │                     │
                    ▼                     ▼
         ┌──────────────────┐  ┌──────────────────┐
         │   Profile Data   │  │  Preferences     │
         │  (name, email)   │  │  (length, variety)
         └──────────────────┘  └──────────────────┘
                    │                     │
         ┌──────────┴──────────┬──────────┴───────────┐
         │                     │                      │
         ▼                     ▼                      ▼
    ┌─────────────┐  ┌──────────────────┐  ┌─────────────────┐
    │  Dietary    │  │  Nutrition       │  │  Favorite       │
    │ Restrictions│  │  Goals           │  │  Foods          │
    └────┬────────┘  └────────┬─────────┘  └────────┬────────┘
         │                    │                     │
         └────────┬───────────┴──────────┬──────────┘
                  │                      │
                  ▼                      ▼
         ┌────────────────────┐  ┌────────────────┐
         │  Past Meal History │  │  Future Meals  │
         │  (Array of meals)  │  │   (To Avoid)   │
         └────────┬───────────┘  └────────────────┘
                  │
    ┌─────────────┴──────────────┐
    │                            │
    ▼                            ▼
┌──────────────────┐  ┌─────────────────────┐
│  MEAL_001        │  │  MEAL_002           │
│  (Metadata)      │  │  (Metadata)         │
│  • recipe_name   │  │  • recipe_name      │
│  • cuisine       │  │  • cuisine          │
│  • rating        │  │  • rating           │
│  • prep_time     │  │  • prep_time        │
└──────────────────┘  └─────────────────────┘
```

---

## Key Points

1. **User ID as Primary Key**: All user data is organized under unique user IDs
2. **Past Meal History is Critical**: Used by RAG to ensure variety and avoid repetition
3. **Preferences Drive Generation**: meal_plan_preferences inform how meals are selected
4. **Denormalization Strategy**: User data includes meal summaries for quick RAG analysis
5. **Scalable Structure**: Easy to add more users, meals, and preferences

---

## Quick Reference: What the RAG System Uses

```
From Firebase User Data:
├─ dietary_restrictions    → Filter inappropriate meals
├─ nutrition_goals         → Align meal suggestions
├─ favorite_foods          → Identify user preferences
├─ past_meal_history       → CRITICAL! Avoid meal repetition
│                             Track cuisine patterns
│                             Identify under-explored cuisines
├─ meal_plan_preferences   → Guide generation scope
│  ├─ length              → How many days to plan for
│  ├─ variety             → How much novelty to introduce
│  └─ cuisine_preferences → Focus areas
│
→ GENERATES UNIQUE, CONTEXTUALLY AWARE MEALS
```
