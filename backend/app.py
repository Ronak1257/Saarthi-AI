from fastapi import FastAPI, Request, Depends, HTTPException
from db import SessionLocal, engine
from models import Base, Goal, Conversation, User
import os, json, random
from dotenv import load_dotenv
from groq import Groq
from passlib.context import CryptContext
from jose import JWTError, jwt
from sqlalchemy.orm import Session
from fastapi.middleware.cors import CORSMiddleware

load_dotenv()

# Config
client = Groq(api_key=os.getenv("GROQ_API_KEY"))
Base.metadata.create_all(bind=engine)
app = FastAPI()
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
JWT_SECRET = os.getenv("JWT_SECRET")
JWT_ALGORITHM = os.getenv("JWT_ALGORITHM")

# Load wisdom JSON
with open("wisdom.json", "r", encoding="utf-8") as f:
    wisdom_data = json.load(f)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # You can restrict this to your frontend URL later
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Dependency for DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Utility functions
def hash_password(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(password: str, hashed: str) -> bool:
    return pwd_context.verify(password, hashed)

def create_access_token(data: dict):
    return jwt.encode(data, JWT_SECRET, algorithm=JWT_ALGORITHM)

def decode_access_token(token: str):
    try:
        return jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")

# Register endpoint
@app.post("/register")
async def register(request: Request, db: Session = Depends(get_db)):
    data = await request.json()
    email = data["email"]
    password = data["password"]

    if db.query(User).filter(User.email == email).first():
        raise HTTPException(status_code=400, detail="Email already registered")

    hashed_pw = hash_password(password)
    new_user = User(email=email, password_hash=hashed_pw)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return {"message": "User registered successfully"}

# Login endpoint
@app.post("/login")
async def login(request: Request, db: Session = Depends(get_db)):
    data = await request.json()
    email = data["email"]
    password = data["password"]

    user = db.query(User).filter(User.email == email).first()
    if not user or not verify_password(password, user.password_hash):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    token = create_access_token({"user_id": user.id, "email": user.email})
    return {"access_token": token}

# Chat endpoint (auth required)
@app.post("/chat")
async def chat_with_ai(request: Request, db: Session = Depends(get_db)):
    data = await request.json()
    token = data.get("token")
    if not token:
        raise HTTPException(status_code=401, detail="Token required")

    user_data = decode_access_token(token)

    user_id = user_data["user_id"]
    message = data["message"]

    goal = db.query(Goal).filter(Goal.user_id == user_id).first()

    system_prompt = f"You are a wise and motivating AI life companion. \
    The user’s short-term goal is: {goal.short_term_goal if goal else 'Not set'}. \
    Long-term goal is: {goal.long_term_goal if goal else 'Not set'}. \
    Use wisdom from the Bhagavad Gita and modern productivity quotes to guide them."

    wisdom_piece = random.choice(
        wisdom_data["bhagavad_gita"] + [{"text": q} for q in wisdom_data["modern_quotes"]]
    )
    wisdom_text = wisdom_piece["text"]

    response = client.chat.completions.create(
        model="llama3-8b-8192",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": f"{message}\n(Wisdom reference: {wisdom_text})"}
        ],
        temperature=0.7,
        max_tokens=500
    )

    ai_reply = response.choices[0].message.content

    conv = Conversation(user_id=user_id, message=message, ai_response=ai_reply)
    db.add(conv)
    db.commit()

    return {"reply": ai_reply}

# Set goals endpoint (auth required)
@app.post("/set-goals")
async def set_goals(request: Request, db: Session = Depends(get_db)):
    data = await request.json()
    token = data.get("token")
    if not token:
        raise HTTPException(status_code=401, detail="Token required")

    user_data = decode_access_token(token)
    user_id = user_data["user_id"]
    short_goal = data["short_term_goal"]
    long_goal = data["long_term_goal"]

    goal = Goal(user_id=user_id, short_term_goal=short_goal, long_term_goal=long_goal)
    db.merge(goal)
    db.commit()

    return {"status": "goals_saved"}

@app.get("/history")
async def get_history(
    token: str,
    page: int = 1,
    limit: int = 10,
    db: Session = Depends(get_db)
):
    # Decode JWT
    user_data = decode_access_token(token)
    user_id = user_data["user_id"]

    # Calculate offset
    offset = (page - 1) * limit

    # Fetch conversations
    conversations = (
        db.query(Conversation)
        .filter(Conversation.user_id == user_id)
        .order_by(Conversation.created_at.asc())
        .offset(offset)
        .limit(limit)
        .all()
    )

    # Count total messages
    total_count = db.query(Conversation).filter(Conversation.user_id == user_id).count()

    # Format response
    history_list = [
        {
            "message": conv.message,
            "reply": conv.ai_response,
            "created_at": conv.created_at.strftime("%Y-%m-%d %H:%M:%S")
        }
        for conv in conversations
    ]

    return {
        "page": page,
        "limit": limit,
        "total": total_count,
        "pages": (total_count + limit - 1) // limit,
        "history": history_list
    }
