from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from datetime import datetime
import sys
from pathlib import Path

# Add src to Python path
sys.path.append(str(Path(__file__).parent.parent.parent / "src"))

from agents import run_hedge_fund
from backtester import Backtester

app = FastAPI(title="AI Hedge Fund API")

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Next.js frontend
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class HedgeFundRequest(BaseModel):
    ticker: str
    start_date: datetime | None = None
    end_date: datetime | None = None

class BacktestRequest(BaseModel):
    ticker: str
    start_date: datetime
    end_date: datetime
    initial_capital: float = 100000.0

@app.get("/api/health")
async def health_check():
    return {"status": "healthy"}

@app.post("/api/run-hedge-fund")
async def run_ai_hedge_fund(request: HedgeFundRequest):
    try:
        result = run_hedge_fund(
            ticker=request.ticker,
            start_date=request.start_date,
            end_date=request.end_date
        )
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/run-backtest")
async def run_backtest(request: BacktestRequest):
    try:
        backtester = Backtester(
            ticker=request.ticker,
            initial_capital=request.initial_capital
        )
        results = backtester.run(
            start_date=request.start_date,
            end_date=request.end_date
        )
        return {
            "final_value": results.get("final_value"),
            "net_profit": results.get("net_profit"),
            "sharpe_ratio": results.get("sharpe_ratio"),
            "max_drawdown": results.get("max_drawdown"),
            "equity_curve": results.get("equity_curve")
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) 