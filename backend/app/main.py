import json
from fastapi import FastAPI, HTTPException, Query
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
    allow_origins=[
        "http://localhost:3000",
        "https://your-netlify-app.netlify.app",  
    ],    
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
# backend/app/main.py

# ... (keep all your other imports and code) ...

# --- THIS IS A TEMPORARY TEST ENDPOINT ---
# backend/app/main.py

@app.get("/generate-post-stream", summary="Generate LinkedIn Post (with Streaming)")
async def generate_post_stream(topic: str = Query(..., min_length=1)):
    """
    Accepts a topic as a query parameter and streams the agent's response.
    """

    async def stream_agent_response():
        input_prompt = (
            f"Write a professional LinkedIn post about the latest news on the topic: '{topic}'. "
            "The post should be engaging, well-structured, and include 3 relevant hashtags."
        )
        
        try:
            loop = asyncio.get_running_loop()
            
            def get_stream_chunks():
                chunks = []
                for chunk in agent.agent_executor.stream({"input": input_prompt}):
                    chunks.append(chunk)
                return chunks
            
            chunks = await loop.run_in_executor(None, get_stream_chunks)
            
            # Track news sources
            news_sources = []
            
            # Process each chunk
            for chunk in chunks:
                serializable_chunk = {}
                
                if "actions" in chunk and len(chunk["actions"]) > 0:
                    action = chunk["actions"][0]
                    serializable_chunk = {
                        "type": "action",
                        "tool": action.tool,
                        "tool_input": str(action.tool_input),
                        "log": action.log
                    }
                
                elif "steps" in chunk and len(chunk["steps"]) > 0:
                    agent_step = chunk["steps"][0]
                    observation = str(agent_step.observation)[:500]
                    
                    # Extract news sources from observation
                    # The search tool returns titles and links
                    if "Title:" in observation and "Link:" in observation:
                        lines = observation.split('\n')
                        for i, line in enumerate(lines):
                            if line.startswith('Title:') and i + 1 < len(lines) and lines[i + 1].startswith('Link:'):
                                title = line.replace('Title:', '').strip()
                                link = lines[i + 1].replace('Link:', '').strip()
                                if title and link and len(news_sources) < 3:
                                    news_sources.append({
                                        "title": title,
                                        "link": link
                                    })
                    
                    serializable_chunk = {
                        "type": "observation",
                        "observation": observation
                    }
                
                elif "output" in chunk:
                    serializable_chunk = {
                        "type": "output",
                        "output": chunk["output"]
                    }
                
                if serializable_chunk:
                    yield f"data: {json.dumps(serializable_chunk)}\n\n"
                    await asyncio.sleep(0.05)
            
            # Send news sources at the end
            if news_sources:
                yield f"data: {json.dumps({'type': 'sources', 'sources': news_sources})}\n\n"
            
            yield "data: [DONE]\n\n"

        except Exception as e:
            print(f"Streaming error: {e}")
            import traceback
            traceback.print_exc()
            error_message = {"type": "error", "error": str(e)}
            yield f"data: {json.dumps(error_message)}\n\n"

    response = StreamingResponse(stream_agent_response(), media_type="text/event-stream")
    response.headers["Access-Control-Allow-Origin"] = "*"
    response.headers["Cache-Control"] = "no-cache"
    return response
