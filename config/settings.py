import os
from dotenv import load_dotenv
from pathlib import Path

load_dotenv()

class Settings:
    # LLM Configuration
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")
    LITELLM_MODEL = os.getenv("LITELLM_MODEL", "gpt-4o-mini")
    
    # SEC Configuration
    SEC_USER_AGENT = os.getenv("SEC_USER_AGENT", "your_email@example.com")
    SEC_BASE_URL = "https://www.sec.gov"
    SEC_EDGAR_URL = "https://data.sec.gov"
    
    # File Paths
    BASE_DIR = Path(__file__).parent.parent
    OUTPUT_DIR = BASE_DIR / "output"
    REPORTS_DIR = OUTPUT_DIR / "reports"
    CHARTS_DIR = OUTPUT_DIR / "charts"
    DATA_DIR = BASE_DIR / "data"
    
    # Logging
    LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
    
    # Create directories if they don't exist
    for dir_path in [OUTPUT_DIR, REPORTS_DIR, CHARTS_DIR, DATA_DIR]:
        dir_path.mkdir(parents=True, exist_ok=True)

settings = Settings()