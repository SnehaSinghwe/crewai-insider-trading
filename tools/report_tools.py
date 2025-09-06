from crewai_tools import BaseTool
from datetime import datetime
import json
from pathlib import Path
from typing import Dict, List
from utils.logger import setup_logger
from config.settings import settings

logger = setup_logger(__name__)

class ReportGenerationTool(BaseTool):
    name: str = "Report Generation Tool"
    description: str = "Generates comprehensive insider trading reports with analysis"
    
    def _run(self, sec_data: str, insider_data: str, chart_paths: str = "") -> str:
        """Generate comprehensive report"""
        try:
            # Parse input data
            sec_filings = json.loads(sec_data) if sec_data else []
            insider_trades = json.loads(insider_data) if insider_data else []
            
            # Generate report
            report = self._generate_html_report(sec_filings, insider_trades, chart_paths)
            
            # Save report
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            report_path = settings.REPORTS_DIR / f"insider_trading_report_{timestamp}.html"
            
            with open(report_path, 'w', encoding='utf-8') as f:
                f.write(report)
            
            logger.info(f"Report generated: {report_path}")
            return str(report_path)
            
        except Exception as e:
            logger.error(f"Error generating report: {e}")
            return f"Error generating report: {str(e)}"
    
    def _generate_html_report(self, sec_filings: List[Dict], insider_trades: List[Dict], chart_paths: str) -> str:
        """Generate HTML report"""
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        
        # Calculate summary statistics
        total_trades = len(insider_trades)
        total_value = sum(trade.get('value', 0) for trade in insider_trades)
        total_shares = sum(trade.get('shares', 0) for trade in insider_trades)
        
        # Get most active companies
        company_activity = {}
        for trade in insider_trades:
            company = trade.get('company', 'Unknown')
            company_activity[company] = company_activity.get(company, 0) + trade.get('value', 0)
        
        most_active = sorted(company_activity.items(), key=lambda x: x[1], reverse=True)[:5]
        
        html_content = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <title>Insider Trading Analysis Report</title>
            <style>
                body {{ font-family: Arial, sans-serif; margin: 40px; }}
                .header {{ background-color: #2c3e50; color: white; padding: 20px; text-align: center; }}
                .summary {{ background-color: #ecf0f1; padding: 20px; margin: 20px 0; }}
                .section {{ margin: 20px 0; }}
                table {{ border-collapse: collapse; width: 100%; }}
                th, td {{ border: 1px solid #ddd; padding: 8px; text-align: left; }}
                th {{ background-color: #f2f2f2; }}
                .metric {{ display: inline-block; margin: 10px; padding: 10px; background-color: #3498db; color: white; border-radius: 5px; }}
            </style>
        </head>
        <body>
            <div class="header">
                <h1>CrowdWisdomTrading - Insider Trading Analysis</h1>
                <p>Report Generated: {timestamp}</p>
            </div>
            
            <div class="summary">
                <h2>Executive Summary</h2>
                <div class="metric">Total Trades: {total_trades}</div>
                <div class="metric">Total Value: ${total_value:,.0f}</div>
                <div class="metric">Total Shares: {total_shares:,.0f}</div>
            </div>
            
            <div class="section">
                <h2>Most Active Companies (Last 24 Hours)</h2>
                <table>
                    <tr><th>Company</th><th>Total Transaction Value</th></tr>
        """
        
        for company, value in most_active:
            html_content += f"<tr><td>{company}</td><td>${value:,.0f}</td></tr>"
        
        html_content += """
                </table>
            </div>
            
            <div class="section">
                <h2>Recent Insider Transactions</h2>
                <table>
                    <tr><th>Company</th><th>Insider</th><th>Title</th><th>Type</th><th>Shares</th><th>Price</th><th>Value</th></tr>
        """
        
        for trade in insider_trades:
            html_content += f"""
                <tr>
                    <td>{trade.get('company', 'N/A')}</td>
                    <td>{trade.get('insider_name', 'N/A')}</td>
                    <td>{trade.get('title', 'N/A')}</td>
                    <td>{trade.get('transaction_type', 'N/A')}</td>
                    <td>{trade.get('shares', 0):,.0f}</td>
                    <td>${trade.get('price', 0):.2f}</td>
                    <td>${trade.get('value', 0):,.0f}</td>
                </tr>
            """
        
        html_content += """
                </table>
            </div>
            
            <div class="section">
                <h2>SEC Filings Activity</h2>
                <p>Total SEC filings in last 24 hours: """ + str(len(sec_filings)) + """</p>
                <table>
                    <tr><th>Company</th><th>Form Type</th><th>Filing Date</th></tr>
        """
        
        for filing in sec_filings[:10]:  # Show first 10
            html_content += f"""
                <tr>
                    <td>{filing.get('company', 'N/A')}</td>
                    <td>{filing.get('form', 'N/A')}</td>
                    <td>{filing.get('filing_date', 'N/A')}</td>
                </tr>
            """
        
        html_content += """
                </table>
            </div>
            
            <div class="section">
                <h2>Analysis & Insights</h2>
                <ul>
                    <li><strong>Market Activity:</strong> """ + f"Detected {total_trades} insider transactions in the last 24 hours" + """</li>
                    <li><strong>Transaction Volume:</strong> """ + f"Total value of ${total_value:,.0f} across all transactions" + """</li>
                    <li><strong>Most Active:</strong> """ + (most_active[0][0] if most_active else "No activity detected") + """</li>
                </ul>
            </div>
            
            <div class="section">
                <h2>Charts and Visualizations</h2>
                <p>Interactive charts have been generated and saved separately for detailed analysis.</p>
                <p>Chart files: """ + chart_paths + """</p>
            </div>
            
            <footer style="text-align: center; margin-top: 40px; color: #7f8c8d;">
                <p>Generated by CrowdWisdomTrading AI Agent System</p>
            </footer>
        </body>
        </html>
        """
        
        return html_content