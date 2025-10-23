# backend/main.py

import json
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from app.agent import NewsToLinkedInAgent  # Corrected import
from fastapi.responses import StreamingResponse
import asyncio

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

@app.post("/generate-post", summary="Generate LinkedIn Post (No Streaming)")
async def generate_post(request: GenerateRequest):
    """Accepts a topic and returns a generated LinkedIn post without streaming."""
    topic = request.topic.strip()
    if not topic:
        raise HTTPException(status_code=400, detail="The 'topic' field cannot be empty.")
    
    try:
        result = await agent.generate_post(topic)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An internal error occurred: {str(e)}")

# --- NEW: Streaming Endpoint ---
@app.post("/generate-post-stream", summary="Generate LinkedIn Post (with Streaming)")
async def generate_post_stream(request: GenerateRequest):
    """
    Accepts a topic and streams the agent's thought process and final output.
    """
    topic = request.topic.strip()
    if not topic:
        raise HTTPException(status_code=400, detail="The 'topic' field cannot be empty.")

    async def stream_agent_response():
        """Asynchronous generator that yields agent steps as JSON strings."""
        input_prompt = (
            f"Write a professional LinkedIn post about the latest news on the topic: '{topic}'. "
            "The post should be engaging, well-structured, and include 3 relevant hashtags."
        )
        
        # Use the agent's `stream` method for real-time output
        async for chunk in agent.agent_executor.stream({"input": input_prompt}):
            # Each chunk is a dictionary representing a step in the agent's process
            # We'll format it as a server-sent event (SSE)
            yield f"data: {json.dumps(chunk)}\n\n"
            await asyncio.sleep(0.1) # Small delay to make the stream more visible

    return StreamingResponse(stream_agent_response(), media_type="text/event-stream")

