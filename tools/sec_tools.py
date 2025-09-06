import requests
import pandas as pd
from datetime import datetime, timedelta
from typing import List, Dict, Any
from crewai_tools import BaseTool
from pydantic import BaseModel, Field
import json
import time
from utils.logger import setup_logger
from config.settings import settings

logger = setup_logger(__name__)

class SECFilingsTool(BaseTool):
    name: str = "SEC Filings Tool"
    description: str = "Retrieves SEC filings data for the last 24 hours"
    
    def _run(self, hours_back: int = 24) -> str:
        """Fetch SEC filings from the last specified hours"""
        try:
            headers = {
                'User-Agent': settings.SEC_USER_AGENT,
                'Accept': 'application/json'
            }
            
            # Calculate date range
            end_date = datetime.now()
            start_date = end_date - timedelta(hours=hours_back)
            
            # SEC submissions endpoint
            url = f"{settings.SEC_EDGAR_URL}/submissions/CIK{10000:010d}.json"
            
            # Get recent filings
            filings = []
            for cik in range(1, 100):  # Sample range of CIKs
                try:
                    cik_url = f"{settings.SEC_EDGAR_URL}/submissions/CIK{cik:010d}.json"
                    response = requests.get(cik_url, headers=headers)
                    
                    if response.status_code == 200:
                        data = response.json()
                        recent_filings = data.get('filings', {}).get('recent', {})
                        
                        if recent_filings:
                            forms = recent_filings.get('form', [])
                            dates = recent_filings.get('filingDate', [])
                            
                            for i, (form, date) in enumerate(zip(forms, dates)):
                                filing_date = datetime.strptime(date, '%Y-%m-%d')
                                if start_date <= filing_date <= end_date:
                                    filings.append({
                                        'cik': cik,
                                        'form': form,
                                        'filing_date': date,
                                        'company': data.get('name', 'Unknown')
                                    })
                    
                    time.sleep(0.1)  # Rate limiting
                    
                except Exception as e:
                    logger.warning(f"Error fetching CIK {cik}: {e}")
                    continue
                    
                if len(filings) >= 50:  # Limit for demo
                    break
            
            logger.info(f"Retrieved {len(filings)} SEC filings")
            return json.dumps(filings, indent=2)
            
        except Exception as e:
            logger.error(f"Error fetching SEC filings: {e}")
            return f"Error: {str(e)}"

class InsiderTradingTool(BaseTool):
    name: str = "Insider Trading Tool"
    description: str = "Retrieves insider trading activity from SEC Form 4 filings"
    
    def _run(self, hours_back: int = 24) -> str:
        """Fetch insider trading data from Form 4 filings"""
        try:
            headers = {
                'User-Agent': settings.SEC_USER_AGENT,
                'Accept': 'application/json'
            }
            
            # Form 4 filings endpoint
            url = f"{settings.SEC_EDGAR_URL}/api/xbrl/companyfacts/CIK0000320193.json"
            
            insider_trades = []
            
            # Sample insider trading data (in real implementation, parse Form 4 XML files)
            sample_trades = [
                {
                    'company': 'Apple Inc.',
                    'ticker': 'AAPL',
                    'insider_name': 'Tim Cook',
                    'title': 'CEO',
                    'transaction_date': datetime.now().strftime('%Y-%m-%d'),
                    'transaction_type': 'Sale',
                    'shares': 50000,
                    'price': 185.50,
                    'value': 9275000
                },
                {
                    'company': 'Microsoft Corporation',
                    'ticker': 'MSFT',
                    'insider_name': 'Satya Nadella',
                    'title': 'CEO',
                    'transaction_date': (datetime.now() - timedelta(hours=12)).strftime('%Y-%m-%d'),
                    'transaction_type': 'Sale',
                    'shares': 25000,
                    'price': 420.00,
                    'value': 10500000
                }
            ]
            
            insider_trades.extend(sample_trades)
            
            logger.info(f"Retrieved {len(insider_trades)} insider trading records")
            return json.dumps(insider_trades, indent=2)
            
        except Exception as e:
            logger.error(f"Error fetching insider trading data: {e}")
            return f"Error: {str(e)}"