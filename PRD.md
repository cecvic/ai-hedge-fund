Project Overview & Requirements

    We have an existing Python-based AI Hedge Fund project that currently contains the core logic for fetching market data, generating trading signals, and running backtests.
    We want to add a modern, professional-looking frontend (similar in style to financial dashboards like Bloomberg) and minimal backend routes to connect the new UI with the existing Python logic.

Tech Stack Choices

    Use Next.js (React) for the frontend.
        The UI should have a polished, data-driven look.
        Leverage a component library or style framework (e.g., Material UI, Tailwind, or Ant Design) for a clean yet finance-oriented design (charts, tables, data cards, etc.).
    For the backend, use a lightweight FastAPI (Python) or Flask service to wrap existing Python code into REST endpoints.
        The backend should expose an endpoint for running the AI Hedge Fund logic and returning results (positions, signals, etc.).
        Another endpoint should trigger backtesting for a given ticker, date range, and initial capital.

Detailed Task Breakdown
A) Backend (FastAPI / Flask)

    Create a new directory (e.g., “server” or “backend”).
    Add a small FastAPI/Flask application that:
        Has routes like “POST /api/run-hedge-fund” to invoke the existing “run_hedge_fund” function in “src/agents.py” with user-specified ticker, start_date, end_date, etc. Return the final JSON outcome.
        Has routes like “POST /api/run-backtest” to invoke “Backtester” from “src/backtester.py,” run it, and return results/performance metrics.
        (Optional) Include a route “GET /api/health” for a basic health check.
    Ensure you can run this backend locally (e.g., “uvicorn main:app --reload” if using FastAPI).

B) Frontend (Next.js + TypeScript)

    Create a new Next.js project (e.g., “npx create-next-app@latest --ts”).
    Directory structure suggestion:
        pages/
            index.tsx (Landing/Dashboard)
            hedge-fund.tsx (Form/Panel to run AI Hedge Fund)
            backtest.tsx (Form/Panel to configure and view backtest results)
        components/ (Charts, form inputs, data grids, etc.)
        styles/ (Any global or theme-based styling)
    Dashboard / Landing Page
        Show a summary of functionality: “Run Hedge Fund” and “Backtest.”
        Possibly an introduction or marketing window describing the AI Hedge Fund.
    Hedge Fund Page
        Provide a form for the user to input a ticker, optional start date, optional end date, etc.
        Button to “Run Hedge Fund,” which calls the backend “/api/run-hedge-fund” endpoint.
        Display the returned signals, recommended action, and confidence in a table or cards.
        Include data visualizations showing the most recent close price, or daily signals if desired.
    Backtest Page
        Provide a form to set ticker, start_date, end_date, initial capital, etc.
        On submission, call “/api/run-backtest” and display performance metrics:
            Final portfolio value
            Net profit/loss
            Basic equity curve (chart)
            Sharpe ratio, max drawdown
        Use a chart library (e.g., Recharts, Chart.js, or Highcharts) to visualize equity curve.
    Styling & Appearance
        Emulate a financial dashboard aesthetic: clean typography, subtle color palette, data-driven design.
        Use card-based or grid-based layouts for signals, portfolio info, or backtest results.
    Integration with Backend
        In Next.js, create API utility functions (e.g., “utils/api.ts”) to make requests to the Python backend.
        For local development, you might run the Python backend on port 8000 and Next.js on port 3000.
    Run Locally
        Document instructions in a README so that one can do:
            “poetry install” or “pip install -r requirements.txt” for the Python backend.
            “uvicorn main:app --reload” to run the backend.
            “npm install” in the Next.js folder, then “npm run dev” to run the frontend.

Additional Considerations

    Include a .env file or some config for the backend to store environment variables (e.g., API keys).
    Make sure that the final solution can be tested end-to-end: user enters ticker details in the Next.js UI, which triggers the backend, runs the AI Hedge Fund logic or backtest, and returns data displayed on a chart or in a table.
    For advanced styling or more professional data layouts, you can adopt a finance-oriented theme or design system.

Deliverables

    A functioning Next.js frontend with the described pages and components.
    A Python-based backend (FastAPI/Flask) exposing the described endpoints for hedge fund runs and backtesting.
    Basic instructions in each folder (frontend and backend) on how to install and run locally on a development server.