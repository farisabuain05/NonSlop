"""
Firebase database service for retrieving user meal plan data.
Handles connection to Firebase and data retrieval for meal generation.
"""

from dataclasses import dataclass
from typing import Optional, List
from datetime import datetime


@dataclass
class UserMealData:
    """Data structure for user meal information from Firebase."""
    user_id: str
    dietary_restrictions: str
    nutrition_goals: str
    favorite_foods: str
    past_meal_history: List[str]
    meal_plan_preferences: dict  # Contains 'length' and 'variety' keys


class FirebaseService:
    """
    Service for retrieving user data from Firebase Realtime Database.
    
    Note: This is a template service. Actual Firebase integration requires:
    - firebase-admin SDK installation
    - Firebase service account credentials
    - Firebase project setup
    """

    def __init__(self, credentials_path: Optional[str] = None):
        """
        Initialize Firebase service.
        
        Args:
            credentials_path: Path to Firebase service account JSON credentials.
                            Will use FIREBASE_CREDENTIALS_PATH env var if not provided.
        """
        self.credentials_path = credentials_path
        self.db = None
        self._initialize_firebase()

    def _initialize_firebase(self):
        """
        Initialize Firebase Admin SDK.
        
        In production, this will:
        1. Read service account credentials
        2. Initialize Firebase Admin App
        3. Get reference to Realtime Database
        """
        try:
            import firebase_admin
            from firebase_admin import credentials, db
            
            # Load credentials
            cred = credentials.Certificate(self.credentials_path)
            
            # Initialize Firebase (check if already initialized)
            try:
                firebase_admin.get_app()
            except ValueError:
                firebase_admin.initialize_app(
                    cred,
                    {"databaseURL": "https://your-project.firebaseio.com"}
                )
            
            self.db = db
            
        except ImportError:
            print("Warning: firebase-admin not installed. Install with: pip install firebase-admin")
            self.db = None
        except Exception as e:
            print(f"Warning: Could not initialize Firebase: {str(e)}")
            self.db = None

    def get_user_meal_data(self, user_id: str) -> UserMealData:
        """
        Retrieve user meal data from Firebase.
        
        Args:
            user_id: The Firebase user ID
            
        Returns:
            UserMealData: Structured user meal information
            
        Raises:
            ValueError: If user not found
            Exception: If Firebase connection fails
        """
        if not self.db:
            raise Exception("Firebase not initialized. Check credentials and installation.")
        
        try:
            # Fetch user data from Firebase path: /users/{user_id}
            user_ref = self.db.reference(f"users/{user_id}")
            user_data = user_ref.get().val()
            
            if not user_data:
                raise ValueError(f"User {user_id} not found in Firebase")
            
            # Parse and structure the data
            return UserMealData(
                user_id=user_id,
                dietary_restrictions=user_data.get("dietary_restrictions", ""),
                nutrition_goals=user_data.get("nutrition_goals", ""),
                favorite_foods=user_data.get("favorite_foods", ""),
                past_meal_history=user_data.get("past_meal_history", []),
                meal_plan_preferences=user_data.get("meal_plan_preferences", {
                    "length": 7,
                    "variety": "high"
                })
            )
            
        except Exception as e:
            raise Exception(f"Error retrieving user data from Firebase: {str(e)}") from e

    def save_generated_meal(self, user_id: str, meal_data: dict) -> bool:
        """
        Save generated meal to user's past meal history in Firebase.
        
        Args:
            user_id: The Firebase user ID
            meal_data: Generated meal data to save
            
        Returns:
            bool: True if successful, False otherwise
        """
        if not self.db:
            raise Exception("Firebase not initialized")
        
        try:
            meal_entry = {
                "recipe_name": meal_data.get("recipe_name"),
                "generated_at": datetime.now().isoformat(),
                "ingredients_count": len(meal_data.get("ingredients", [])),
                "instruction_count": len(meal_data.get("instructions", []))
            }
            
            # Append to past meal history
            user_ref = self.db.reference(f"users/{user_id}/past_meal_history")
            history = user_ref.get().val() or []
            history.append(meal_entry)
            user_ref.set(history)
            
            return True
            
        except Exception as e:
            print(f"Error saving meal to Firebase: {str(e)}")
            return False


# Example usage with mock data (for development without Firebase)
def get_mock_user_meal_data(user_id: str) -> UserMealData:
    """
    Get mock user data for development/testing without Firebase.
    This will be used in the pipeline until Firebase is fully set up.
    
    Args:
        user_id: The user ID (used for demonstration)
        
    Returns:
        UserMealData: Mock user meal information
    """
    if user_id == "USER_001":
        return UserMealData(
            user_id="USER_001",
            dietary_restrictions="vegetarian, gluten-free, nut-free",
            nutrition_goals="high protein, weight loss, balanced macros",
            favorite_foods="Mediterranean cuisine, tofu-based dishes, quinoa, Asian fusion",
            past_meal_history=[
                "Mediterranean Tofu Kofta Power Bowls with Lemon-Herb Quinoa",
                "Aegean Spiced Tofu & Quinoa Harvest Bowl",
                "Lemon-Herb Crusted Tofu with Mediterranean Quinoa Pilaf",
                "Roasted Vegetable & Quinoa Buddha Bowl with Tahini Dressing",
                "Thai-Inspired Tofu Stir-Fry with Brown Rice"
            ],
            meal_plan_preferences={
                "length": 5,
                "variety": "high"
            }
        )
    elif user_id == "USER_002":
        return UserMealData(
            user_id="USER_002",
            dietary_restrictions="vegan, gluten-free, soy-free",
            nutrition_goals="low carb, high fiber, muscle building",
            favorite_foods="Indian cuisine, legumes, cruciferous vegetables, nuts",
            past_meal_history=[
                "Chickpea Tikka Masala with Cauliflower Rice",
                "Spiced Lentil & Vegetable Curry",
                "Roasted Chickpea & Kale Salad with Tahini Vinaigrette"
            ],
            meal_plan_preferences={
                "length": 7,
                "variety": "medium"
            }
        )
    else:
        raise ValueError(f"Mock user {user_id} not found. Use USER_001 or USER_002")
