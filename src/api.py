from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Dict, Optional
from datetime import datetime
from main import run_hedge_fund

app = FastAPI()

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class AnalysisRequest(BaseModel):
    ticker: str
    start_date: str
    end_date: str
    portfolio: Dict[str, float]
    selected_analysts: Optional[List[str]] = None

@app.post("/analyze")
async def analyze_investment(request: AnalysisRequest):
    try:
        # Convert string dates to datetime objects
        start_date = datetime.strptime(request.start_date, "%Y-%m-%d")
        end_date = datetime.strptime(request.end_date, "%Y-%m-%d")

        # Run the hedge fund analysis
        result = run_hedge_fund(
            ticker=request.ticker,
            start_date=request.start_date,
            end_date=request.end_date,
            portfolio=request.portfolio,
            selected_analysts=request.selected_analysts
        )

        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000) 