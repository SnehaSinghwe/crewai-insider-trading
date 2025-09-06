import matplotlib.pyplot as plt
import seaborn as sns
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
from datetime import datetime, timedelta
from typing import Dict, List
from crewai_tools import BaseTool
import json
from pathlib import Path
from utils.logger import setup_logger
from config.settings import settings

logger = setup_logger(__name__)

class ChartGenerationTool(BaseTool):
    name: str = "Chart Generation Tool"
    description: str = "Creates charts comparing current and historical insider trading data"
    
    def _run(self, current_data: str, historical_data: str = None) -> str:
        """Generate comparison charts for insider trading data"""
        try:
            current_trades = json.loads(current_data)
            
            if not current_trades:
                return "No current data available for chart generation"
            
            # Create DataFrame
            df = pd.DataFrame(current_trades)
            
            # Generate multiple chart types
            charts_created = []
            
            # 1. Trading Volume by Company
            if 'company' in df.columns and 'shares' in df.columns:
                fig1 = self._create_volume_chart(df)
                chart1_path = settings.CHARTS_DIR / f"trading_volume_{datetime.now().strftime('%Y%m%d_%H%M%S')}.html"
                fig1.write_html(str(chart1_path))
                charts_created.append(str(chart1_path))
            
            # 2. Transaction Value Distribution
            if 'value' in df.columns:
                fig2 = self._create_value_distribution_chart(df)
                chart2_path = settings.CHARTS_DIR / f"value_distribution_{datetime.now().strftime('%Y%m%d_%H%M%S')}.html"
                fig2.write_html(str(chart2_path))
                charts_created.append(str(chart2_path))
            
            # 3. Transaction Types Pie Chart
            if 'transaction_type' in df.columns:
                fig3 = self._create_transaction_type_chart(df)
                chart3_path = settings.CHARTS_DIR / f"transaction_types_{datetime.now().strftime('%Y%m%d_%H%M%S')}.html"
                fig3.write_html(str(chart3_path))
                charts_created.append(str(chart3_path))
            
            logger.info(f"Created {len(charts_created)} charts")
            return f"Charts created successfully: {', '.join(charts_created)}"
            
        except Exception as e:
            logger.error(f"Error creating charts: {e}")
            return f"Error creating charts: {str(e)}"
    
    def _create_volume_chart(self, df: pd.DataFrame):
        """Create trading volume chart"""
        volume_by_company = df.groupby('company')['shares'].sum().sort_values(ascending=False)
        
        fig = go.Figure(data=[
            go.Bar(
                x=volume_by_company.values,
                y=volume_by_company.index,
                orientation='h',
                marker_color='skyblue'
            )
        ])
        
        fig.update_layout(
            title='Insider Trading Volume by Company (Last 24 Hours)',
            xaxis_title='Number of Shares',
            yaxis_title='Company',
            height=600
        )
        
        return fig
    
    def _create_value_distribution_chart(self, df: pd.DataFrame):
        """Create transaction value distribution chart"""
        fig = px.histogram(
            df, 
            x='value', 
            nbins=20,
            title='Distribution of Transaction Values (Last 24 Hours)',
            labels={'value': 'Transaction Value ($)', 'count': 'Number of Transactions'}
        )
        
        return fig
    
    def _create_transaction_type_chart(self, df: pd.DataFrame):
        """Create transaction type pie chart"""
        type_counts = df['transaction_type'].value_counts()
        
        fig = go.Figure(data=[
            go.Pie(
                labels=type_counts.index,
                values=type_counts.values,
                hole=0.3
            )
        ])
        
        fig.update_layout(
            title='Transaction Types Distribution (Last 24 Hours)'
        )
        
        return fig