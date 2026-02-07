# Firebase Security Rules Setup Guide

## Quick Summary
Firebase Security Rules control who can read/write data in your database. Since you're starting in **TEST MODE**, the rules are temporarily permissive, but you should configure proper rules now for when you switch to Locked Mode.

---

## Step-by-Step: Set Your Security Rules

### Step 1: Open Firebase Console
1. Go to [Firebase Console](https://console.firebase.google.com/)
2. Select your project
3. Click on "Realtime Database" in the left sidebar
4. Click the **"Rules"** tab at the top (next to "Data")

```
Firebase Console
└── Your Project
    └── Realtime Database
        ├── Data      [View your data]
        └── Rules     [← CLICK HERE]
```

---

### Step 2: Replace the Default Rules

You should see a text editor with JSON rules. **Clear everything** and paste one of the rule sets below based on your development phase:

---

## Rule Set 1: FOR DEVELOPMENT (TEST MODE)
Use this while developing and testing. Rules are permissive but still have some structure.

```json
{
  "rules": {
    "users": {
      "$uid": {
        ".read": true,
        ".write": true,
        "dietary_restrictions": {
          ".validate": "newData.isString() && newData.val().length > 0"
        },
        "nutrition_goals": {
          ".validate": "newData.isString() && newData.val().length > 0"
        },
        "favorite_foods": {
          ".validate": "newData.isString() && newData.val().length > 0"
        },
        "past_meal_history": {
          "$index": {
            ".validate": "newData.hasChildren(['meal_id', 'recipe_name', 'generated_at'])"
          }
        }
      }
    },
    "meals": {
      ".read": true,
      ".write": true
    }
  }
}
```

**What this does:**
- ✅ Anyone can read user data (good for testing)
- ✅ Anyone can write user data (good for development)
- ✅ Validates that required fields exist
- ❌ NOT suitable for production

---

## Rule Set 2: FOR PRODUCTION (LOCKED MODE)
Use this after you set up Firebase Authentication and go to Locked Mode.

```json
{
  "rules": {
    "users": {
      "$uid": {
        ".read": "auth.uid == $uid || root.child('admins').child(auth.uid).exists()",
        ".write": "auth.uid == $uid || root.child('admins').child(auth.uid).exists()",
        
        "profile": {
          ".validate": "newData.hasChildren(['first_name', 'email'])"
        },
        "dietary_restrictions": {
          ".validate": "newData.isString() && newData.val().length > 0"
        },
        "nutrition_goals": {
          ".validate": "newData.isString() && newData.val().length > 0"
        },
        "favorite_foods": {
          ".validate": "newData.isString() && newData.val().length > 0"
        },
        "meal_plan_preferences": {
          ".validate": "newData.hasChildren(['length', 'variety'])"
        },
        "past_meal_history": {
          "$index": {
            ".validate": "newData.hasChildren(['meal_id', 'recipe_name', 'generated_at'])"
          }
        }
      }
    },
    "meals": {
      ".read": "auth != null",
      ".write": "root.child('admins').child(auth.uid).exists()"
    },
    "admins": {
      ".read": "auth != null && root.child('admins').child(auth.uid).exists()",
      ".write": "auth != null && root.child('admins').child(auth.uid).exists()"
    }
  }
}
```

**What this does:**
- 🔒 Users can only read/write their own data (`auth.uid == $uid`)
- 🔒 Admins have elevated access (can manage all users)
- ✅ Validates all required fields
- ✅ Suitable for production
- ⚠️ Requires Firebase Authentication setup

---

## Step 3: Click "Publish"

After choosing your rules:
1. Copy the rules from above
2. Paste into the Firebase Console Rules editor
3. Click the **"Publish"** button (bottom right)
4. Wait for confirmation: "Rules updated successfully"

```
Firebase Rules Editor
┌─────────────────────────────────────┐
│ Paste rules here                    │
│                                     │
│ {                                   │
│   "rules": {                        │
│     "users": { ... }                │
│   }                                 │
│ }                                   │
│                                     │
│              [Publish] ← CLICK HERE  │
└─────────────────────────────────────┘
```

---

## Understanding Firebase Security Rules

### Basic Rule Structure
```json
{
  "rules": {
    "path": {
      ".read": "condition",    // Who can READ this path?
      ".write": "condition",   // Who can WRITE this path?
      ".validate": "condition" // What format is VALID?
    }
  }
}
```

### Common Conditions

| Condition | Meaning | Example |
|-----------|---------|---------|
| `true` | Anyone | `".read": true` |
| `false` | No one | `".read": false` |
| `auth != null` | Authenticated users | `".read": "auth != null"` |
| `auth.uid == $uid` | Only the user themselves | `".read": "auth.uid == $uid"` |
| `root.child('admins').child(auth.uid).exists()` | User is an admin | `".write": "root.child('admins').child(auth.uid).exists()"` |

### Validation Rules

```json
{
  "field": {
    ".validate": "newData.isString() && newData.val().length > 0"
    // ↑ Value must be a non-empty string
  },
  
  "array_field": {
    "$index": {
      ".validate": "newData.hasChildren(['required_field_1', 'required_field_2'])"
      // ↑ Each array item must have these fields
    }
  }
}
```

---

## Step 4: Test Your Rules (Optional but Recommended)

Firebase Console has a **Rules Simulator** to test if your rules work correctly.

### Test Example: Can User Read Their Own Data?

1. In Firebase Console, go to **Rules** tab
2. Click the **"Simulator"** button (top right)
3. Enter:
   - **Operation**: `read`
   - **Path**: `users/USER_001`
   - **Auth UID**: `USER_001`
4. Click **"Run"**
5. Result should say: **"Simulator said: Allowed ✓"**

```
Rules Simulator
┌─────────────────────────────┐
│ Operation: [read ▼]         │
│ Path: users/USER_001        │
│ Auth UID: USER_001          │
│                             │
│ [Run Simulator]             │
│                             │
│ ✓ Simulator said: Allowed   │
└─────────────────────────────┘
```

---

## Current Development Status: TEST MODE

Since you're in **TEST MODE**, Firebase has default permissive rules. Your custom rules won't be fully enforced until you switch to **Locked Mode** (after 30 days or manually).

```
TEST MODE (First 30 days)
├─ Default Rules: Permissive (anyone can read/write)
├─ Your Custom Rules: Added but not enforced
├─ Good for: Development and testing
└─ Expires: 30 days from creation

↓ After 30 days ↓

LOCKED MODE (Production)
├─ Default Rules: Restrictive (auth required)
├─ Your Custom Rules: Now enforced!
├─ Good for: Production with real data
└─ Requires: Firebase Authentication
```

---

## For Now: Development Phase

**While in TEST MODE**, follow these steps:

### 1. Add Security Rules Now (Even Though Not Enforced)
```
Why? You want them ready for when you switch to Locked Mode.
This prevents having to rewrite rules later.
```

### 2. Use Rule Set 1 (Development Rules) ← START HERE
- Allows testing without authentication
- Still validates data format
- Easy transition to production rules later

### 3. Add Sample Data
Use DATABASE_STRUCTURE.md examples to populate your database with test users (USER_001, USER_002, etc.)

### 4. Before Going to Production (30 days later)
- Switch to **Locked Mode** in Firebase Console
- Change to **Rule Set 2** (Production Rules)
- Set up Firebase Authentication
- Test that users can only access their own data

---

## Security Rules for Your Specific Schema

Based on your DATABASE_STRUCTURE.md, here's what your rules validate:

### Users Data
```json
"users": {
  "$uid": {
    ".write": "auth.uid == $uid",  // Only user can edit their profile
    
    "dietary_restrictions": {
      ".validate": "newData.isString()"  // Must be text
    },
    "nutrition_goals": {
      ".validate": "newData.isString()"
    },
    "favorite_foods": {
      ".validate": "newData.isString()"
    },
    "past_meal_history": {
      "$index": {
        ".validate": "newData.hasChildren(['meal_id', 'recipe_name', 'generated_at'])"
        // Each meal must have these 3 fields
      }
    }
  }
}
```

### Meals Data (Public Reading, Admin Writing)
```json
"meals": {
  ".read": "auth != null",  // Any logged-in user can read
  ".write": "root.child('admins').child(auth.uid).exists()"
  // Only admins can add new meals
}
```

---

## Troubleshooting Rules

### Problem: "Permission Denied" Errors
**Solution**: Check if your rules match your auth setup
- Are you authenticated?
- Does your UID match the rule?
- Did you click "Publish"?

### Problem: Data Not Validating
**Solution**: Check validation rules
```json
// Make sure required fields are all there
"past_meal_history": {
  "$index": {
    ".validate": "newData.hasChildren(['meal_id', 'recipe_name', 'generated_at'])"
  }
}
```

### Problem: Rules Won't Save
**Solution**: Check for JSON syntax errors
- Use Firebase Console syntax checker
- Check for missing commas, quotes, braces
- Firebase will show you the exact line with error

---

## Next Steps

1. ✅ **Right Now**: Set Rule Set 1 (Development Rules) in Firebase Console
2. ✅ **Copy your Database URL** from Firebase Console
3. ✅ **Add to .env file**:
   ```
   FIREBASE_DATABASE_URL=https://your-project-name.firebaseio.com
   ```
4. ✅ **Update firebase_service.py** with your database URL
5. ✅ **Add sample data** using DATABASE_STRUCTURE.md examples
6. ⏳ **Later (30 days)**: Switch to Locked Mode + Rule Set 2

---

## Quick Reference

| Action | Where in Firebase Console |
|--------|-------------------------|
| View data | Realtime Database → Data tab |
| Edit rules | Realtime Database → Rules tab |
| Test rules | Realtime Database → Rules tab → Simulator button |
| Get database URL | Realtime Database → Data tab (URL at top) |
| Get credentials (later) | Project Settings → Service Accounts |

