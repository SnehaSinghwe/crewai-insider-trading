import asyncio
import os
import sys
from datetime import datetime
from pathlib import Path

# Add project root to Python path
sys.path.append(str(Path(__file__).parent))

from flows.insider_trading_flow import InsiderTradingFlow
from utils.logger import setup_logger
from config.settings import settings
from data.storage import DataStorage
import litellm

# Configure LiteLLM
litellm.api_key = settings.OPENAI_API_KEY

logger = setup_logger(__name__)

def check_environment():
    """Check if all required environment variables are set"""
    required_vars = ['OPENAI_API_KEY', 'SEC_USER_AGENT']
    missing_vars = []
    
    for var in required_vars:
        if not os.getenv(var):
            missing_vars.append(var)
    
    if missing_vars:
        logger.error(f"Missing required environment variables: {missing_vars}")
        logger.error("Please set these variables in your .env file")
        return False
    
    return True

def print_banner():
    """Print application banner"""
    banner = """
    ╔══════════════════════════════════════════════════════════════╗
    ║                 CrowdWisdomTrading AI Agent                  ║
    ║                 Insider Trading Analysis                     ║
    ║                      Powered by CrewAI                       ║
    ╚══════════════════════════════════════════════════════════════╝
    """
    print(banner)

async def main():
    """Main execution function"""
    print_banner()
    logger.info("Starting CrowdWisdomTrading AI Agent...")
    
    # Check environment
    if not check_environment():
        sys.exit(1)
    
    try:
        # Initialize data storage
        storage = DataStorage()
        logger.info("Data storage initialized")
        
        # Create and run the CrewAI flow
        logger.info("Initializing CrewAI Flow...")
        flow = InsiderTradingFlow()
        
        # Execute the flow
        logger.info("Starting insider trading analysis flow...")
        result = flow.kickoff()
        
        logger.info("Flow execution completed successfully!")
        logger.info(f"Results: {result}")
        
        # Print summary
        print("\n" + "="*60)
        print("EXECUTION SUMMARY")
        print("="*60)
        print(f"Status: {result.get('status', 'Unknown')}")
        print(f"Report Path: {result.get('report_path', 'Not generated')}")
        print(f"Charts: {result.get('chart_paths', 'Not generated')}")
        print("="*60)
        
        return result
        
    except KeyboardInterrupt:
        logger.info("Process interrupted by user")
        print("\nProcess interrupted by user. Exiting...")
        sys.exit(0)
        
    except Exception as e:
        logger.error(f"Error during execution: {e}")
        print(f"\nError: {e}")
        sys.exit(1)

def run_analysis():
    """Synchronous wrapper for the main function"""
    try:
        # Run the async main function
        if sys.platform == "win32":
            asyncio.set_event_loop_policy(asyncio.WindowsProactorEventLoopPolicy())
        
        return asyncio.run(main())
        
    except Exception as e:
        logger.error(f"Failed to run analysis: {e}")
        raise

if __name__ == "__main__":
    run_analysis()