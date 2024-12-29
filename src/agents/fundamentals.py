import os
from dotenv import load_dotenv
from langchain_openai.chat_models import ChatOpenAI
from langchain_core.messages import HumanMessage
from agents.state import AgentState, show_agent_reasoning
import json

# Load environment variables
load_dotenv()

# Initialize the OpenAI model with explicit API key
llm = ChatOpenAI(
    model="gpt-4o-mini",
    openai_api_key=os.getenv("OPENAI_API_KEY"),
    temperature=0
)

##### Fundamental Agent #####
def fundamentals_agent(state: AgentState):
    """Analyzes fundamental data and generates trading signals."""
    show_reasoning = state["metadata"]["show_reasoning"]
    data = state["data"]
    metrics = data["financial_metrics"][0] if data["financial_metrics"] else {}

    # Initialize signals list for different fundamental aspects
    signals = []
    reasoning = {}
    
    # 1. Profitability Analysis
    profitability_score = 0
    roe = metrics.get("return_on_equity", 0)
    net_margin = metrics.get("net_margin", 0)
    operating_margin = metrics.get("operating_margin", 0)
    
    if roe > 0.15:  # Strong ROE above 15%
        profitability_score += 1
    if net_margin > 0.20:  # Healthy profit margins
        profitability_score += 1
    if operating_margin > 0.15:  # Strong operating efficiency
        profitability_score += 1
        
    signals.append('bullish' if profitability_score >= 2 else 'bearish' if profitability_score == 0 else 'neutral')
    reasoning["profitability_signal"] = {
        "signal": signals[0],
        "details": f"ROE: {roe:.2%}, Net Margin: {net_margin:.2%}, Op Margin: {operating_margin:.2%}"
    }
    
    # 2. Growth Analysis
    growth_score = 0
    revenue_growth = metrics.get("revenue_growth", 0)
    earnings_growth = metrics.get("earnings_growth", 0)
    book_value_growth = metrics.get("book_value_growth", 0)
    
    if revenue_growth > 0.10:  # 10% revenue growth
        growth_score += 1
    if earnings_growth > 0.10:  # 10% earnings growth
        growth_score += 1
    if book_value_growth > 0.10:  # 10% book value growth
        growth_score += 1
        
    signals.append('bullish' if growth_score >= 2 else 'bearish' if growth_score == 0 else 'neutral')
    reasoning["growth_signal"] = {
        "signal": signals[1],
        "details": f"Revenue Growth: {revenue_growth:.2%}, Earnings Growth: {earnings_growth:.2%}"
    }
    
    # 3. Financial Health
    health_score = 0
    current_ratio = metrics.get("current_ratio", 0)
    debt_to_equity = metrics.get("debt_to_equity", 0)
    fcf_per_share = metrics.get("free_cash_flow_per_share", 0)
    eps = metrics.get("earnings_per_share", 0)
    
    if current_ratio > 1.5:  # Strong liquidity
        health_score += 1
    if debt_to_equity < 0.5:  # Conservative debt levels
        health_score += 1
    if eps != 0 and fcf_per_share > eps * 0.8:  # Strong FCF conversion
        health_score += 1
        
    signals.append('bullish' if health_score >= 2 else 'bearish' if health_score == 0 else 'neutral')
    reasoning["financial_health_signal"] = {
        "signal": signals[2],
        "details": f"Current Ratio: {current_ratio:.2f}, D/E: {debt_to_equity:.2f}"
    }
    
    # 4. Price to X ratios
    pe_ratio = metrics.get("price_to_earnings_ratio", 0)
    pb_ratio = metrics.get("price_to_book_ratio", 0)
    ps_ratio = metrics.get("price_to_sales_ratio", 0)
    
    price_ratio_score = 0
    if pe_ratio > 0 and pe_ratio < 25:  # Reasonable P/E ratio
        price_ratio_score += 1
    if pb_ratio > 0 and pb_ratio < 3:  # Reasonable P/B ratio
        price_ratio_score += 1
    if ps_ratio > 0 and ps_ratio < 5:  # Reasonable P/S ratio
        price_ratio_score += 1
        
    signals.append('bullish' if price_ratio_score >= 2 else 'bearish' if price_ratio_score == 0 else 'neutral')
    reasoning["price_ratios_signal"] = {
        "signal": signals[3],
        "details": f"P/E: {pe_ratio:.2f}, P/B: {pb_ratio:.2f}, P/S: {ps_ratio:.2f}"
    }
    
    # Determine overall signal
    bullish_signals = signals.count('bullish')
    bearish_signals = signals.count('bearish')
    
    if bullish_signals > bearish_signals:
        overall_signal = 'bullish'
    elif bearish_signals > bullish_signals:
        overall_signal = 'bearish'
    else:
        overall_signal = 'neutral'
    
    # Calculate confidence level
    total_signals = len(signals)
    confidence = max(bullish_signals, bearish_signals) / total_signals
    
    message_content = {
        "signal": overall_signal,
        "confidence": f"{round(confidence * 100)}%",
        "reasoning": reasoning
    }
    
    # Create the fundamental analysis message
    message = HumanMessage(
        content=json.dumps(message_content),
        name="fundamentals_agent",
    )
    
    # Print the reasoning if the flag is set
    if show_reasoning:
        show_agent_reasoning(message_content, "Fundamental Analysis Agent")
    
    return {
        "messages": [message],
        "data": data,
    }