from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# Try importing your router safely
try:
    from matching import router  # Absolute import (works on Vercel)
except ImportError:
    from .matching import router  # Fallback for local dev

app = FastAPI(title="CrewAI Student Matching")

# ✅ Update with your deployed frontend URL (no trailing slash!)
origins = [
    "https://agentic-ai-study-group-creation-io.vercel.app",  # ✅ removed trailing slash
    "http://localhost:3000",
    "http://127.0.0.1:3000"
]

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],  # Allow all HTTP methods
    allow_headers=["*"],  # Allow all headers
)

# Include your routes
app.include_router(router)

@app.get("/")
def root():
    return {"message": "CrewAI Student Matching API is running 🚀"}
