import os
from dotenv import load_dotenv
from langchain_openai.chat_models import ChatOpenAI
from datetime import datetime
from agents.state import AgentState
from tools.alpha_vantage_api import (
    get_prices,
    calculate_financial_metrics,
    get_financial_line_items
)

# Load environment variables
load_dotenv()

# Initialize the OpenAI model with explicit API key
llm = ChatOpenAI(
    model="gpt-4o-mini",
    openai_api_key=os.getenv("OPENAI_API_KEY"),
    temperature=0
)

def market_data_agent(state: AgentState):
    """Responsible for gathering and preprocessing market data"""
    messages = state["messages"]
    data = state["data"]

    # Set default dates
    end_date = data["end_date"] or datetime.now().strftime('%Y-%m-%d')
    if not data["start_date"]:
        # Calculate 3 months before end_date
        end_date_obj = datetime.strptime(end_date, '%Y-%m-%d')
        start_date = end_date_obj.replace(month=end_date_obj.month - 3) if end_date_obj.month > 3 else \
            end_date_obj.replace(year=end_date_obj.year - 1, month=end_date_obj.month + 9)
        start_date = start_date.strftime('%Y-%m-%d')
    else:
        start_date = data["start_date"]

    # Get the historical price data
    prices = get_prices(
        ticker=data["ticker"], 
        start_date=start_date, 
        end_date=end_date,
    )

    # Get the financial metrics
    financial_metrics = [calculate_financial_metrics(data["ticker"])]

    # Get the financial line items (last 2 periods for comparison)
    financial_line_items = get_financial_line_items(data["ticker"])[:2]

    # Note: Alpha Vantage doesn't provide insider trades data, so we'll remove that
    # from the response. The sentiment agent will need to be updated to use
    # alternative data sources for sentiment analysis.

    return {
        "messages": messages,
        "data": {
            **data, 
            "prices": prices, 
            "start_date": start_date, 
            "end_date": end_date,
            "financial_metrics": financial_metrics,
            "financial_line_items": financial_line_items,
            "market_cap": financial_metrics[0]["market_cap"] if financial_metrics else None,
        }
    }