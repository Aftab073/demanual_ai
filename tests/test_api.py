import pytest
from httpx import AsyncClient
from unittest.mock import MagicMock

# Import the FastAPI app instance from your main file
from backend.app.main import app

# Define a mock agent that returns a predictable response
class MockNewsToLinkedInAgent:
    def generate_post(self, topic: str):
        if not topic or not topic.strip():
            return {"error": "The 'topic' field cannot be empty."}
        return {
            "topic": topic,
            "news_sources": ["http://mock-news.com/story1"],
            "linkedin_post": f"This is a mock LinkedIn post about {topic}.",
            "image_suggestion": f"A mock image suggestion for {topic}."
        }

# Use a pytest fixture to replace the real agent with our mock agent for all tests
@pytest.fixture(autouse=True)
def override_agent_dependency(monkeypatch):
    """Replaces the real NewsToLinkedInAgent with a mock for testing."""
    monkeypatch.setattr(app, 'agent', MockNewsToLinkedInAgent())

@pytest.mark.asyncio
async def test_health_check():
    """Tests that the /health endpoint is working correctly."""
    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await client.get("/health")
        assert response.status_code == 200
        assert response.json() == {"status": "ok"}

@pytest.mark.asyncio
async def test_generate_post_success():
    """Tests the /generate-post endpoint with a valid topic."""
    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await client.post("/generate-post", json={"topic": "AI advancements"})
        assert response.status_code == 200
        data = response.json()
        assert data["topic"] == "AI advancements"
        assert "linkedin_post" in data
        assert data["linkedin_post"] == "This is a mock LinkedIn post about AI advancements."

@pytest.mark.asyncio
async def test_generate_post_empty_topic():
    """Tests that the API returns a 400 error for an empty topic."""
    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await client.post("/generate-post", json={"topic": " "})
        assert response.status_code == 400
        assert response.json() == {"detail": "The 'topic' field cannot be empty."}

