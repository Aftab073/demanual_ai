# backend/app/config.py

import os
from dotenv import load_dotenv

# Load environment variables from the .env file in the parent 'backend' directory
load_dotenv()

class Settings:
    SERPAPI_KEY: str = os.getenv("SERPAPI_KEY")
    GOOGLE_API_KEY: str = os.getenv("GOOGLE_API_KEY")

settings = Settings()
