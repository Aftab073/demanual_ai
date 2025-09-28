import os
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.agents import tool, AgentExecutor, create_react_agent
from langchain import hub
from serpapi import GoogleSearch

@tool
def get_recent_news(query: str) -> str:
    """Searches for recent news about a given topic and returns the top result."""
    params = {
        "q": query,
        "tbm": "nws",
        "api_key": os.environ["SERPAPI_KEY"],
    }
    search = GoogleSearch(params)
    results = search.get_dict()
    news_results = results.get("news_results", [])
    return news_results[0]["snippet"] if news_results else "No recent news found."

def create_linkedin_agent():
    """Creates an agent that can generate a LinkedIn post from recent news."""
    llm = ChatGoogleGenerativeAI(model="gemini-pro", temperature=0.7)
    tools = [get_recent_news]
    prompt = hub.pull("hwchase17/react")
    agent = create_react_agent(llm, tools, prompt)
    return AgentExecutor(agent=agent, tools=tools, verbose=True)
