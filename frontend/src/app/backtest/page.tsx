'use client';

import { useState } from 'react';
import Layout from '@/components/Layout';
import { api } from '@/utils/api';
import {
  Box,
  Button,
  Card,
  CardContent,
  CircularProgress,
  Grid,
  TextField,
  Typography,
} from '@mui/material';
import {
  LineChart,
  Line,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer,
} from 'recharts';

interface BacktestResults {
  final_value: number;
  net_profit: number;
  sharpe_ratio: number;
  max_drawdown: number;
  equity_curve: { date: string; value: number }[];
}

export default function Backtest() {
  const [loading, setLoading] = useState(false);
  const [ticker, setTicker] = useState('');
  const [startDate, setStartDate] = useState('');
  const [endDate, setEndDate] = useState('');
  const [initialCapital, setInitialCapital] = useState('100000');
  const [results, setResults] = useState<BacktestResults | null>(null);
  const [error, setError] = useState('');

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    setError('');
    setResults(null);

    try {
      const data = await api.runBacktest({
        ticker: ticker.toUpperCase(),
        start_date: startDate,
        end_date: endDate,
        initial_capital: Number(initialCapital),
      });
      setResults(data);
    } catch (err: any) {
      setError(err.response?.data?.detail || 'An error occurred');
    } finally {
      setLoading(false);
    }
  };

  return (
    <Layout>
      <Typography variant="h4" gutterBottom>
        Backtest Strategy
      </Typography>

      <Grid container spacing={3}>
        <Grid item xs={12} md={6}>
          <Card>
            <CardContent>
              <form onSubmit={handleSubmit}>
                <Box sx={{ display: 'flex', flexDirection: 'column', gap: 2 }}>
                  <TextField
                    label="Ticker Symbol"
                    value={ticker}
                    onChange={(e) => setTicker(e.target.value)}
                    required
                  />
                  <TextField
                    label="Start Date"
                    type="date"
                    value={startDate}
                    onChange={(e) => setStartDate(e.target.value)}
                    required
                    InputLabelProps={{ shrink: true }}
                  />
                  <TextField
                    label="End Date"
                    type="date"
                    value={endDate}
                    onChange={(e) => setEndDate(e.target.value)}
                    required
                    InputLabelProps={{ shrink: true }}
                  />
                  <TextField
                    label="Initial Capital"
                    type="number"
                    value={initialCapital}
                    onChange={(e) => setInitialCapital(e.target.value)}
                    required
                  />
                  <Button
                    variant="contained"
                    type="submit"
                    disabled={loading || !ticker || !startDate || !endDate}
                  >
                    {loading ? <CircularProgress size={24} /> : 'Run Backtest'}
                  </Button>
                </Box>
              </form>
            </CardContent>
          </Card>
        </Grid>

        <Grid item xs={12} md={6}>
          {error && (
            <Typography color="error" gutterBottom>
              {error}
            </Typography>
          )}
          
          {results && (
            <>
              <Card sx={{ mb: 2 }}>
                <CardContent>
                  <Grid container spacing={2}>
                    <Grid item xs={6}>
                      <Typography variant="subtitle2" color="text.secondary">
                        Final Value
                      </Typography>
                      <Typography variant="h6">
                        ${results.final_value.toLocaleString()}
                      </Typography>
                    </Grid>
                    <Grid item xs={6}>
                      <Typography variant="subtitle2" color="text.secondary">
                        Net Profit
                      </Typography>
                      <Typography variant="h6" color={results.net_profit >= 0 ? 'success.main' : 'error.main'}>
                        ${results.net_profit.toLocaleString()}
                      </Typography>
                    </Grid>
                    <Grid item xs={6}>
                      <Typography variant="subtitle2" color="text.secondary">
                        Sharpe Ratio
                      </Typography>
                      <Typography variant="h6">
                        {results.sharpe_ratio.toFixed(2)}
                      </Typography>
                    </Grid>
                    <Grid item xs={6}>
                      <Typography variant="subtitle2" color="text.secondary">
                        Max Drawdown
                      </Typography>
                      <Typography variant="h6" color="error.main">
                        {(results.max_drawdown * 100).toFixed(2)}%
                      </Typography>
                    </Grid>
                  </Grid>
                </CardContent>
              </Card>

              <Card>
                <CardContent>
                  <Typography variant="h6" gutterBottom>
                    Equity Curve
                  </Typography>
                  <Box sx={{ height: 300 }}>
                    <ResponsiveContainer width="100%" height="100%">
                      <LineChart data={results.equity_curve}>
                        <CartesianGrid strokeDasharray="3 3" />
                        <XAxis dataKey="date" />
                        <YAxis />
                        <Tooltip />
                        <Line
                          type="monotone"
                          dataKey="value"
                          stroke="#1a237e"
                          dot={false}
                        />
                      </LineChart>
                    </ResponsiveContainer>
                  </Box>
                </CardContent>
              </Card>
            </>
          )}
        </Grid>
      </Grid>
    </Layout>
  );
} 