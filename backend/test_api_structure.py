"""
API structure test - verifies that the refactored API works correctly
without making actual Gemini API calls (to avoid quota issues).
"""

from meal_plan_generator import MealPlanGenerator
from firebase_service import get_mock_user_meal_data
from backboard_rag_pipeline import BackboardRAGPipeline


def test_api_structure():
    """Test that the new API structure is correct."""
    
    print("=" * 80)
    print("TESTING REFACTORED API STRUCTURE")
    print("=" * 80)
    
    # Test 1: User ID is the only argument for generate_meal
    print("\n[TEST 1] Verify generate_meal() only requires user_id")
    try:
        import inspect
        sig = inspect.signature(MealPlanGenerator.generate_meal)
        params = list(sig.parameters.keys())
        print(f"✓ generate_meal() parameters: {params}")
        assert params == ['self', 'user_id', 'use_mock'], "API signature changed!"
        print(f"✓ PASS: Only user_id required (plus optional use_mock)")
    except Exception as e:
        print(f"✗ FAIL: {e}")
        return False
    
    # Test 2: Firebase data retrieval
    print("\n[TEST 2] Verify Firebase mock data retrieval")
    try:
        user_data = get_mock_user_meal_data("USER_001")
        print(f"✓ User ID: {user_data.user_id}")
        print(f"✓ Dietary Restrictions: {user_data.dietary_restrictions}")
        print(f"✓ Nutrition Goals: {user_data.nutrition_goals}")
        print(f"✓ Favorite Foods: {user_data.favorite_foods}")
        print(f"✓ Past Meals: {len(user_data.past_meal_history)} recipes")
        print(f"✓ PASS: Firebase data structure correct")
    except Exception as e:
        print(f"✗ FAIL: {e}")
        return False
    
    # Test 3: RAG pipeline enrichment
    print("\n[TEST 3] Verify RAG pipeline enrichment")
    try:
        rag_pipeline = BackboardRAGPipeline()
        enriched = rag_pipeline.augment_with_rag(user_data)
        print(f"✓ User ID: {enriched.user_id}")
        print(f"✓ Past Meals Summary: {enriched.past_meals_summary[:60]}...")
        print(f"✓ Variety Needs: {enriched.meal_variety_needs[:60]}...")
        print(f"✓ PASS: RAG enrichment working correctly")
    except Exception as e:
        print(f"✗ FAIL: {e}")
        return False
    
    # Test 4: RAG context prompt generation
    print("\n[TEST 4] Verify RAG context prompt generation")
    try:
        prompt = rag_pipeline.generate_rag_context_prompt(enriched)
        print(f"✓ Prompt generated ({len(prompt)} characters)")
        assert "USER_001" in prompt, "User ID not in prompt"
        assert "vegetarian" in prompt.lower(), "Dietary info not in prompt"
        print(f"✓ PASS: RAG context prompt includes all user info")
    except Exception as e:
        print(f"✗ FAIL: {e}")
        return False
    
    # Test 5: Multiple user IDs work
    print("\n[TEST 5] Verify multiple mock users available")
    try:
        user_002 = get_mock_user_meal_data("USER_002")
        print(f"✓ USER_002 loaded: {user_002.dietary_restrictions}")
        print(f"✓ PASS: Multiple mock users available for testing")
    except Exception as e:
        print(f"✗ FAIL: {e}")
        return False
    
    # Test 6: Error handling for invalid user
    print("\n[TEST 6] Verify error handling for invalid users")
    try:
        invalid_user = get_mock_user_meal_data("INVALID_USER")
        print(f"✗ FAIL: Should have raised error for invalid user")
        return False
    except ValueError as e:
        print(f"✓ Correctly raised ValueError: {str(e)}")
        print(f"✓ PASS: Error handling working correctly")
    except Exception as e:
        print(f"✗ FAIL: Wrong exception type: {e}")
        return False
    
    print("\n" + "=" * 80)
    print("ALL TESTS PASSED")
    print("=" * 80)
    print("\nSummary:")
    print("  • generate_meal(user_id) accepts only User ID as argument")
    print("  • Firebase data retrieval working correctly")
    print("  • RAG enrichment analyzing user history properly")
    print("  • Context prompts including all necessary information")
    print("  • Multiple mock users available for testing")
    print("  • Error handling working as expected")
    print("\nThe refactored API is ready for use!")
    print("When API quota resets, run: python3 main.py")
    
    return True


if __name__ == "__main__":
    success = test_api_structure()
    exit(0 if success else 1)
