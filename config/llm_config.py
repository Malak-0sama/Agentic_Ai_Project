import os

from dotenv import load_dotenv


load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

GEMINI_MODEL = os.getenv("GEMINI_MODEL", "gemini-3.6-flash")

# Do not raise at import time — that would break Streamlit diagnostics and
# unrelated module imports when the key is temporarily missing. Callers that
# need the API (GeminiProvider) still validate and raise a clear error.
