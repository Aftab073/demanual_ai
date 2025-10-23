# backend/check_models.py

import os
import google.generativeai as genai
from dotenv import load_dotenv

# Load the .env file to get the API key
load_dotenv()

try:
    # Configure the client with your API key
    genai.configure(api_key=os.environ["GOOGLE_API_KEY"])

    print("Successfully connected to Google AI. Available models for text generation:")
    
    # List all available models and filter for the ones that can generate text
    for m in genai.list_models():
        if 'generateContent' in m.supported_generation_methods:
            print(f"- {m.name}")

except Exception as e:
    print(f"An error occurred: {e}")
    print("\nPlease ensure your GOOGLE_API_KEY is correct in the .env file.")

