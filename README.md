# dreammotion-ai
AI video studio web app with a draggable, animated landing page, user login, and saved projects. Built with HTML, CSS, JavaScript and Python FastAPI.

# DreamMotion AI

**Your Imagination. Your Story. Your Video.**

DreamMotion AI is a full-stack web app for planning AI-powered videos. You can create an account, log in securely, and save your video ideas as projects. The landing page has a dark navy and violet design with draggable character cards.

## 🌐 Live Demo

**Website:** https://smiling-coder.github.io/dreammotion-ai/

The live site is hosted on GitHub Pages and shows the **frontend only**: the landing page, draggable cards and theme toggle. Sign up and login need the Python backend, which runs locally for now (see "How to Run").

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
- **Hosting:** GitHub Pages (frontend)

## Project Structure

```
dreammotion-ai/
├── .github/workflows/
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


## AI Video Generation

AI video generation is **not connected yet**. Without a provider, the server replies that none is configured instead of showing a fake result. To connect one later, copy `.env.example` to `.env` and set `VIDEO_PROVIDER_URL` and `VIDEO_PROVIDER_KEY`. Never put real keys in the frontend files.

## Roadmap

- [x] Landing page and theme
- [x] Login and saved projects
- [x] Live frontend on GitHub Pages
- [ ] Backend hosting for live login
- [ ] Storyboard editor
- [ ] Character library
- [ ] Voice and subtitles
- [ ] Timeline editor and video export
- [ ] Admin dashboard
- [ ] Tests and deployment guide

## Author

Pallavi ([smiling-coder](https://github.com/smiling-coder)), BCA student.
