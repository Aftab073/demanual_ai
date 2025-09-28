"""
backend/main.py

This file contains the main FastAPI application for the Demanual AI LinkedIn Post Generator.
It sets up the API endpoints, handles requests, and integrates the NewsToLinkedInAgent.
"""
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from .agent import NewsToLinkedInAgent

# Initialize the FastAPI application
app = FastAPI(title="Demanual AI LinkedIn Post Generator")

# Define the list of allowed origins for CORS
origins = [
    "http://localhost",
    "http://localhost:3000", # For React dev server
    "http://127.0.0.1",
    "http://127.0.0.1:3000",
]

# Add CORS middleware to the application
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Define the request model for the /generate-post endpoint
class GenerateRequest(BaseModel):
    topic: str

# Instantiate the agent
agent = NewsToLinkedInAgent()

@app.get("/health", summary="Health Check", description="A simple endpoint to check if the API is running.")
async def health():
    """
    Returns a status of 'ok' to indicate the service is healthy.
    """
    return {"status": "ok"}

@app.post("/generate-post", summary="Generate LinkedIn Post", description="Generates a LinkedIn post based on a given topic.")
async def generate_post(request: GenerateRequest):
    """
    Accepts a topic, uses the agent to find news and generate a post,
    and returns the result as JSON.
    """
    if not request.topic or not request.topic.strip():
        raise HTTPException(status_code=400, detail="The 'topic' field cannot be empty.")
    
    # Generate the post using the agent
    result = agent.generate_post(request.topic)
    
    # Handle potential errors returned from the agent
    if "error" in result:
        raise HTTPException(status_code=500, detail=result["error"])
        
    return result

# To run this application, use the following command in your terminal:
# uvicorn backend.main:app --host 0.0.0.0 --port 8000 --reload
