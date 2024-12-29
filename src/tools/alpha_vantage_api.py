import os
from typing import Dict, Any, List
import pandas as pd
import requests
from datetime import datetime, timedelta

# Constants
BASE_URL = "https://www.alphavantage.co/query"
ALPHA_VANTAGE_API_KEY = os.getenv("ALPHA_VANTAGE_API_KEY")

def validate_api_key():
    """Validate that the Alpha Vantage API key is set and working."""
    if not ALPHA_VANTAGE_API_KEY:
        raise ValueError(
            "Alpha Vantage API key not found. Please set the ALPHA_VANTAGE_API_KEY environment variable."
        )
    
    # Test the API key with a simple request
    test_url = f"{BASE_URL}/TIME_SERIES_DAILY"
    params = {
        "function": "TIME_SERIES_DAILY",
        "symbol": "AAPL",  # Use AAPL as a test
        "apikey": ALPHA_VANTAGE_API_KEY,
        "outputsize": "compact"
    }
    
    try:
        response = requests.get(test_url, params=params)
        response.raise_for_status()
        data = response.json()
        
        if "Note" in data:
            raise ValueError(f"API Key error: {data['Note']}")
        if "Error Message" in data:
            raise ValueError(f"API Key error: {data['Error Message']}")
            
        return True
    except requests.RequestException as e:
        raise ValueError(f"Failed to validate API key: {str(e)}")
    except ValueError as e:
        raise ValueError(f"Invalid API key: {str(e)}")

# Validate API key on module import
try:
    validate_api_key()
except ValueError as e:
    print(f"\nWarning: {str(e)}")
    print("Some functionality may be limited or unavailable.")

def get_api_key() -> str:
    """Get Alpha Vantage API key from environment variables."""
    api_key = os.environ.get("ALPHA_VANTAGE_API_KEY")
    if not api_key:
        raise ValueError("ALPHA_VANTAGE_API_KEY environment variable is not set")
    return api_key

def get_prices(ticker: str, start_date: str = None, end_date: str = None) -> List[Dict[str, Any]]:
    """Get historical price data from Alpha Vantage."""
    try:
        url = f"{BASE_URL}/TIME_SERIES_DAILY"
        params = {
            "function": "TIME_SERIES_DAILY",
            "symbol": ticker,
            "apikey": ALPHA_VANTAGE_API_KEY,
            "outputsize": "full"
        }
        
        print(f"\nFetching price data for {ticker}...")
        response = requests.get(url, params=params)
        response.raise_for_status()
        
        data = response.json()
        
        # Debug information
        print(f"Response status code: {response.status_code}")
        print(f"Response headers: {response.headers}")
        print("Response keys:", list(data.keys()))
        
        if "Time Series (Daily)" not in data:
            print(f"Error: Unexpected API response format. Data received: {data}")
            if "Note" in data:
                print(f"API Note: {data['Note']}")
            if "Information" in data:
                print(f"API Information: {data['Information']}")
            raise ValueError("Invalid API response format")

        time_series = data["Time Series (Daily)"]
        
        # Convert to list of records
        prices = []
        for date, values in time_series.items():
            if (not start_date or date >= start_date) and (not end_date or date <= end_date):
                prices.append({
                    "date": date,
                    "open": float(values["1. open"]),
                    "high": float(values["2. high"]),
                    "low": float(values["3. low"]),
                    "close": float(values["4. close"]),
                    "volume": int(values["5. volume"])
                })
        
        if not prices:
            print(f"Warning: No price data found for {ticker} between {start_date} and {end_date}")
            return []
            
        print(f"Successfully fetched {len(prices)} price records")
        return sorted(prices, key=lambda x: x["date"])
        
    except requests.RequestException as e:
        print(f"Error fetching price data: {str(e)}")
        if hasattr(e.response, 'text'):
            print(f"Response text: {e.response.text}")
        return []
    except (KeyError, ValueError) as e:
        print(f"Error parsing price data: {str(e)}")
        return []

def get_company_overview(ticker: str) -> Dict[str, Any]:
    """Fetch company overview data from Alpha Vantage."""
    api_key = get_api_key()
    url = f"https://www.alphavantage.co/query?function=OVERVIEW&symbol={ticker}&apikey={api_key}"
    
    response = requests.get(url)
    if response.status_code != 200:
        raise Exception(f"Error fetching data: {response.status_code} - {response.text}")
    
    data = response.json()
    if not data or "Symbol" not in data:
        raise ValueError("No company overview data returned")
    
    return data

def get_income_statement(ticker: str) -> List[Dict[str, Any]]:
    """Fetch income statement data from Alpha Vantage."""
    api_key = get_api_key()
    url = f"https://www.alphavantage.co/query?function=INCOME_STATEMENT&symbol={ticker}&apikey={api_key}"
    
    response = requests.get(url)
    if response.status_code != 200:
        raise Exception(f"Error fetching data: {response.status_code} - {response.text}")
    
    data = response.json()
    annual_reports = data.get("annualReports", [])
    if not annual_reports:
        raise ValueError("No income statement data returned")
    
    return annual_reports

def get_cash_flow(ticker: str) -> List[Dict[str, Any]]:
    """Fetch cash flow statement data from Alpha Vantage."""
    api_key = get_api_key()
    url = f"https://www.alphavantage.co/query?function=CASH_FLOW&symbol={ticker}&apikey={api_key}"
    
    response = requests.get(url)
    if response.status_code != 200:
        raise Exception(f"Error fetching data: {response.status_code} - {response.text}")
    
    data = response.json()
    annual_reports = data.get("annualReports", [])
    if not annual_reports:
        raise ValueError("No cash flow data returned")
    
    return annual_reports

def get_balance_sheet(ticker: str) -> List[Dict[str, Any]]:
    """Fetch balance sheet data from Alpha Vantage."""
    api_key = get_api_key()
    url = f"https://www.alphavantage.co/query?function=BALANCE_SHEET&symbol={ticker}&apikey={api_key}"
    
    response = requests.get(url)
    if response.status_code != 200:
        raise Exception(f"Error fetching data: {response.status_code} - {response.text}")
    
    data = response.json()
    annual_reports = data.get("annualReports", [])
    if not annual_reports:
        raise ValueError("No balance sheet data returned")
    
    return annual_reports

def calculate_financial_metrics(ticker: str) -> Dict[str, Any]:
    """Calculate financial metrics from Alpha Vantage data."""
    overview = get_company_overview(ticker)
    income_stmt = get_income_statement(ticker)
    cash_flow = get_cash_flow(ticker)
    balance_sheet = get_balance_sheet(ticker)
    
    # Get the most recent data
    latest_income = income_stmt[0]
    latest_cash_flow = cash_flow[0]
    latest_balance = balance_sheet[0]
    
    # Calculate growth rates
    if len(income_stmt) > 1:
        prev_net_income = float(income_stmt[1]["netIncome"])
        current_net_income = float(latest_income["netIncome"])
        earnings_growth = (current_net_income - prev_net_income) / abs(prev_net_income) if prev_net_income != 0 else 0
    else:
        earnings_growth = 0
    
    return {
        "market_cap": float(overview.get("MarketCapitalization", 0)),
        "pe_ratio": float(overview.get("PERatio", 0)),
        "peg_ratio": float(overview.get("PEGRatio", 0)),
        "earnings_growth": earnings_growth,
        "profit_margin": float(overview.get("ProfitMargin", 0)),
        "operating_margin": float(overview.get("OperatingMarginTTM", 0)),
        "roa": float(overview.get("ReturnOnAssetsTTM", 0)),
        "roe": float(overview.get("ReturnOnEquityTTM", 0)),
        "revenue": float(latest_income.get("totalRevenue", 0)),
        "revenue_per_share": float(overview.get("RevenuePerShareTTM", 0)),
        "debt_to_equity": float(overview.get("DebtToEquityRatio", 0))
    }

def get_financial_line_items(ticker: str) -> List[Dict[str, Any]]:
    """Get financial line items from Alpha Vantage data."""
    cash_flow = get_cash_flow(ticker)
    income_stmt = get_income_statement(ticker)
    balance_sheet = get_balance_sheet(ticker)
    
    line_items = []
    for i in range(min(len(cash_flow), len(income_stmt), len(balance_sheet))):
        cf = cash_flow[i]
        is_data = income_stmt[i]
        bs = balance_sheet[i]
        
        # Calculate working capital
        current_assets = float(bs.get("totalCurrentAssets", 0))
        current_liabilities = float(bs.get("totalCurrentLiabilities", 0))
        working_capital = current_assets - current_liabilities
        
        line_items.append({
            "fiscal_date": cf["fiscalDateEnding"],
            "free_cash_flow": float(cf.get("operatingCashflow", 0)) - float(cf.get("capitalExpenditures", 0)),
            "net_income": float(is_data.get("netIncome", 0)),
            "depreciation_and_amortization": float(cf.get("depreciation", 0)),
            "capital_expenditure": float(cf.get("capitalExpenditures", 0)),
            "working_capital": working_capital
        })
    
    return line_items 

def get_news_sentiment(ticker: str) -> List[Dict]:
    """Get news sentiment data for a given ticker."""
    try:
        url = f"{BASE_URL}/NEWS_SENTIMENT"
        params = {
            "function": "NEWS_SENTIMENT",
            "tickers": ticker,
            "apikey": ALPHA_VANTAGE_API_KEY,
            "limit": 50  # Limit to 50 most recent news items
        }
        
        response = requests.get(url, params=params)
        response.raise_for_status()  # Raise an error for bad status codes
        
        data = response.json()
        
        if "feed" not in data or not data["feed"]:
            print(f"Warning: No news sentiment data available for {ticker}")
            return []
            
        return data["feed"]
        
    except requests.RequestException as e:
        print(f"Error fetching news sentiment data: {str(e)}")
        return []
    except (KeyError, ValueError) as e:
        print(f"Error parsing news sentiment data: {str(e)}")
        return [] 