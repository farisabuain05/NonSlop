# API Keys & Credentials Reference

## ✅ Currently Configured

### 1. **Gemini API Key** ✓
- **Status**: ✅ CONFIGURED in `.env`
- **Location**: `GEMINI_API_KEY` in `.env`
- **Service**: Google Generative AI (Gemini 2.5 Flash)
- **Obtained from**: [Google AI Studio](https://aistudio.google.com/)
- **Usage**: Meal plan generation via natural language AI
- **Current Quota**: Free tier (20 requests/day)
- **Cost**: Free tier available, paid plans start at usage-based pricing

---

## ❌ Missing / Not Yet Configured

### 1. **Firebase Service Account Credentials** ❌ MISSING
- **Status**: ⚠️ NOT CONFIGURED
- **Required for**: Reading user data from Firebase Realtime Database
- **What you need**:
  - Firebase project (create at [Google Cloud Console](https://console.firebase.google.com/))
  - Service account JSON file with credentials
  - Database URL

- **Steps to obtain**:
  1. Go to [Firebase Console](https://console.firebase.google.com/)
  2. Create a new project or select existing one
  3. Set up Realtime Database (create database)
  4. Go to Project Settings → Service Accounts
  5. Click "Generate New Private Key"
  6. Save the JSON file securely
  
- **Configuration location**: 
  - File: `firebase_service.py` line 79 (credentials_path parameter)
  - Environment variable: `FIREBASE_CREDENTIALS_PATH` (optional)
  - Database URL: Update `firebaseio.com` URL in `_initialize_firebase()`

- **How to add to project**:
  ```python
  # In config.py, add:
  FIREBASE_CREDENTIALS_PATH = os.getenv("FIREBASE_CREDENTIALS_PATH")
  FIREBASE_DATABASE_URL = os.getenv("FIREBASE_DATABASE_URL")
  
  # In .env file, add:
  FIREBASE_CREDENTIALS_PATH=/path/to/serviceAccount.json
  FIREBASE_DATABASE_URL=https://your-project.firebaseio.com
  ```

### 2. **Backboard.io API Credentials** ❌ NOT YET NEEDED
- **Status**: ⏳ FUTURE (currently using native RAG implementation)
- **When needed**: When integrating actual Backboard.io services
- **What you'll need**:
  - Backboard.io API key
  - Backboard.io project ID
  - Backboard.io workspace credentials

- **Currently**: Using native Python RAG pipeline (no external service needed yet)

---

## Summary: What's Missing

| Service | Status | Priority | Details |
|---------|--------|----------|---------|
| Gemini API | ✅ Ready | High | Already configured with API key |
| Firebase Realtime DB | ❌ Missing | **CRITICAL** | Needed to read user data |
| Firebase Service Account | ❌ Missing | **CRITICAL** | Needed to authenticate with Firebase |
| Backboard.io | ⏳ Pending | Low | Future integration for advanced RAG |

---

## Next Steps for Setup

### Immediate (Required for Production)
1. **Create Firebase Project**
   - Visit: https://console.firebase.google.com/
   - Click "Add project"
   - Enable Realtime Database
   - Set security rules (see DATABASE_STRUCTURE.md)

2. **Get Firebase Credentials**
   - Project Settings → Service Accounts
   - Generate private key (JSON format)
   - Store securely (never commit to Git)

3. **Update Configuration**
   - Add `FIREBASE_CREDENTIALS_PATH` to `.env`
   - Add `FIREBASE_DATABASE_URL` to `.env`
   - Update `firebase_service.py` with correct paths

4. **Update mock data to real data**
   - Modify `firebase_service.py` 
   - Change `use_mock=False` in production calls

### Future (Optional, Advanced)
1. **Integrate Backboard.io** (if you want professional RAG service)
2. **Add authentication** (Firebase Auth)
3. **Implement caching** (Redis or similar)

---

## Security Best Practices

### DO:
✅ Store API keys in `.env` file (not in code)  
✅ Add `.env` to `.gitignore`  
✅ Use environment variables for sensitive data  
✅ Rotate API keys regularly  
✅ Use Firebase security rules to restrict access  
✅ Use service account for backend (not browser/mobile keys)  

### DON'T:
❌ Commit `.env` file to Git  
❌ Hardcode API keys in Python files  
❌ Share credentials publicly  
❌ Use browser API keys for backend operations  
❌ Store credentials in version control  

---

## Credential Files Checklist

```
/backend/
├── .env                          [✓ CREATE - ADD YOUR KEYS HERE]
├── serviceAccount.json           [❌ MISSING - DOWNLOAD FROM FIREBASE]
├── firebase_service.py           [✓ READY - Just needs config]
├── config.py                     [✓ READY - Update with Firebase URLs]
└── .gitignore                    [✓ SHOULD INCLUDE: .env, *.json, secrets/]
```

### .gitignore entries needed:
```
.env
.env.local
*.json
!.env.example
secrets/
credentials/
```

---

## Testing Your Configuration

Once you have Firebase set up, test with:
```bash
python3 test_api_structure.py    # Verify API structure
python3 firebase_rag_example.py  # Test full pipeline
```

Change `use_mock=False` to use real Firebase instead of mock data.

---

## Support Resources

- **Gemini API**: https://ai.google.dev/
- **Firebase**: https://firebase.google.com/docs/
- **Firebase Admin SDK**: https://firebase.google.com/docs/database/admin/start
- **Backboard.io**: https://backboard.io/docs (when ready)
