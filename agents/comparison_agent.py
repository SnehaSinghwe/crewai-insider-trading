from crewai import Agent
from tools.chart_tools import ChartGenerationTool
from utils.logger import setup_logger

logger = setup_logger(__name__)

class ComparisonAgent:
    @staticmethod
    def create_agent() -> Agent:
        return Agent(
            role="Data Analysis and Visualization Expert",
            goal="Compare current insider trading data with historical patterns and create visualizations",
            backstory="""You are a data visualization expert specializing in financial 
            market analysis. You excel at creating compelling charts and identifying 
            trends in trading data that help investors make informed decisions.""",
            tools=[ChartGenerationTool()],
            verbose=True,
            memory=True,
            max_iter=3,
            max_retry_limit=2
        )