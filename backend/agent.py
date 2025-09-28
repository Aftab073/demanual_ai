"""
backend/agent.py

Defines the NewsToLinkedInAgent class using Hugging Face's native InferenceClient
and SerpApi, using the modern 'chat_completion' method.
"""
import os
import logging
from typing import List, Dict
from dotenv import load_dotenv
from serpapi import GoogleSearch
from huggingface_hub import InferenceClient
from pathlib import Path

# Load environment variables
dotenv_path = Path(__file__).parent / '.env'
load_dotenv(dotenv_path=dotenv_path)

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class NewsToLinkedInAgent:
    """
    An agent that uses Hugging Face's InferenceClient to generate LinkedIn posts.
    """
    def __init__(self):
        """Initializes the agent and sets up API clients."""
        self.hf_token = os.getenv("HUGGING_FACE_API_KEY")
        self.serpapi_key = os.getenv("SERPAPI_KEY")

        if not self.hf_token or not self.serpapi_key:
            raise ValueError("HUGGING_FACE_API_KEY and SERPAPI_KEY must be set.")

        # Initialize the native Hugging Face InferenceClient
        self.client = InferenceClient(token=self.hf_token)
        self.model = "mistralai/Mixtral-8x7B-Instruct-v0.1"

    def _run_web_search(self, query: str, num_results: int = 3) -> List[Dict[str, str]]:
        """Performs a web search for recent news articles using SerpApi."""
        try:
            params = {
                "q": query,
                "tbm": "nws",
                "api_key": self.serpapi_key,
                "num": num_results,
            }
            search = GoogleSearch(params)
            results = search.get_dict()
            news_results = results.get("news_results", [])
            return [{"url": item.get("link"), "snippet": item.get("snippet")} for item in news_results]
        except Exception as e:
            logging.error(f"Error during SerpAPI search for '{query}': {e}")
            return []

    def generate_post(self, topic: str) -> dict:
        """Generates a LinkedIn post using the 'chat_completion' method."""
        search_queries = [
            f"latest news on {topic}",
            f"{topic} recent developments",
        ]
        
        all_sources = []
        for query in search_queries:
            all_sources.extend(self._run_web_search(query))

        unique_sources = {source['url']: source for source in all_sources if source.get('url')}
        top_sources = list(unique_sources.values())[:3]
        
        if not top_sources:
            return {"error": "Could not find any recent news sources for the topic."}

        context_snippets = "\n".join([f"- {source['snippet']}" for source in top_sources])

        # Use a list of messages, which is the standard for chat completion
        messages = [
            {
                "role": "user",
                "content": f"""
                Act as a marketing expert. Based on the following news snippets about '{topic}', write a professional and engaging LinkedIn post.

                News Snippets:
                {context_snippets}

                The post should have:
                - A professional tone suitable for a LinkedIn audience.
                - 3 to 6 short paragraphs that summarize the key points.
                - 2 to 3 bullet points suggesting different angles or ideas for discussion.
                - Relevant hashtags.
                """
            }
        ]

        try:
            # Use the chat_completion method as per the latest documentation
            response = self.client.chat_completion(
                model=self.model,
                messages=messages,
                max_tokens=500
            )
            # The response object has a 'choices' attribute
            linkedin_post = response.choices[0].message.content
        except Exception as e:
            logging.error(f"Error generating post with Hugging Face model: {e}")
            return {"error": "Failed to generate LinkedIn post content."}
            
        return {
            "topic": topic,
            "news_sources": [source['url'] for source in top_sources],
            "linkedin_post": linkedin_post,
            "image_suggestion": f"A professional graphic related to '{topic}' showing innovation."
        }

if __name__ == '__main__':
    agent = NewsToLinkedInAgent()
    result = agent.generate_post(topic="advancements in AI hardware")
    print(result)
