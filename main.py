import os, sqlite3, secrets, hashlib, time
from fastapi import FastAPI, HTTPException, Header
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

DB = os.getenv("DATABASE_PATH", "dreammotion.db")
app = FastAPI(title="DreamMotion AI")
app.add_middleware(CORSMiddleware,
    allow_origins=[os.getenv("ALLOWED_ORIGIN", "http://localhost:5500")],
    allow_methods=["*"], allow_headers=["*"])

def db():
    c = sqlite3.connect(DB); c.row_factory = sqlite3.Row
    c.execute("PRAGMA foreign_keys=ON"); return c

with db() as c:
    c.executescript("""
    CREATE TABLE IF NOT EXISTS users(id INTEGER PRIMARY KEY, email TEXT UNIQUE NOT NULL,
      salt TEXT NOT NULL, hash TEXT NOT NULL, role TEXT DEFAULT 'user');
    CREATE TABLE IF NOT EXISTS sessions(token TEXT PRIMARY KEY,
      user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE, expires REAL);
    CREATE TABLE IF NOT EXISTS projects(id INTEGER PRIMARY KEY,
      user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
      title TEXT NOT NULL, prompt TEXT DEFAULT '', status TEXT DEFAULT 'draft', created REAL);
    """)

def hash_pw(pw, salt): return hashlib.pbkdf2_hmac("sha256", pw.encode(), bytes.fromhex(salt), 200_000).hex()

class Cred(BaseModel):
    email: str = Field(min_length=5, max_length=120, pattern=r"^[^@\s]+@[^@\s]+\.[^@\s]+$")
    password: str = Field(min_length=8, max_length=100)
class ProjectIn(BaseModel):
    title: str = Field(min_length=1, max_length=120)
    prompt: str = Field(default="", max_length=4000)

def user_from(auth):
    if not auth or not auth.startswith("Bearer "): raise HTTPException(401, "Please log in.")
    with db() as c:
        r = c.execute("SELECT user_id FROM sessions WHERE token=? AND expires>?", (auth[7:], time.time())).fetchone()
    if not r: raise HTTPException(401, "Session expired. Log in again.")
    return r["user_id"]

def new_session(c, uid):
    t = secrets.token_urlsafe(32)
    c.execute("INSERT INTO sessions VALUES(?,?,?)", (t, uid, time.time() + 7 * 86400)); return t

@app.post("/api/register")
def register(d: Cred):
    salt = secrets.token_hex(16)
    try:
        with db() as c:
            uid = c.execute("INSERT INTO users(email,salt,hash) VALUES(?,?,?)",
                            (d.email.lower(), salt, hash_pw(d.password, salt))).lastrowid
            return {"token": new_session(c, uid)}
    except sqlite3.IntegrityError:
        raise HTTPException(409, "That email is already registered.")

@app.post("/api/login")
def login(d: Cred):
    with db() as c:
        u = c.execute("SELECT * FROM users WHERE email=?", (d.email.lower(),)).fetchone()
        if not u or not secrets.compare_digest(u["hash"], hash_pw(d.password, u["salt"])):
            raise HTTPException(401, "Email or password is incorrect.")
        return {"token": new_session(c, u["id"])}

@app.get("/api/projects")
def list_projects(authorization: str = Header(None)):
    uid = user_from(authorization)
    with db() as c:
        return [dict(r) for r in c.execute("SELECT id,title,prompt,status FROM projects WHERE user_id=? ORDER BY id DESC", (uid,))]

@app.post("/api/projects")
def add_project(p: ProjectIn, authorization: str = Header(None)):
    uid = user_from(authorization)
    with db() as c:
        pid = c.execute("INSERT INTO projects(user_id,title,prompt,created) VALUES(?,?,?,?)",
                        (uid, p.title, p.prompt, time.time())).lastrowid
    return {"id": pid}

@app.delete("/api/projects/{pid}")
def del_project(pid: int, authorization: str = Header(None)):
    uid = user_from(authorization)
    with db() as c: c.execute("DELETE FROM projects WHERE id=? AND user_id=?", (pid, uid))
    return {"ok": True}

@app.get("/api/providers")
def providers():
    on = bool(os.getenv("VIDEO_PROVIDER_URL"))
    return {"configured": on, "message": "Provider ready." if on else
            "No video provider is configured. Set VIDEO_PROVIDER_URL in .env. Editing and storyboards still work."}

@app.post("/api/generate")
def generate(p: ProjectIn, authorization: str = Header(None)):
    user_from(authorization)
    if not os.getenv("VIDEO_PROVIDER_URL"):
        raise HTTPException(503, "No video provider is configured. See README, step 4.")
    raise HTTPException(501, "Provider adapter not written yet (Phase 4).")
