from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware # Import the middleware
from . import matching

app = FastAPI(title="CrewAI Student Matching")

# Add CORS middleware
origins = [
    "http://localhost:3000", # The origin of your React frontend
    "http://127.0.0.1:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"], # Allow all HTTP methods
    allow_headers=["*"], # Allow all headers
)

# Include routes
app.include_router(matching.router)

@app.get("/")
def root():
    return {"message": "CrewAI Student Matching API is running 🚀"}