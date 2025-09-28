<h1 align="center">Demanual AI - LinkedIn Post Generator</h1>

<p align="center">
  <em>An AI-powered backend service that automatically generates professional LinkedIn posts from recent news.</em>
</p>

<hr>

<h3>Project Description</h3>

<p>
This project is a backend service that automatically generates professional LinkedIn posts based on a given topic. It fetches the latest news articles using the SerpApi web search API, synthesizes the information using a powerful large language model from Hugging Face, and formats the output into an engaging post complete with content ideas and hashtags. The entire project was built following step-by-step guidance, demonstrating a streamlined and "demanualized" development process.
</p>

<hr>

<h3>Tech Stack</h3>

<ul>
  <li><b>Backend:</b> Python 3.11, FastAPI</li>
  <li><b>Web Server:</b> Gunicorn, Uvicorn</li>
  <li><b>AI & LLMs:</b> Hugging Face InferenceClient (Mixtral model)</li>
  <li><b>Web Search:</b> Google Search Results for Python (SerpApi)</li>
  <li><b>Testing:</b> Pytest, HTTPX</li>
  <li><b>Deployment:</b> Render</li>
</ul>

<hr>

<h3>Local Setup and Installation</h3>

<ol>
  <li>
    <strong>Clone the Repository</strong>
    <pre><code>git clone https://github.com/Aftab073/demanual_ai.git
cd demanual_ai</code></pre>
  </li>
  <li>
    <strong>Create and Activate a Virtual Environment</strong>
    <pre><code>python3 -m venv venv
source venv/bin/activate</code></pre>
  </li>
  <li>
    <strong>Set Up Environment Variables</strong>
    <p>Copy the example environment file and add your secret API keys.</p>
    <pre><code>cp backend/.env.example backend/.env</code></pre>
    <p>Now, edit <code>backend/.env</code> with your keys.</p>
  </li>
  <li>
    <strong>Install Dependencies</strong>
    <pre><code>pip install -r backend/requirements.txt</code></pre>
  </li>
  <li>
    <strong>Run the Development Server</strong>
    <pre><code>uvicorn backend.main:app --reload</code></pre>
    <p>The API is now available at <code>http://127.0.0.1:8000</code>.</p>
  </li>
</ol>

<hr>

<h3>API Usage and Endpoints</h3>

<h4>Generate a Post</h4>
<p>Send a <code>POST</code> request to the <code>/generate-post</code> endpoint with your desired topic.</p>

<strong>Example cURL Request:</strong>
<pre><code>curl -X POST "http://127.0.0.1:8000/generate-post" \
-H "Content-Type: application/json" \
-d '{"topic": "advancements in quantum computing"}'</code></pre>

<h4>API Documentation (Swagger UI)</h4>
<p>Interactive API documentation is available when the server is running.</p>
<ul>
    <li><b>Local URL:</b> <a href="http://127.0.0.1:8000/docs">http://127.0.0.1:8000/docs</a></li>
    <li><b>Hosted URL:</b> <code>https://demanual-ai.onrender.com/docs</code></li>
</ul>

<hr>


