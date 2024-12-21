import { AppBar, Box, Container, Toolbar, Typography, Button } from '@mui/material';
import Link from 'next/link';
import { ReactNode } from 'react';

interface LayoutProps {
  children: ReactNode;
}

export default function Layout({ children }: LayoutProps) {
  return (
    <Box sx={{ display: 'flex', flexDirection: 'column', minHeight: '100vh' }}>
      <AppBar position="static" sx={{ backgroundColor: '#1a237e' }}>
        <Toolbar>
          <Typography variant="h6" component="div" sx={{ flexGrow: 1 }}>
            AI Hedge Fund
          </Typography>
          <Link href="/" passHref>
            <Button color="inherit">Dashboard</Button>
          </Link>
          <Link href="/hedge-fund" passHref>
            <Button color="inherit">Hedge Fund</Button>
          </Link>
          <Link href="/backtest" passHref>
            <Button color="inherit">Backtest</Button>
          </Link>
        </Toolbar>
      </AppBar>
      <Container component="main" sx={{ mt: 4, mb: 4, flex: 1 }}>
        {children}
      </Container>
      <Box component="footer" sx={{ py: 3, px: 2, mt: 'auto', backgroundColor: '#f5f5f5' }}>
        <Container maxWidth="sm">
          <Typography variant="body2" color="text.secondary" align="center">
            © {new Date().getFullYear()} AI Hedge Fund
          </Typography>
        </Container>
      </Box>
    </Box>
  );
} 