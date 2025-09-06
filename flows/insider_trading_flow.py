from crewai import Crew, Task
from crewai.flow import Flow, listen, start
from agents.sec_data_agent import SECDataAgent
from agents.insider_trading_agent import InsiderTradingAgent  
from agents.comparison_agent import ComparisonAgent
from agents.report_agent import ReportAgent
from utils.logger import setup_logger
from config.settings import settings
import litellm
from typing import Dict, Any

logger = setup_logger(__name__)

# Configure LiteLLM
litellm.api_key = settings.OPENAI_API_KEY
litellm.model = settings.LITELLM_MODEL

class InsiderTradingFlow(Flow):
    """CrewAI Flow for insider trading analysis"""
    
    def __init__(self):
        super().__init__()
        self.sec_agent = SECDataAgent.create_agent()
        self.insider_agent = InsiderTradingAgent.create_agent()
        self.comparison_agent = ComparisonAgent.create_agent()
        self.report_agent = ReportAgent.create_agent()
        
    @start()
    def fetch_sec_data(self) -> Dict[str, Any]:
        """Start the flow by fetching SEC data"""
        logger.info("Starting SEC data retrieval...")
        
        task = Task(
            description="""Retrieve SEC filing data from the last 24 hours. 
            Focus on recent filings that might indicate insider trading activity.
            Return the data in JSON format with company names, filing types, and dates.""",
            agent=self.sec_agent,
            expected_output="JSON formatted SEC filings data from last 24 hours"
        )
        
        crew = Crew(
            agents=[self.sec_agent],
            tasks=[task],
            verbose=True
        )
        
        result = crew.kickoff()
        logger.info("SEC data retrieval completed")
        
        return {
            "sec_data": str(result),
            "status": "completed"
        }
    
    @listen(fetch_sec_data)
    def analyze_insider_trading(self, sec_context: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze insider trading activity based on SEC data"""
        logger.info("Starting insider trading analysis...")
        
        task = Task(
            description=f"""Analyze insider trading activity from Form 4 filings in the last 24 hours.
            Use the SEC data context: {sec_context['sec_data']}
            
            Identify:
            - Key insider transactions (buys/sells)
            - Transaction volumes and values
            - Notable patterns or unusual activity
            
            Return detailed insider trading data in JSON format.""",
            agent=self.insider_agent,
            expected_output="JSON formatted insider trading analysis with transaction details"
        )
        
        crew = Crew(
            agents=[self.insider_agent],
            tasks=[task],
            verbose=True
        )
        
        result = crew.kickoff()
        logger.info("Insider trading analysis completed")
        
        return {
            "sec_data": sec_context["sec_data"],
            "insider_data": str(result),
            "status": "completed"
        }
    
    @listen(analyze_insider_trading)
    def create_comparisons(self, analysis_context: Dict[str, Any]) -> Dict[str, Any]:
        """Create charts comparing current and historical data"""
        logger.info("Starting chart generation...")
        
        task = Task(
            description=f"""Create comprehensive charts and visualizations comparing 
            current insider trading activity with historical patterns.
            
            Current insider trading data: {analysis_context['insider_data']}
            
            Generate:
            - Trading volume charts by company
            - Transaction value distributions
            - Transaction type breakdowns
            - Time-based activity patterns
            
            Save all charts and return the file paths.""",
            agent=self.comparison_agent,
            expected_output="List of generated chart file paths with descriptions"
        )
        
        crew = Crew(
            agents=[self.comparison_agent],
            tasks=[task],
            verbose=True
        )
        
        result = crew.kickoff()
        logger.info("Chart generation completed")
        
        return {
            "sec_data": analysis_context["sec_data"],
            "insider_data": analysis_context["insider_data"],
            "chart_paths": str(result),
            "status": "completed"
        }
    
    @listen(create_comparisons)
    def generate_final_report(self, chart_context: Dict[str, Any]) -> Dict[str, Any]:
        """Generate the final comprehensive report"""
        logger.info("Starting final report generation...")
        
        task = Task(
            description=f"""Generate a comprehensive insider trading analysis report 
            incorporating all collected data and visualizations.
            
            Include:
            - SEC filings data: {chart_context['sec_data']}
            - Insider trading analysis: {chart_context['insider_data']}
            - Generated charts: {chart_context['chart_paths']}
            
            Create a professional HTML report with:
            - Executive summary with key metrics
            - Most active insider trading companies
            - Detailed transaction tables
            - Market insights and analysis
            - Embedded chart references
            
            Save the report and return the file path.""",
            agent=self.report_agent,
            expected_output="Path to generated comprehensive insider trading report"
        )
        
        crew = Crew(
            agents=[self.report_agent],
            tasks=[task],
            verbose=True
        )
        
        result = crew.kickoff()
        logger.info("Final report generation completed")
        
        return {
            "report_path": str(result),
            "sec_data": chart_context["sec_data"],
            "insider_data": chart_context["insider_data"],
            "chart_paths": chart_context["chart_paths"],
            "status": "completed"
        }