import json
import pandas as pd
from datetime import datetime, timedelta
from typing import Dict, List, Any
from pathlib import Path
import requests
from utils.logger import setup_logger

logger = setup_logger(__name__)

def validate_json_data(data: str) -> bool:
    """Validate if string contains valid JSON"""
    try:
        json.loads(data)
        return True
    except (json.JSONDecodeError, TypeError):
        return False

def clean_company_name(name: str) -> str:
    """Clean and standardize company names"""
    if not name:
        return "Unknown"
    
    # Remove common suffixes and clean
    suffixes = [" Inc.", " Corp.", " Corporation", " LLC", " Ltd.", " LP"]
    cleaned = name.strip()
    
    for suffix in suffixes:
        if cleaned.endswith(suffix):
            cleaned = cleaned[:-len(suffix)]
    
    return cleaned.strip()

def calculate_percentage_change(current: float, previous: float) -> float:
    """Calculate percentage change between two values"""
    if previous == 0:
        return 0.0
    return ((current - previous) / previous) * 100

def format_currency(amount: float) -> str:
    """Format currency with appropriate suffixes"""
    if amount >= 1_000_000_000:
        return f"${amount/1_000_000_000:.1f}B"
    elif amount >= 1_000_000:
        return f"${amount/1_000_000:.1f}M"
    elif amount >= 1_000:
        return f"${amount/1_000:.1f}K"
    else:
        return f"${amount:.2f}"

def get_trading_day_range(days_back: int = 7) -> tuple:
    """Get trading day range excluding weekends"""
    end_date = datetime.now()
    start_date = end_date - timedelta(days=days_back)
    
    # Adjust for weekends
    while start_date.weekday() >= 5:  # 5=Saturday, 6=Sunday
        start_date -= timedelta(days=1)
    
    while end_date.weekday() >= 5:
        end_date -= timedelta(days=1)
    
    return start_date, end_date

def ensure_directory_exists(path: Path) -> None:
    """Ensure directory exists, create if not"""
    path.mkdir(parents=True, exist_ok=True)