# dreammotion-ai
AI video studio web app with a draggable, animated landing page, user login, and saved projects. Built with HTML, CSS, JavaScript and Python FastAPI.


# DreamMotion AI

**Your Imagination. Your Story. Your Video.**

DreamMotion AI is a full-stack web app for planning AI-powered videos. You can create an account, log in securely, and save your video ideas as projects. The landing page has a dark navy and violet design with draggable character cards.

## Features

- Animated landing page with draggable cards (Bear, Pillu, Scene 1)
- Light and dark theme
- Sign up and login with hashed passwords
- Create, view and delete projects
- Honest AI setup: the server says clearly when no video provider is connected

## Tech Stack

- **Frontend:** HTML, CSS, JavaScript
- **Backend:** Python, FastAPI
- **Database:** SQLite

## Project Structure

```
dreammotion-ai/
├── backend/
│   ├── app/
│   │   ├── __init__.py
│   │   └── main.py
│   └── requirements.txt
├── frontend/
│   ├── index.html
│   ├── styles.css
│   └── app.js
├── .env.example
└── README.md
```

## How to Run

### 1. Start the backend

```
cd backend
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000
```

On Mac or Linux, use `source venv/bin/activate` instead of `venv\Scripts\activate`.

### 2. Start the frontend

Open a new terminal:

```
cd frontend
python -m http.server 5500
```

### 3. Open the website

Go to `http://localhost:5500`

## AI Video Generation

AI video generation is **not connected yet**. Without a provider, the server replies that none is configured instead of showing a fake result. To connect one later, copy `.env.example` to `.env` and set `VIDEO_PROVIDER_URL` and `VIDEO_PROVIDER_KEY`. Never put real keys in the frontend files.

## Roadmap

- [x] Landing page and theme
- [x] Login and saved projects
- [ ] Storyboard editor
- [ ] Character library
- [ ] Voice and subtitles
- [ ] Timeline editor and video export
- [ ] Admin dashboard
- [ ] Tests and deployment guide

## Author

Pallavi ([smiling-coder](https://github.com/smiling-coder)), BCA student.
