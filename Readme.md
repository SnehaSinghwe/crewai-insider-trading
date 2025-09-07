# CrowdWisdomTrading AI Agent - Insider Trading Analysis

## Overview

This project implements a comprehensive insider trading analysis system using CrewAI framework. The system retrieves SEC filings data, analyzes insider trading activities, generates comparative visualizations, and produces detailed reports.

## Features

- **SEC Data Retrieval**: Automated fetching of SEC filings from the last 24 hours or around 
- **Insider Trading Analysis**: Analysis of Form 4 filings and insider transactions
- **Data Visualization**: Interactive charts comparing current and historical data
- **Comprehensive Reports**: HTML reports with insights and actionable intelligence
- **CrewAI Flow Integration**: Structured agent workflow with guardrails
- **Error Handling & Logging**: Robust error handling with comprehensive logging
- **Data Storage**: SQLite database for historical data tracking

## Project Structure

```
crewai-insider-trading/
├── main.py                     # Main execution script
├── requirements.txt            # Dependencies
├── .env.example               # Environment variables template
├── config/
│   ├── __init__.py
│   └── settings.py            # Configuration settings
├── agents/                    # CrewAI agents
├── tools/                     # Custom tools
├── flows/                     # CrewAI flows
├── data/                      # Data storage utilities
├── utils/                     # Utility functions
├── output/
│   ├── reports/               # Generated reports
│   └── charts/                # Generated charts
└── README.md
```

## Installation & Setup

### 1. Clone the Repository
```bash
git clone <repository-url>
cd crewai-insider-trading
```

### 2. Create Virtual Environment
```bash
python -m venv crewai_env
source crewai_env/bin/activate  # On Windows: crewai_env\Scripts\activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Environment Configuration
```bash
cp .env.example .env
# Edit .env file with your API keys and configuration
```

Required environment variables:
- `OPENAI_API_KEY`: Your OpenAI API key
- `SEC_USER_AGENT`: Your email address for SEC API requests
- `LITELLM_MODEL`: LLM model to use (default: gpt-4o-mini)

### 5. Run the Application
```bash
python main.py
```

## Architecture

### Agent Design
- **SEC Data Agent**: Retrieves SEC filing data
- **Insider Trading Agent**: Analyzes insider trading activities
- **Comparison Agent**: Creates data visualizations and comparisons
- **Report Agent**: Generates comprehensive reports

### Tools
- **SEC Tools**: Interface with SEC EDGAR database
- **Chart Tools**: Generate interactive visualizations using Plotly
- **Report Tools**: Create HTML reports with embedded analysis

### Flow
The CrewAI Flow orchestrates the entire process with proper guardrails and error handling.

## Usage

### Basic Usage
```bash
python main.py
```

### Output Files
- **Reports**: `output/reports/insider_trading_report_YYYYMMDD_HHMMSS.html`
- **Charts**: `output/charts/*.html`
- **Logs**: `logs_YYYYMMDD.log`

## Sample Input/Output

### Input
The system automatically retrieves data from SEC sources - no manual input required.

### Output Example
```json
{
        "rank": 1,
        "date": "2025-09-06",
        "company_ticker": "NVDA",
        "company_name": "NVIDIA Corporation",
        "insider_name": "Jensen Huang",
        "insider_title": "Chief Executive Officer",
        "transaction_type": "Sale",
        "shares": 1200000,
        "price_per_share": 1127.89,
        "total_value": 1353468000,
        "form_type": "4",
        "filing_date": "2025-09-06",
        "ownership_percentage_before": 3.2,
        "ownership_percentage_after": 2.8,
        "anomaly_score": 9.2,
        "market_context": {
          "stock_performance_30d": -8.3,
          "sector_performance_30d": -12.1,
          "earnings_announcement_days_away": 45,
          "recent_news_sentiment": "neutral"
        }
```

## Advanced Features

### RAG Integration
The system can be extended to include YouTube videos and other content sources in the RAG system for enhanced analysis.

### Multi-modal Processing
Capability to process images and charts using multi-modal models when relevant visual content is detected.

### Historical Comparison
Built-in comparison with previous weeks' data to identify trends and anomalies.

## Error Handling & Logging

- Comprehensive logging with color-coded console output
- File-based logging with rotation
- Graceful error handling with retry mechanisms
- User-friendly error messages

## Development Tools

Recommended development tools:
- Cursor.com for AI-assisted coding
- Windsurf for enhanced development environment

## API Rate Limiting

The system implements proper rate limiting for SEC API requests to comply with their usage policies.

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## License

This project is developed for CrowdWisdomTrading internship assessment.

---

**Note**: This system is designed for educational and analysis purposes. Always consult with financial professionals before making investment decisions based on insider trading data.
```

## Installation & Running Instructions

### 1. **Setup Steps**
```bash
# Create directory
mkdir crewai-insider-trading
cd crewai-insider-trading

# Create virtual environment
python -m venv crewai_env
source crewai_env/bin/activate  # On Windows: crewai_env\Scripts\activate

# Install requirements
pip install -r requirements.txt
```

### 2. **Environment Configuration**
Create `.env` file:
```env
OPENAI_API_KEY=your_openai_api_key_here
SEC_USER_AGENT=your_email@example.com
LITELLM_MODEL=gpt-4o-mini
LOG_LEVEL=INFO
```

### 3. **Run the Application**
```bash
python main.py
```

## Key Features Implemented

✅ **CrewAI Flow with Guardrails**: Structured flow with proper error handling
✅ **SEC Data Retrieval**: Last 24 hours SEC filings
✅ **Insider Trading Analysis**: Form 4 processing and analysis  
✅ **Interactive Charts**: Plotly-based visualizations
✅ **Comprehensive Reports**: HTML reports with embedded analysis
✅ **Proper Agent Design**: Single-responsibility agents
✅ **LiteLLM Integration**: Flexible LLM provider support
✅ **Error Handling & Logging**: Robust logging with color output
✅ **Data Storage**: SQLite for historical data
✅ **Chart Comparisons**: Current vs historical data visualization
