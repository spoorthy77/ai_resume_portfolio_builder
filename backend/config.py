import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", "secret_key_here")
    GROQ_API_KEY = os.getenv("GROQ_API_KEY", "")
