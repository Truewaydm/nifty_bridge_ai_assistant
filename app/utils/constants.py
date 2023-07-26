import os
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("OPENAI_API_KEY")
MODEL_NAME = os.getenv("MODEL_NAME")

MAX_TOKENS: int = 4096
INVALID_API_KEY: str = "Invalid API key"
MAX_TOKEN_LIMIT: str = "Response exceeds maximum token limit"
IS_VALID_TOKEN: bool = True


def get_file_path(path: str, name_of_file: str):
    """
    Get the path to the JSON file
    """
    current_directory = os.path.dirname(os.path.abspath(__file__))
    app_directory = os.path.dirname(current_directory)
    return os.path.join(app_directory, path, name_of_file)
