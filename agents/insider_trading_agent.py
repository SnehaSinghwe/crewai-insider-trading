from crewai import Agent
from tools.sec_tools import InsiderTradingTool
from utils.logger import setup_logger

logger = setup_logger(__name__)

class InsiderTradingAgent:
    @staticmethod
    def create_agent() -> Agent:
        return Agent(
            role="Insider Trading Specialist",
            goal="Identify and analyze insider trading activities from SEC Form 4 filings",
            backstory="""You are a specialist in insider trading analysis with expertise 
            in Form 4 filings. You can identify patterns in insider transactions and 
            assess their significance for market participants.""",
            tools=[InsiderTradingTool()],
            verbose=True,
            memory=True,
            max_iter=3,
            max_retry_limit=2
        )