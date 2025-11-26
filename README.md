# Football Injury Prediction Model

This is a web app that predicts injury risks for football players using machine learning. The frontend is built with React and the backend uses Django.

## What it does

- Predicts injury risk based on player data
- Takes player information through a form
- Gives recommendations based on the prediction
- Has a clean, dark-themed UI
- Uses a REST API to handle predictions

## Project Structure

Pretty straightforward setup:
- `backend/` - All the Django stuff lives here
  - `api/` - The API app with the prediction endpoint
  - `injury_prediction/` - Django project settings
  - `api/models/` - Put your trained model (`injury_model.pkl`) here
- `frontend/` - React app
  - `src/components/` - React components
  - `src/App.jsx` - Main app component

## What you need

Make sure you have these installed:
- Python 3.8+ 
- Node.js 16+
- npm (comes with Node.js)

## Getting Started

### Setting up the Backend

First, let's get Django running:

1. Go to the backend folder:
   ```bash
   cd backend
   ```

2. Create a virtual environment (trust me, you want to do this):
   ```bash
   # On Windows
   python -m venv venv
   venv\Scripts\activate

   # On Mac/Linux
   python3 -m venv venv
   source venv/bin/activate
   ```

3. Install all the Python packages:
   ```bash
   pip install -r requirements.txt
   ```

4. You need to create a `.env` file with a SECRET_KEY. Here's the easiest way to get one:
   
   After installing the dependencies, run:
   ```bash
   python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
   ```
   
   Copy that key and create a `.env` file in the `backend` folder with:
   ```
   SECRET_KEY=whatever-key-you-got
   DEBUG=True
   ```

5. Set up the database:
   ```bash
   python manage.py migrate
   ```

6. (Optional) Create an admin user if you want to access the Django admin:
   ```bash
   python manage.py createsuperuser
   ```

7. Start the server:
   ```bash
   python manage.py runserver
   ```
   
   You should see it running on `http://localhost:8000`

### Setting up the Frontend

Now for the React part:

1. Open a new terminal and go to the frontend folder:
   ```bash
   cd frontend
   ```

2. Install the npm packages:
   ```bash
   npm install
   ```

3. Start the dev server:
   ```bash
   npm run dev
   ```
   
   It'll be running on `http://localhost:5173`

## Adding Your Model

Once you have a trained model, save it as `injury_model.pkl` and put it in `backend/api/models/`. The API will automatically load it when you start the server.

To save your model:
```python
import joblib
joblib.dump(your_trained_model, 'backend/api/models/injury_model.pkl')
```

## Updating the Form Fields

The current form fields are set up for a dummy model. You'll need to:

1. Update `frontend/src/components/PredictionForm.jsx` - change the form fields to match your model's features
2. Update `backend/api/views.py` - modify the `features` array (around line 69) to extract the right data in the right order

Make sure the feature order in the backend matches exactly what your model expects.

## Tech Stack

**Backend:**
- Django 4.2
- Django REST Framework
- scikit-learn
- pandas, numpy

**Frontend:**
- React 18
- Vite (for fast dev server)
- Regular CSS (no frameworks)

## Notes

- The Django admin is at `http://localhost:8000/admin/` if you created a superuser
- The frontend proxies API calls to the backend automatically
- Make sure both servers are running when testing the full app

Security note about OAuth token delivery
---------------------------------------
The app now returns the API token to the frontend after social login using an URL fragment (example: http://localhost:5173/#token=...).
Fragments are not sent to servers and therefore do not appear in server access logs, which reduces the chance of token leakage.

If you'd rather receive the token with a different mechanism (POST exchange, cookie-based session, or hash-less redirect), I can implement that for a more secure production setup.

Social signup behavior
----------------------
By default the app requires users who sign in with Google to complete the site's signup form (manual completion). If an account is not yet provisioned for the incoming social login the user will be redirected to a social signup page where they must confirm or fill in any missing fields before the local account is created.

If you prefer immediate auto-provisioning (skip manual signup) change `SOCIALACCOUNT_AUTO_SIGNUP = True` in `backend/injury_prediction/settings.py`. Be aware this will create local accounts automatically when the provider supplies enough information (email, name).

Running the end-to-end test (Playwright)
---------------------------------------
We've added a lightweight Playwright-based e2e test that verifies the frontend captures a token fragment after a simulated social login. To run it locally:

1. Install frontend deps and Playwright (from the workspace root or in `frontend`):

```bash
cd frontend
npm install
npx playwright install
```

2. Start the frontend dev server (dev server must be running during the test):

```bash
npm run dev
```

3. Run the tests in a separate terminal:

```bash
npm run test:e2e
```

The test doesn't communicate with Google — it intercepts the backend login URL and simulates the redirect back to the SPA with a token (suitable for CI/local verification).

## Troubleshooting: Google OAuth / "Continue with Google" errors

If clicking "Continue with Google" results in a server error like:


Follow these steps:

1. Duplicate app config (MultipleObjectsReturned)
   - This happens when allauth finds more than one Google app configuration. There are two ways to configure provider credentials:
     - The Django admin (SocialApp model)
     - The `SOCIALACCOUNT_PROVIDERS` `APP` block in `backend/injury_prediction/settings.py`
   - Make sure you only use one method. The project defaults to keeping credentials in the database (Django Admin). If you put credentials both places, allauth will see two apps and raise MultipleObjectsReturned.
   - Fix: remove the `APP` key from `SOCIALACCOUNT_PROVIDERS` in `backend/injury_prediction/settings.py` or delete the duplicate SocialApp in the Django admin so only one app exists.

2. redirect_uri_mismatch / Authorization errors from Google
   - In the Google Cloud Console -> Credentials for your OAuth client make sure the "Authorized redirect URIs" includes:
     `http://localhost:8000/accounts/google/login/callback/`
   - Also ensure the client type is "Web application" and the Client ID / Client Secret match the SocialApp record or the settings-based `APP` values.

3. Frontend URL / CORS
   - The frontend uses `VITE_BACKEND_URL` (falls back to http://localhost:8000). If your backend runs on a different URL/port, set the env var in `frontend/.env`:

```
VITE_BACKEND_URL=http://localhost:8000
```

Then restart your frontend dev server so the env changes are picked up.

Authentication prompt behavior
------------------------------
If Google is already signed-in in the browser (common), Google normally won't ask the user for a password again —
it will simply let them choose an account and continue. If you want to force the user to re-enter their Google
password on every sign-in, configure the provider to include a `prompt` parameter. This project uses the
`prompt=login` option by default so the user will be asked to re-authenticate.

You can change the behavior in `backend/injury_prediction/settings.py` under `SOCIALACCOUNT_PROVIDERS['google']['AUTH_PARAMS']`.
Available values include `login` (force re-auth), `select_account` (show account chooser), and `consent` (force consent screen).

