import os
import asyncio
import re
from pathlib import Path
from langchain.prompts import PromptTemplate
from langchain.agents import AgentExecutor, create_react_agent, Tool
from langchain_community.utilities import SerpAPIWrapper
from langchain_google_genai import ChatGoogleGenerativeAI

from app.config import settings  
from app.search_tool import SearchToolWithSources

class NewsToLinkedInAgent:
    def __init__(self):
        serp_api_key = os.getenv("SERPAPI_KEY")
        google_api_key = os.getenv("GOOGLE_API_KEY")

        # --- Use the new SearchToolWithSources ---
        self.search_with_sources = SearchToolWithSources(serp_api_key=serp_api_key)
        self.tools = [
            Tool(
                name="Search",
                func=self.search_with_sources.run,
                description="Useful for searching the web for recent news, events, and information about a topic. Returns a list of search results with titles, links, and snippets."
            )
        ]

        # Initialize the Google Gemini Model
        self.llm = ChatGoogleGenerativeAI(
            model="gemini-2.5-flash", # Or another model from your check_models.py output
            google_api_key=google_api_key,
            temperature=0.7,
        )

        # Create a Prompt Template
        prompt = PromptTemplate.from_template(
            """
            You are a professional social media manager. Your goal is to write an insightful and engaging LinkedIn post based on the latest news about the given topic. You must use the 'Search' tool to find relevant information before writing your final answer.

            You have access to the following tools: {tools}

            Use the following format:
            Question: The user's request to write a post about a topic.
            Thought: You should always think about what to do. You must use the 'Search' tool.
            Action: The action to take, should be one of [{tool_names}].
            Action Input: The input to the action (the topic to search for).
            Observation: The result of the action.
            ... (this Thought/Action/Action Input/Observation can repeat, but you should only search once).
            Thought: I now have enough information, including multiple news snippets, to write the LinkedIn post.
            Final Answer: The final, complete LinkedIn post text, and nothing else. Make sure it is well-structured and engaging.

            Begin!

            Question: {input}
            Thought:{agent_scratchpad}
            """
        )

        # Create the Agent and Executor
        agent = create_react_agent(self.llm, self.tools, prompt)
        self.agent_executor = AgentExecutor(
            agent=agent,
            tools=self.tools,
            verbose=True,
            handle_parsing_errors=True,
            max_iterations=5,
        )

    async def generate_post(self, topic: str) -> dict:
        """Generates a post and includes the captured news sources."""
        input_prompt = (
            f"Write a professional LinkedIn post about the latest news on the topic: '{topic}'. "
            "The post should be engaging, well-structured, and include 3 relevant hashtags."
        )
        loop = asyncio.get_running_loop()
        
        try:
            response = await loop.run_in_executor(
                None,
                lambda: self.agent_executor.invoke({"input": input_prompt})
            )
            linkedin_post = response.get("output", "Error: Could not generate content.")
            # --- Get the captured sources from our custom tool ---
            news_sources = self.search_with_sources.sources
            
        except Exception as e:
            print(f"Error during agent execution: {e}")
            linkedin_post = f"Sorry, an error occurred while generating the post: {e}"
            news_sources = []

        return {
            "topic": topic,
            "linkedin_post": linkedin_post,
            "news_sources": news_sources,
            "image_suggestion": f"A professional graphic about '{topic}'."
        }
