from crewai import Agent
from tools.sec_tools import SECFilingsTool
from utils.logger import setup_logger
from config.settings import settings

logger = setup_logger(__name__)

class SECDataAgent:
    @staticmethod
    def create_agent() -> Agent:
        return Agent(
            role="SEC Data Analyst",
            goal="Retrieve and analyze SEC filing data from the last 24 hours",
            backstory="""You are an expert SEC data analyst specializing in retrieving 
            and processing regulatory filings. You have deep knowledge of SEC filing 
            requirements and can efficiently extract relevant information from EDGAR database.""",
            tools=[SECFilingsTool()],
            verbose=True,
            memory=True,
            max_iter=3,
            max_retry_limit=2
        )