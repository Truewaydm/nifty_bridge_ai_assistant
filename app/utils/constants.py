import os
from dotenv import load_dotenv

# Create .env file and add parameters
load_dotenv()

API_KEY = os.getenv("OPENAI_API_KEY")
MODEL_NAME = os.getenv("MODEL_NAME")

MAX_TOKENS: int = 4096
INVALID_API_KEY: str = "Invalid API key"
MAX_TOKEN_LIMIT: str = "Response exceeds maximum token limit"
IS_VALID_TOKEN: bool = True
