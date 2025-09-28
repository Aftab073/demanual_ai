"""
backend/agent.py

Defines the NewsToLinkedInAgent class using LangChain, Google Gemini, and SerpApi.
- Loads API keys from environment variables.
- Performs web searches for recent news.
- Generates a LinkedIn post using Google's generative model.
- Includes error handling and timeouts for external API calls.
"""
import os
import logging
from typing import List, Dict
from dotenv import load_dotenv
from serpapi import GoogleSearch
from langchain_google_genai import ChatGoogleGenerativeAI

# Load environment variables from a .env file
from pathlib import Path
dotenv_path = Path(__file__).parent / '.env'
load_dotenv(dotenv_path=dotenv_path)

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class NewsToLinkedInAgent:
    """
    An agent that finds recent news on a topic and generates a professional LinkedIn post.
    """
    def __init__(self):
        """Initializes the agent by loading API keys and setting up clients."""
        self.gemini_key = os.getenv("GEMINI_API_KEY")
        self.serpapi_key = os.getenv("SERPAPI_KEY")

        if not self.gemini_key or not self.serpapi_key:
            raise ValueError("GEMINI_API_KEY and SERPAPI_KEY must be set in your .env file.")

        # Initialize the Google Gemini client
        self.llm = ChatGoogleGenerativeAI(model="gemini-1.0-pro", google_api_key=self.gemini_key)

    def _run_web_search(self, query: str, num_results: int = 3) -> List[Dict[str, str]]:
        """
        Performs a web search for recent news articles using the SerpApi.
        """
        try:
            params = {
                "q": query,
                "tbm": "nws",  # 'nws' for news search
                "api_key": self.serpapi_key,
                "num": num_results,
            }
            search = GoogleSearch(params)
            results = search.get_dict()
            news_results = results.get("news_results", [])
            
            return [
                {"url": item.get("link"), "snippet": item.get("snippet")}
                for item in news_results
            ]
        except Exception as e:
            logging.error(f"Error during SerpAPI search for '{query}': {e}")
            return []

    def generate_post(self, topic: str) -> dict:
        """
        Generates a LinkedIn post by searching for news and using Gemini for content creation.
        """
        # 1. Run web searches to gather recent news
        search_queries = [
            f"latest news on {topic}",
            f"{topic} recent developments",
            f"breaking news {topic}"
        ]
        
        all_sources = []
        for query in search_queries:
            all_sources.extend(self._run_web_search(query))

        # 2. Collect and deduplicate top URLs and snippets
        unique_sources = {source['url']: source for source in all_sources if source.get('url')}
        top_sources = list(unique_sources.values())[:3]
        
        if not top_sources:
            return {
                "error": "Could not find any recent news sources for the topic."
            }

        context_snippets = "\n".join([f"- {source['snippet']}" for source in top_sources])

        # 3. Use Gemini to generate the LinkedIn post
        prompt = f"""
        Act as a marketing expert. Based on the following news snippets about '{topic}', write a professional and engaging LinkedIn post.

        News Snippets:
        {context_snippets}

        The post should have:
        - A professional tone suitable for a LinkedIn audience.
        - 3 to 6 short paragraphs that summarize the key points.
        - 2 to 3 bullet points suggesting different angles or ideas for discussion.
        - Relevant hashtags.
        """

        try:
            response = self.llm.invoke(prompt)
            linkedin_post = response.content
        except Exception as e:
            logging.error(f"Error generating post with Gemini: {e}")
            return {"error": "Failed to generate LinkedIn post content."}
            
        # 4. Return the final JSON structure
        return {
            "topic": topic,
            "news_sources": [source['url'] for source in top_sources],
            "linkedin_post": linkedin_post,
            "image_suggestion": f"A professional graphic related to '{topic}' showing growth or innovation."
        }

# Example of how to run the agent (for testing)
if __name__ == '__main__':
    agent = NewsToLinkedInAgent()
    result = agent.generate_post(topic="advancements in large language models")
    print(result)
