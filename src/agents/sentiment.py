import os
from dotenv import load_dotenv
from langchain_openai.chat_models import ChatOpenAI
import pandas as pd
import numpy as np
from agents.state import AgentState, show_agent_reasoning
from tools.alpha_vantage_api import get_news_sentiment
import json
from langchain.schema import HumanMessage

# Load environment variables
load_dotenv()

# Initialize the OpenAI model with explicit API key
llm = ChatOpenAI(
    model="gpt-4o-mini",
    openai_api_key=os.getenv("OPENAI_API_KEY"),
    temperature=0
)

def sentiment_agent(state: AgentState):
    """Analyzes market sentiment and generates trading signals."""
    data = state["data"]
    show_reasoning = state["metadata"]["show_reasoning"]

    try:
        # Get news sentiment data
        news_items = get_news_sentiment(data["ticker"])
    except ValueError:
        # Handle case where no news data is available
        message_content = {
            "signal": "neutral",
            "confidence": "0%",
            "reasoning": {
                "signal_distribution": {
                    "bullish": 0,
                    "bearish": 0,
                    "neutral": 1
                },
                "recent_articles": [],
                "average_sentiment_score": 0,
                "error": "No news sentiment data available"
            }
        }

        if show_reasoning:
            show_agent_reasoning(message_content, "Sentiment Analysis Agent")

        return {
            "messages": [HumanMessage(
                content=json.dumps(message_content),
                name="sentiment_agent"
            )],
            "data": data
        }
    
    # Extract sentiment scores and labels
    sentiment_scores = pd.Series([item['sentiment_score'] for item in news_items])
    sentiment_labels = pd.Series([item['sentiment_label'] for item in news_items])
    
    # Convert sentiment labels to signals
    signals = []
    for score in sentiment_scores:
        if score > 0.25:  # Significantly positive
            signals.append("bullish")
        elif score < -0.25:  # Significantly negative
            signals.append("bearish")
        else:
            signals.append("neutral")
    
    # Determine overall signal
    bullish_signals = signals.count("bullish")
    bearish_signals = signals.count("bearish")
    neutral_signals = signals.count("neutral")
    
    if bullish_signals > bearish_signals and bullish_signals > neutral_signals:
        overall_signal = "bullish"
    elif bearish_signals > bullish_signals and bearish_signals > neutral_signals:
        overall_signal = "bearish"
    else:
        overall_signal = "neutral"

    # Calculate confidence level based on the proportion of indicators agreeing
    total_signals = len(signals)
    max_signals = max(bullish_signals, bearish_signals, neutral_signals)
    confidence = max_signals / total_signals if total_signals > 0 else 0

    # Prepare detailed reasoning
    recent_articles = [
        {
            "title": item["title"],
            "sentiment": item["sentiment_label"],
            "score": item["sentiment_score"]
        }
        for item in news_items[:5]  # Show 5 most recent articles
    ]

    message_content = {
        "signal": overall_signal,
        "confidence": f"{round(confidence * 100)}%",
        "reasoning": {
            "signal_distribution": {
                "bullish": bullish_signals,
                "bearish": bearish_signals,
                "neutral": neutral_signals
            },
            "recent_articles": recent_articles,
            "average_sentiment_score": float(sentiment_scores.mean())
        }
    }

    if show_reasoning:
        print("\nSentiment Analysis:")
        print(f"Signal: {overall_signal} (Confidence: {message_content['confidence']})")
        print("\nSignal Distribution:")
        print(f"Bullish: {bullish_signals}")
        print(f"Bearish: {bearish_signals}")
        print(f"Neutral: {neutral_signals}")
        print(f"\nAverage Sentiment Score: {sentiment_scores.mean():.3f}")
        print("\nRecent Articles:")
        for article in recent_articles:
            print(f"- {article['title']} (Sentiment: {article['sentiment']}, Score: {article['score']:.3f})")

    return {
        "messages": [HumanMessage(
            content=json.dumps(message_content),
            name="sentiment_agent"
        )],
        "data": data
    }
