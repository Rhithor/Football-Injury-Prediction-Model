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

