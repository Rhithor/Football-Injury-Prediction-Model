# Google OAuth Setup Guide

This guide will help you set up Google OAuth for the Injury Prediction Model.

## Step 1: Create Google OAuth Credentials

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project or select an existing one
3. Enable the Google+ API:
   - Go to "APIs & Services" > "Library"
   - Search for "Google+ API"
   - Click "Enable"
4. Create OAuth 2.0 credentials:
   - Go to "APIs & Services" > "Credentials"
   - Click "Create Credentials" > "OAuth client ID"
   - If prompted, create an OAuth consent screen first:
     - Choose "External"
     - Fill in app name, user support email, and developer contact
     - Add scopes: `email`, `profile`
     - Add test users (your email)
   - For application type, select "Web application"
   - Add authorized redirect URI:
     ```
     http://localhost:8000/accounts/google/login/callback/
     ```
   - Click "Create"
   - You'll see your Client ID and Client Secret - **copy these**

## Step 2: Set Environment Variables

Create or update the `.env` file in the `backend` folder:

```
SECRET_KEY=your-django-secret-key
DEBUG=True
GOOGLE_CLIENT_ID=your-client-id-here
GOOGLE_SECRET=your-client-secret-here
```

Replace:
- `your-client-id-here` with your Google Client ID
- `your-client-secret-here` with your Google Client Secret

## Step 3: Register Google OAuth in Django

Run the setup script from the backend directory:

```bash
cd backend
# Make sure your virtual environment is activated
env/Scripts/activate  # On Windows
# or: source env/bin/activate  # On Mac/Linux

python scripts/create_socialapp.py
```

You should see output like:
```
SocialApp for google created/updated and attached to site: localhost:8000
```

## Step 4: Verify Setup

1. Go to Django Admin: `http://localhost:8000/admin/`
2. Login with your superuser account
3. Navigate to "Social applications"
4. You should see a "Google" entry with:
   - Provider: Google
   - Client id: (your client ID)
   - Secret: (your client secret)
   - Sites: localhost:8000

## Step 5: Test It

1. Go to the frontend: `http://localhost:5173/register`
2. Click "Sign up with Google"
3. Select your Google account
4. You should now see the signup form instead of an error

## Troubleshooting

### "Third-Party Login Failure" error
- Check that `GOOGLE_CLIENT_ID` and `GOOGLE_SECRET` are correctly set in `.env`
- Verify the SocialApp exists in Django admin
- Check that the authorized redirect URI in Google Cloud Console matches exactly

### MultipleObjectsReturned error
- You have duplicate Google app configurations
- Go to Django admin > Social applications
- Delete any duplicate Google entries (keep only one)
- If you see the same entry twice, one might be in settings and one in the database
- Remove the `APP` key from `SOCIALACCOUNT_PROVIDERS['google']` in `backend/injury_prediction/settings.py`

### redirect_uri_mismatch error
- In Google Cloud Console, go to Credentials
- Edit your OAuth client
- Make sure "Authorized redirect URIs" includes: `http://localhost:8000/accounts/google/login/callback/`
- The URL must match exactly (including protocol and port)

### CORS errors
- Make sure `VITE_BACKEND_URL` is set correctly in `frontend/.env`
- Default is `http://localhost:8000`
- Both frontend and backend servers must be running

## Production Deployment

For production, you'll need to:

1. Update authorized redirect URI in Google Cloud Console:
   ```
   https://your-production-domain.com/accounts/google/login/callback/
   ```

2. Set environment variables on your production server:
   ```
   GOOGLE_CLIENT_ID=production-client-id
   GOOGLE_SECRET=production-client-secret
   FRONTEND_URL=https://your-production-domain.com
   ```

3. Update `ALLOWED_HOSTS` and `CSRF_TRUSTED_ORIGINS` in Django settings

4. Run the setup script again on the production server to create/update the SocialApp
