# AI Hedge Fund

A modern web application for running AI-powered hedge fund strategies and backtesting.

## Project Structure

```
.
├── backend/           # FastAPI backend
│   ├── app/          # API routes and application code
│   └── requirements.txt
├── frontend/         # Next.js frontend
├── src/             # Core Python hedge fund logic
└── README.md
```

## Setup & Installation

### Backend (FastAPI)

1. Create a Python virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

2. Install dependencies:
   ```bash
   cd backend
   pip install -r requirements.txt
   ```

3. Run the backend server:
   ```bash
   cd app
   uvicorn main:app --reload
   ```

The backend will be available at http://localhost:8000

### Frontend (Next.js)

1. Install Node.js dependencies:
   ```bash
   cd frontend
   npm install
   ```

2. Run the development server:
   ```bash
   npm run dev
   ```

The frontend will be available at http://localhost:3000

## Features

- Run AI hedge fund strategy on any ticker
- Backtest strategy performance with customizable parameters
- Interactive charts and performance metrics
- Modern, responsive UI with Material Design

## Development

- Backend API documentation available at http://localhost:8000/docs
- Frontend uses Material UI components and Recharts for data visualization
- TypeScript for type safety in the frontend
- FastAPI for high-performance backend API
