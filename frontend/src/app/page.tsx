'use client';

import Layout from '@/components/Layout';
import { Box, Card, CardContent, Grid, Typography } from '@mui/material';

export default function Home() {
  return (
    <Layout>
      <Box sx={{ mb: 4 }}>
        <Typography variant="h4" component="h1" gutterBottom>
          Welcome to AI Hedge Fund
        </Typography>
        <Typography variant="subtitle1" color="text.secondary" gutterBottom>
          Advanced algorithmic trading powered by artificial intelligence
        </Typography>
      </Box>

      <Grid container spacing={3}>
        <Grid item xs={12} md={6}>
          <Card>
            <CardContent>
              <Typography variant="h6" gutterBottom>
                Hedge Fund Strategy
              </Typography>
              <Typography variant="body2" color="text.secondary">
                Run our AI-powered hedge fund strategy on any ticker. Get real-time signals and confidence scores for optimal trading decisions.
              </Typography>
            </CardContent>
          </Card>
        </Grid>

        <Grid item xs={12} md={6}>
          <Card>
            <CardContent>
              <Typography variant="h6" gutterBottom>
                Backtest Performance
              </Typography>
              <Typography variant="body2" color="text.secondary">
                Evaluate strategy performance with comprehensive backtesting. Analyze key metrics including Sharpe ratio, max drawdown, and equity curves.
              </Typography>
            </CardContent>
          </Card>
        </Grid>
      </Grid>
    </Layout>
  );
}
