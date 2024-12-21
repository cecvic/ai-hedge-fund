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

export default function HedgeFund() {
  const [loading, setLoading] = useState(false);
  const [ticker, setTicker] = useState('');
  const [startDate, setStartDate] = useState('');
  const [endDate, setEndDate] = useState('');
  const [results, setResults] = useState<any>(null);
  const [error, setError] = useState('');

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    setError('');
    setResults(null);

    try {
      const data = await api.runHedgeFund({
        ticker: ticker.toUpperCase(),
        start_date: startDate || undefined,
        end_date: endDate || undefined,
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
        Run Hedge Fund Strategy
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
                    InputLabelProps={{ shrink: true }}
                  />
                  <TextField
                    label="End Date"
                    type="date"
                    value={endDate}
                    onChange={(e) => setEndDate(e.target.value)}
                    InputLabelProps={{ shrink: true }}
                  />
                  <Button
                    variant="contained"
                    type="submit"
                    disabled={loading || !ticker}
                  >
                    {loading ? <CircularProgress size={24} /> : 'Run Strategy'}
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
            <Card>
              <CardContent>
                <Typography variant="h6" gutterBottom>
                  Results
                </Typography>
                <pre style={{ whiteSpace: 'pre-wrap' }}>
                  {JSON.stringify(results, null, 2)}
                </pre>
              </CardContent>
            </Card>
          )}
        </Grid>
      </Grid>
    </Layout>
  );
} 