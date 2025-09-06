import json
import sqlite3
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Any, Optional
from utils.logger import setup_logger
from config.settings import settings

logger = setup_logger(__name__)

class DataStorage:
    """Handle data storage and retrieval"""
    
    def __init__(self):
        self.db_path = settings.DATA_DIR / "insider_trading.db"
        self.init_database()
    
    def init_database(self):
        """Initialize SQLite database"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                # SEC Filings table
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS sec_filings (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        cik TEXT,
                        company_name TEXT,
                        form_type TEXT,
                        filing_date TEXT,
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                    )
                """)
                
                # Insider Trading table
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS insider_trades (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        company_name TEXT,
                        ticker TEXT,
                        insider_name TEXT,
                        insider_title TEXT,
                        transaction_date TEXT,
                        transaction_type TEXT,
                        shares INTEGER,
                        price REAL,
                        value REAL,
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                    )
                """)
                
                # Reports table
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS reports (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        report_path TEXT,
                        report_type TEXT,
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                    )
                """)
                
                conn.commit()
                logger.info("Database initialized successfully")
                
        except Exception as e:
            logger.error(f"Error initializing database: {e}")
    
    def save_sec_filings(self, filings: List[Dict[str, Any]]) -> bool:
        """Save SEC filings to database"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                for filing in filings:
                    cursor.execute("""
                        INSERT INTO sec_filings (cik, company_name, form_type, filing_date)
                        VALUES (?, ?, ?, ?)
                    """, (
                        filing.get('cik'),
                        filing.get('company'),
                        filing.get('form'),
                        filing.get('filing_date')
                    ))
                
                conn.commit()
                logger.info(f"Saved {len(filings)} SEC filings")
                return True
                
        except Exception as e:
            logger.error(f"Error saving SEC filings: {e}")
            return False
    
    def save_insider_trades(self, trades: List[Dict[str, Any]]) -> bool:
        """Save insider trades to database"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                for trade in trades:
                    cursor.execute("""
                        INSERT INTO insider_trades 
                        (company_name, ticker, insider_name, insider_title, 
                         transaction_date, transaction_type, shares, price, value)
                        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                    """, (
                        trade.get('company'),
                        trade.get('ticker'),
                        trade.get('insider_name'),
                        trade.get('title'),
                        trade.get('transaction_date'),
                        trade.get('transaction_type'),
                        trade.get('shares'),
                        trade.get('price'),
                        trade.get('value')
                    ))
                
                conn.commit()
                logger.info(f"Saved {len(trades)} insider trades")
                return True
                
        except Exception as e:
            logger.error(f"Error saving insider trades: {e}")
            return False
    
    def get_historical_trades(self, days_back: int = 7) -> List[Dict[str, Any]]:
        """Retrieve historical insider trades"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                cursor.execute("""
                    SELECT * FROM insider_trades 
                    WHERE created_at >= datetime('now', '-{} days')
                    ORDER BY created_at DESC
                """.format(days_back))
                
                columns = [description[0] for description in cursor.description]
                trades = [dict(zip(columns, row)) for row in cursor.fetchall()]
                
                logger.info(f"Retrieved {len(trades)} historical trades")
                return trades
                
        except Exception as e:
            logger.error(f"Error retrieving historical trades: {e}")
            return []