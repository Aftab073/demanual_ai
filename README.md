# Demanual AI: LinkedIn Post Generator

Demanual AI is a smart agent that generates professional, engaging LinkedIn posts from a simple topic. It uses a multi-step reasoning process to search for the latest news on the web and then crafts a post in a style optimized for social media engagement.

This project demonstrates a modern, full-stack AI application architecture using a Python backend, a powerful LLM, and a set of tools for real-world data retrieval.

## Features

-   **AI-Powered Content Creation:** Generates insightful LinkedIn posts complete with relevant hashtags.
-   **Real-Time Web Search:** Uses the SerpAPI tool to find the latest news and information, ensuring content is timely and relevant.
-   **Advanced Agentic Logic:** Built with LangChain, the AI agent uses a ReAct (Reasoning and Acting) framework to dynamically decide when to search for information and when to generate content.
-   **Asynchronous API:** The backend is built with FastAPI, providing a high-performance, non-blocking API.

## Tech Stack

-   **Backend:** Python, FastAPI
-   **AI/LLM:** LangChain, Google Gemini API
-   **Tools:** SerpAPI for web search

## Getting Started

Follow these instructions to set up and run the project locally.

### Prerequisites

-   Python 3.10+
-   An API key from [Google AI Studio](https://aistudio.google.com/)
-   An API key from [SerpAPI](https://serpapi.com/)

### Installation

1.  **Clone the repository:**
    ```
    git clone https://github.com/Aftab073/demanual_ai
    cd demanual_ai/backend
    ```

2.  **Create and activate a virtual environment:**
    ```
    # For macOS/Linux
    python3 -m venv venv
    source venv/bin/activate

    # For Windows
    python -m venv venv
    venv\Scripts\activate
    ```

3.  **Install dependencies:**
    ```
    pip install -r requirements.txt
    ```

4.  **Configure environment variables:**
    Create a file named `.env` inside the `backend/` directory and add your API keys:
    ```
    SERPAPI_KEY="your_serpapi_key_here"
    GOOGLE_API_KEY="your_google_api_key_here"
    ```

### Running the Application

1.  **Start the server:**
    From within the `backend/` directory, run:
    ```
    uvicorn main:app --reload
    ```

2.  **Access the API:**
    The API will be running at `http://127.0.0.1:8000`. You can access the interactive documentation at `http://127.0.0.1:8000/docs`.

## Project Roadmap

-   [x] **Core Agent Logic:** Develop a functional agent that can search and generate posts.
-   [x] **API Development:** Expose the agent's functionality via a FastAPI backend.
-   [ ] **Capture News Sources:** Enhance the agent to return the URLs of the news articles it used.
-   [ ] **Real-Time Streaming:** Implement streaming to show the agent's thought process live.
-   [ ] **Frontend UI:** Build a React-based user interface to interact with the agent.

