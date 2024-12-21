import axios from 'axios';

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

export interface HedgeFundRequest {
  ticker: string;
  start_date?: string;
  end_date?: string;
}

export interface BacktestRequest {
  ticker: string;
  start_date: string;
  end_date: string;
  initial_capital?: number;
}

export const api = {
  async healthCheck() {
    const response = await axios.get(`${API_BASE_URL}/api/health`);
    return response.data;
  },

  async runHedgeFund(data: HedgeFundRequest) {
    const response = await axios.post(`${API_BASE_URL}/api/run-hedge-fund`, data);
    return response.data;
  },

  async runBacktest(data: BacktestRequest) {
    const response = await axios.post(`${API_BASE_URL}/api/run-backtest`, data);
    return response.data;
  }
}; 