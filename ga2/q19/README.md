# Q19: FastAPI Google OAuth Login Verification

## 🎯 What Are We Building?

A FastAPI application that lets users log in with their Google account (like "Sign in with Google" buttons you see everywhere). After logging in, we'll get a special token called an `id_token` that proves who you are.

**Think of it like:** Getting a VIP pass to a concert. Instead of creating a new password for every venue, you show your Google ID (which you already have), and they give you a wristband (the id_token) that proves you're allowed in.

---

## 📚 Step-by-Step Solution

### Part 1: Understanding OAuth (5 minutes)

**What is OAuth?**
- OAuth is like asking your parents for permission to go somewhere
- You (the app) ask Google (the parent) if the user can log in
- Google asks the user "Do you trust this app?"
- If yes, Google gives you a special key (token) proving the user said yes

**What is an id_token?**
- A special encrypted message from Google
- Contains user info: email, name, etc.
- Proves the user really logged in with Google
- Expires after some time (for security)

---

### Part 2: Setting Up Google OAuth Credentials (15-20 minutes)

This is the trickiest part, but follow carefully!

#### Step 1: Go to Google Cloud Console

1. **Open:** https://console.cloud.google.com/
2. **Sign in** with your **personal Google account** (not the IIT Madras one yet!)
3. You should see the Google Cloud Console dashboard

#### Step 2: Create a New Project

1. **Click** the project dropdown at the top (says "Select a project")
2. **Click** "NEW PROJECT"
3. **Name it:** "FastAPI OAuth GA2" (or anything you like)
4. **Click** "CREATE"
5. **Wait** ~30 seconds for it to be created
6. **Select** your new project from the dropdown

#### Step 3: Enable Google+ API (Required for OAuth)

1. **Go to:** https://console.cloud.google.com/apis/library
2. **Search for:** "Google+ API" (yes, even though Google+ is dead!)
3. **Click** on "Google+ API"
4. **Click** "ENABLE"
5. **Wait** for it to enable (~10 seconds)

**Alternative:** Search for "People API" and enable that (newer alternative)

#### Step 4: Configure OAuth Consent Screen

1. **Go to:** https://console.cloud.google.com/apis/credentials/consent
2. **Choose:** "External" (allows any Google account)
3. **Click** "CREATE"

**Fill in the form:**
- **App name:** "FastAPI OAuth Test"
- **User support email:** Your email (auto-filled)
- **Developer contact:** Your email again
- **Click** "SAVE AND CONTINUE"

**On Scopes page:**
- **Click** "ADD OR REMOVE SCOPES"
- **Check these boxes:**
  - `openid`
  - `email`
  - `profile` (userinfo.email and userinfo.profile)
- **Click** "UPDATE"
- **Click** "SAVE AND CONTINUE"

**On Test Users page:**
- **Click** "ADD USERS"
- **Add:** `your-student-id` (the email you'll log in with)
- **Click** "ADD"
- **Click** "SAVE AND CONTINUE"

**On Summary page:**
- **Click** "BACK TO DASHBOARD"

#### Step 5: Create OAuth Credentials

1. **Go to:** https://console.cloud.google.com/apis/credentials
2. **Click** "CREATE CREDENTIALS" → OAuth client ID
3. **Application type:** Web application
4. **Name:** "FastAPI OAuth Client"

**Authorized redirect URIs:**
- **Click** "ADD URI"
- **Add:** `http://localhost:8000/auth`
- **Why?** This is where Google sends users after they log in

5. **Click** "CREATE"

#### Step 6: Copy Your Credentials

A popup will show your credentials:
- **Client ID:** Something like `123456789-abc.apps.googleusercontent.com`
- **Client Secret:** Something like `GOCSPX-abc123xyz`

**IMPORTANT:** Copy both of these! You'll need them in the next step.

---

### Part 3: Setting Up the FastAPI Application (10 minutes)

#### Step 1: Install Dependencies

Open PowerShell in the `ga2/q19` directory:

```powershell
cd ga2/q19
pip install fastapi uvicorn authlib itsdangerous httpx python-dotenv
```

**What are these?**
- `fastapi` - The web framework
- `uvicorn` - Runs the web server
- `authlib` - Handles OAuth (the Google login stuff)
- `httpx` - Makes HTTP requests to Google
- `python-dotenv` - Loads secrets from .env file

#### Step 2: Create the .env File

Create a file called `.env` in `ga2/q19`:

```env
GOOGLE_CLIENT_ID=YOUR_CLIENT_ID_HERE.apps.googleusercontent.com
GOOGLE_CLIENT_SECRET=YOUR_CLIENT_SECRET_HERE
SECRET_KEY=my-super-secret-key-change-this-in-production
```

**Replace:** 
- `YOUR_CLIENT_ID_HERE` with your actual Client ID from Step 6
- `YOUR_CLIENT_SECRET_HERE` with your actual Client Secret from Step 6

**Example:**
```env
GOOGLE_CLIENT_ID=123456789-abc123xyz.apps.googleusercontent.com
GOOGLE_CLIENT_SECRET=GOCSPX-xyz789abc456
SECRET_KEY=my-super-secret-key-change-this-in-production
```

---

### Part 4: Running the Application (5 minutes)

#### Step 1: Start the Server

```powershell
cd ga2/q19
uvicorn main:app --reload
```

**You should see:**
```
INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
INFO:     Started reloader process [12345] using StatReload
INFO:     Started server process [67890]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
```

#### Step 2: Test the App

1. **Open browser:** http://localhost:8000
2. **You should see:** `{"message": "Welcome! Please log in.", "login_url": "/login"}`

---

### Part 5: Logging In and Getting the id_token (5 minutes)

#### Step 1: Start the Login Flow

**In your browser, go to:** http://localhost:8000/login

**What happens:**
1. You're redirected to Google's login page
2. Google asks "FastAPI OAuth Test wants to access your Google Account"
3. **Select your account:** Choose `your-student-id`
4. **Click** "Continue" or "Allow"
5. You're redirected back to http://localhost:8000

#### Step 2: Get Your id_token

**Go to:** http://localhost:8000/id_token

**You should see:**
```json
{
  "id_token": "eyJhbGciOiJSUzI1NiIsImtpZCI6IjE5ZmU..."
}
```

**Copy the entire id_token** (it's a very long string starting with `eyJ`)

#### Step 3: Get Your Client ID

You already have this from Part 2, Step 6!

---

### Part 6: Submitting Your Answer (2 minutes)

Create a JSON file with both values:

```json
{
  "id_token": "eyJhbGciOiJSUzI1NiIsImtpZCI6IjE5ZmU...",
  "client_id": "123456789-abc123xyz.apps.googleusercontent.com"
}
```

**Submit this JSON** as your answer!

---

## 🔍 How It Works (The Magic Explained)

### The OAuth Flow:

```
1. User visits /login
   ↓
2. App redirects to Google
   ↓
3. User logs in with Google
   ↓
4. Google redirects back to /auth with a "code"
   ↓
5. App exchanges "code" for tokens (including id_token)
   ↓
6. App stores tokens in session
   ↓
7. User can now access /id_token to see their token
```

### What's in the id_token?

The `id_token` is a JWT (JSON Web Token) containing:

```json
{
  "iss": "https://accounts.google.com",  // Who issued it (Google)
  "aud": "your-client-id",                // Who it's for (your app)
  "sub": "1234567890",                    // User's unique Google ID
  "email": "your-student-id",
  "email_verified": true,                 // Email is verified
  "name": "Your Name",
  "picture": "https://...",               // Profile picture URL
  "iat": 1234567890,                      // Issued at (timestamp)
  "exp": 1234571490                       // Expires at (timestamp)
}
```

---

## 🐛 Troubleshooting

### Error: "redirect_uri_mismatch"
**Problem:** The redirect URI doesn't match what you configured in Google Cloud Console.

**Solution:**
1. Go back to Google Cloud Console → Credentials
2. Edit your OAuth Client ID
3. Make sure `http://localhost:8000/auth` is in the Authorized redirect URIs
4. Save and try again

### Error: "Access blocked: This app's request is invalid"
**Problem:** OAuth consent screen not configured properly.

**Solution:**
1. Go to OAuth consent screen
2. Make sure `your-student-id` is added as a test user
3. Save and try again

### Error: "Not authenticated"
**Problem:** You haven't logged in yet.

**Solution:**
1. Go to http://localhost:8000/login
2. Complete the login flow
3. Try accessing /id_token again

### Error: "Module not found: authlib"
**Problem:** Dependencies not installed.

**Solution:**
```powershell
pip install -r requirements.txt
```

---

## 📝 Key Endpoints

| Endpoint | Purpose |
|----------|---------|
| `/` | Home page - shows login status |
| `/login` | Starts the OAuth flow |
| `/auth` | Callback URL for Google |
| `/id_token` | Returns the id_token |
| `/user` | Shows user info (debugging) |
| `/logout` | Clears session |

---

## 🔐 Security Notes

### Why OAuth is Better Than Passwords:

1. **No Password Storage:** You don't store or handle passwords
2. **Delegated Authentication:** Google handles all the security
3. **Single Sign-On:** Users can use one Google account everywhere
4. **Token Expiration:** Tokens expire automatically
5. **Revocable:** Users can revoke access anytime from their Google account

### Security Checklist:

- ✅ Never commit `.env` file to git
- ✅ Use strong SECRET_KEY in production
- ✅ Use HTTPS in production (not http)
- ✅ Validate the id_token before trusting it
- ✅ Check token expiration
- ✅ Store tokens securely

---

## 💡 Real-World Applications

### Where OAuth is Used:

1. **"Sign in with Google" buttons** everywhere
2. **Mobile apps** that need user identity
3. **Enterprise apps** connecting to company accounts
4. **API access** with user permissions
5. **Third-party integrations** (e.g., Zapier, IFTTT)

### Why Companies Use It:

- **Reduces support costs** (no password resets)
- **Better security** (Google handles it)
- **Faster user onboarding** (one-click login)
- **Trust** (users trust Google more than random sites)

---

## 🚀 Quick Start (TL;DR)

```powershell
# 1. Install dependencies
pip install fastapi uvicorn authlib itsdangerous httpx python-dotenv

# 2. Create .env file with your Google credentials
# GOOGLE_CLIENT_ID=...
# GOOGLE_CLIENT_SECRET=...

# 3. Run the server
uvicorn main:app --reload

# 4. Visit http://localhost:8000/login
# 5. Log in with your-student-id
# 6. Go to http://localhost:8000/id_token
# 7. Copy the id_token and client_id
# 8. Submit as JSON
```

---

## 📚 Additional Resources

- **OAuth 2.0 Explained:** https://oauth.net/2/
- **Google OAuth Docs:** https://developers.google.com/identity/protocols/oauth2
- **FastAPI OAuth Tutorial:** https://fastapi.tiangolo.com/advanced/security/oauth2-scopes/
- **JWT Decoder (for testing):** https://jwt.io/

---

## ❓ FAQ

**Q: Can I use my personal email instead of the IIT one?**
A: No, the grader checks that the email is exactly `your-student-id`.

**Q: Do I need to verify my OAuth app?**
A: No, for testing purposes you can keep it in "Testing" mode.

**Q: How long does the id_token last?**
A: Usually 1 hour. Get it right before submitting.

**Q: Can I reuse credentials from a previous assignment?**
A: Yes, if you already have a Google OAuth client set up, just update the redirect URI.

**Q: What if I get "This app isn't verified"?**
A: Click "Advanced" → "Go to [app name] (unsafe)" - it's safe because it's your own app.

