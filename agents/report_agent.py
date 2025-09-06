from crewai import Agent
from tools.report_tools import ReportGenerationTool
from utils.logger import setup_logger

logger = setup_logger(__name__)

class ReportAgent:
    @staticmethod
    def create_agent() -> Agent:
        return Agent(
            role="Financial Report Writer",
            goal="Generate comprehensive insider trading reports with actionable insights",
            backstory="""You are an experienced financial analyst and report writer 
            specializing in insider trading analysis. You can synthesize complex data 
            into clear, actionable reports that help traders and investors understand 
            market dynamics.""",
            tools=[ReportGenerationTool()],
            verbose=True,
            memory=True,
            max_iter=3,
            max_retry_limit=2
        )