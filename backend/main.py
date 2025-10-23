from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from backend.agent import NewsToLinkedInAgent

# Initialize FastAPI app
app = FastAPI(
    title="Demanual AI LinkedIn Post Generator",
    description="An API to generate LinkedIn posts from a topic using an AI agent.",
    version="1.0.0"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class GenerateRequest(BaseModel):
    topic: str

# Instantiate the agent at startup
agent = NewsToLinkedInAgent()

@app.get("/health", summary="Health Check")
async def health():
    return {"status": "ok"}

@app.post("/generate-post", summary="Generate LinkedIn Post")
async def generate_post(request: GenerateRequest):
    """Accepts a topic and returns a generated LinkedIn post."""
    topic = request.topic.strip()
    if not topic:
        raise HTTPException(status_code=400, detail="The 'topic' field cannot be empty.")
    
    try:
        result = await agent.generate_post(topic)
        return result
    except Exception as e:
        # Return a clear error message if anything goes wrong
        raise HTTPException(status_code=500, detail=f"An internal error occurred: {str(e)}")
