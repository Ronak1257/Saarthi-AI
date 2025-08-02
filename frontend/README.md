# Saarthi AI — Goal-Driven AI Life Companion

Saarthi AI is a personal AI life companion that remembers your goals, tracks your progress, and motivates you using wisdom from the Bhagavad Gita, Ramayan, and modern productivity principles.

This monorepo contains:
- **Frontend** → React + TailwindCSS + Vite
- **Backend** → FastAPI + SQLite (dev) / Postgres (prod) + Groq API

## 📂 Project Structure

saarthi-ai/
├── backend/ # FastAPI backend
│ ├── app.py
│ ├── db.py
│ ├── models.py
│ ├── wisdom.json
│ ├── requirements.txt
│ └── .env
└── frontend/ # React + Tailwind frontend
├── src/
├── package.json
├── tailwind.config.js
└── vite.config.js


## 🚀 Features
- User authentication (JWT)
- Goal setting (short & long term)
- AI chat with wisdom injection
- Chat history with pagination
- Clean dashboard UI

## 🛠 Tech Stack
**Frontend:** React, Vite, TailwindCSS, Axios, React Router  
**Backend:** FastAPI, SQLAlchemy, SQLite/Postgres, Groq API, JWT

## 📅 Roadmap
- [ ] Wisdom search with RAG
- [ ] Voice chat integration
- [ ] Cloud deployment (Vercel + Railway)
- [ ] Goal progress analytics
