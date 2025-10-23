from langchain_community.utilities import SerpAPIWrapper

class SearchToolWithSources:
    """A wrapper around SerpAPI to capture search result sources."""
    def __init__(self, serp_api_key):
        # We need to ask SerpAPI for the source and snippet, not just a single answer
        params = {
            "engine": "google",
            "gl": "us",
            "hl": "en",
        }
        self.search_tool = SerpAPIWrapper(params=params, serpapi_api_key=serp_api_key)
        self.sources = []

    def run(self, query: str):
        """Run a search and capture the sources from the results."""
        # Reset sources for each new search run
        self.sources = []
        
        # The SerpAPIWrapper can return a dictionary if we ask for more data
        results = self.search_tool.results(query)
        
        # Process the results to extract sources and snippets
        output = ""
        if "organic_results" in results:
            for result in results["organic_results"][:4]: # Limit to top 4 results
                self.sources.append({
                    "title": result.get("title"),
                    "link": result.get("link")
                })
                output += f"Title: {result.get('title')}\n"
                output += f"Link: {result.get('link')}\n"
                output += f"Snippet: {result.get('snippet')}\n\n"
        
        if not output:
            return "No good search results found."
            
        return output