import os
import asyncio
from dotenv import load_dotenv
from pathlib import Path
from langchain.prompts import PromptTemplate
from langchain.agents import AgentExecutor, create_react_agent, Tool
from langchain_community.utilities import SerpAPIWrapper

from langchain_google_genai import ChatGoogleGenerativeAI 



# Disable optional LangSmith tracing
# os.environ["LANGCHAIN_TRACING_V2"] = "false"


# Load environment variables from the .env file in the 'backend' folder
load_dotenv(dotenv_path=Path(__file__).parent / '.env')


class NewsToLinkedInAgent:
    """An AI Agent that uses tools to generate LinkedIn posts from news."""

    def __init__(self):
        """Initializes the agent, tools, and a reliable, instruction-tuned LLM."""
        serp_api_key = os.getenv("SERPAPI_KEY")
        google_api_key = os.getenv("GOOGLE_API_KEY")


        # 1. Initialize the Search Tool
        search = SerpAPIWrapper(serpapi_api_key=serp_api_key)
        self.tools = [
            Tool(
                name="Search",
                func=search.run,
                description="Useful for searching the web for recent news and events about a topic."
            )
        ]

        # 2. Initialize a powerful, free Instruction-Tuned LLM from Hugging Face
        # Mistral-7B-Instruct is much better at following ReAct agent instructions.
        self.llm = ChatGoogleGenerativeAI(
            model="gemini-2.5-flash", 
            google_api_key=google_api_key,
            temperature=0.7, 
        )

        # 3. Create a Correct Prompt Template for the ReAct Agent
        prompt = PromptTemplate.from_template(
            """
            You are a professional social media manager. Write an insightful and engaging LinkedIn post based on the latest news about the given topic.
            
            You have access to the following tools: {tools}
            
            Use the following format:
            Question: the user's request to write a post about a topic
            Thought: you should always think about what to do. Do you need to use a tool?
            Action: the action to take, should be one of [{tool_names}]
            Action Input: the input to the action
            Observation: the result of the action
            ... (this Thought/Action/Action Input/Observation can repeat N times)
            Thought: I now have enough information to write the LinkedIn post.
            Final Answer: The final, complete LinkedIn post text, and nothing else.
            
            Begin!
            
            Question: {input}
            Thought:{agent_scratchpad}
            """
        )

        # 4. Create the Agent and Executor
        agent = create_react_agent(self.llm, self.tools, prompt)
        self.agent_executor = AgentExecutor(
            agent=agent,
            tools=self.tools,
            verbose=True, # Set to True to see the agent's reasoning process
            handle_parsing_errors=True,
            max_iterations=5
        )

    async def generate_post(self, topic: str) -> dict:
        """Generates a post by running the agent executor in a thread-safe way."""
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
        except Exception as e:
            print(f"Error during agent execution: {e}")
            linkedin_post = f"Sorry, an error occurred while generating the post: {e}"

        return {
            "topic": topic,
            "linkedin_post": linkedin_post,
            "news_sources": [],
            "image_suggestion": f"A professional graphic about '{topic}'."
        }
