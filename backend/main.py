import os
from fastapi import FastAPI
from dotenv import load_dotenv
from pydantic import BaseModel
from backend.agent import create_linkedin_agent

load_dotenv()

app = FastAPI()
agent_executor = create_linkedin_agent()

class Query(BaseModel):
    topic: str

@app.post("/generate-post")
async def generate_post(query: Query):
    """Generates a LinkedIn post based on a news topic."""
    prompt = f"Generate an engaging and professional LinkedIn post about the latest news on '{query.topic}'. Include relevant hashtags."
    response = agent_executor.invoke({"input": prompt})
    return {"post": response["output"]}
