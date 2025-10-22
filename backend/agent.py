# backend/agent.py

import os
import asyncio
from typing import Dict, Any, List
from langchain.tools import Tool
from dotenv import load_dotenv
from pathlib import Path

# --- LangChain Imports ---
from langchain_huggingface import HuggingFaceEndpoint
from langchain_community.utilities import SerpAPIWrapper
from langchain.agents import AgentExecutor, create_react_agent
from langchain import hub

# Load environment variables
dotenv_path = Path(__file__).parent / '.env'
load_dotenv(dotenv_path=dotenv_path)

class NewsToLinkedInAgent:
    """
    An agent built with LangChain that generates LinkedIn posts from recent news.
    """
    def __init__(self):
        serp_api_key = os.getenv("SERPAPI_KEY")
        hf_api_key = os.getenv("HUGGING_FACE_API_KEY")

        # 1. Initialize tools
        search = SerpAPIWrapper(serpapi_api_key=serp_api_key)

        # 2. Wrap the search tool so it has a name and description
        self.tools = [
            Tool(
                name="Search Tool",
                func=search.run,
                description="Useful for searching current events or recent news about a topic."
            )
        ]

        # 3. Create your Hugging Face LLM
        self.llm = HuggingFaceEndpoint(
            repo_id=os.getenv("HF_MODEL", "mistralai/Mixtral-8x7B-Instruct-v0.1"),
            huggingfacehub_api_token=hf_api_key,
            temperature=0.7,
        )

        # 4. Pull a generic ReAct prompt from LangChain Hub (this is okay; Hub warning is harmless)
        prompt = hub.pull("hwchase17/react")

        # 5. Initialize the actual ReAct agent
        agent = create_react_agent(self.llm, self.tools, prompt)
        self.agent_executor = AgentExecutor(agent=agent, tools=self.tools, verbose=True)

    async def generate_post(self, topic: str) -> dict:
        """
        Generates a LinkedIn post by invoking the LangChain agent.
        """
        # We create a specific, detailed query for the agent.
        prompt = f"""
        Based on the latest news about '{topic}', write a professional and engaging LinkedIn post.

        The post must have:
        - A professional tone suitable for a LinkedIn audience.
        - 3 to 6 short paragraphs that summarize the key points.
        - 2 to 3 bullet points suggesting different angles for discussion.
        - At least 3 relevant hashtags.

        Your final answer should only be the LinkedIn post content itself, nothing else.
        """
        
        # Use 'ainvoke' for an asynchronous call to the agent executor
        response = await self.agent_executor.ainvoke({"input": prompt})

        # The final result is in the 'output' key
        linkedin_post = response.get("output", "Error: Could not generate content.")
        
        # Note: Extracting sources is more complex with LangChain agents. 
        # For this assignment, we'll return an empty list as a placeholder.
        return {
            "topic": topic,
            "news_sources": [],
            "linkedin_post": linkedin_post,
            "image_suggestion": f"A professional graphic related to '{topic}' showing innovation."
        }
