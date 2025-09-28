
# Demanual AI - LinkedIn Post Generator

This project generates a LinkedIn post from recent news using FastAPI, Google Gemini, and a web search tool.

## Deployment

### Render
- The `Procfile` is configured for Render deployment.
- Set the environment variables `GEMINI_API_KEY` and `SERPAPI_KEY` in the Render dashboard.

### Vercel
- For Vercel, you would typically place the `backend/main.py` code inside an `api/index.py` file.
- Add a `vercel.json` file to configure the build and routing.
