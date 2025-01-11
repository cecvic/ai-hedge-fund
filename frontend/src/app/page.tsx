'use client';

import { useState } from 'react';
import DatePicker from 'react-datepicker';
import "react-datepicker/dist/react-datepicker.css";
import {
  Card,
  Title,
  Text,
  TextInput,
  NumberInput,
  Button,
  MultiSelect,
  MultiSelectItem,
  Grid,
} from '@tremor/react';

const analysts = [
  { value: 'fundamentals', name: 'Fundamentals Analyst' },
  { value: 'technicals', name: 'Technical Analyst' },
  { value: 'sentiment', name: 'Sentiment Analyst' },
  { value: 'valuation', name: 'Valuation Analyst' },
  { value: 'risk', name: 'Risk Manager' },
  { value: 'portfolio', name: 'Portfolio Manager' },
];

export default function Home() {
  const [ticker, setTicker] = useState('');
  const [startDate, setStartDate] = useState<Date | null>(new Date());
  const [endDate, setEndDate] = useState<Date | null>(new Date());
  const [portfolio, setPortfolio] = useState({ cash: 100000 });
  const [selectedAnalysts, setSelectedAnalysts] = useState<string[]>([]);
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState<any>(null);

  const handleAnalyze = async () => {
    if (!startDate || !endDate) return;
    
    setLoading(true);
    try {
      const response = await fetch('/api/analyze', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          ticker,
          startDate: startDate.toISOString().split('T')[0],
          endDate: endDate.toISOString().split('T')[0],
          portfolio,
          selectedAnalysts,
        }),
      });

      const data = await response.json();
      setResult(data);
    } catch (error) {
      console.error('Error:', error);
    } finally {
      setLoading(false);
    }
  };

  return (
    <main className="p-4 md:p-10 mx-auto max-w-7xl">
      <Title>AI Hedge Fund Analysis</Title>
      <Text>Enter your parameters to analyze investment opportunities</Text>

      <Grid numItems={1} numItemsSm={2} numItemsLg={3} className="gap-4 mt-6">
        <Card>
          <Title>Stock Information</Title>
          <TextInput
            className="mt-2"
            placeholder="Enter ticker symbol"
            value={ticker}
            onChange={(e) => setTicker(e.target.value)}
          />
          <div className="mt-4">
            <Text>Start Date</Text>
            <DatePicker
              selected={startDate}
              onChange={(date: Date | null) => setStartDate(date)}
              className="w-full p-2 border rounded"
            />
          </div>
          <div className="mt-4">
            <Text>End Date</Text>
            <DatePicker
              selected={endDate}
              onChange={(date: Date | null) => setEndDate(date)}
              className="w-full p-2 border rounded"
            />
          </div>
        </Card>

        <Card>
          <Title>Portfolio Settings</Title>
          <NumberInput
            className="mt-2"
            placeholder="Initial cash"
            value={portfolio.cash.toString()}
            onValueChange={(value) => setPortfolio({ ...portfolio, cash: Number(value) })}
          />
        </Card>

        <Card>
          <Title>Select Analysts</Title>
          <MultiSelect
            className="mt-2"
            placeholder="Choose analysts"
            value={selectedAnalysts}
            onValueChange={setSelectedAnalysts}
          >
            {analysts.map((analyst) => (
              <MultiSelectItem key={analyst.value} value={analyst.value}>
                {analyst.name}
              </MultiSelectItem>
            ))}
          </MultiSelect>
        </Card>
      </Grid>

      <div className="mt-6">
        <Button
          size="lg"
          onClick={handleAnalyze}
          loading={loading}
          loadingText="Analyzing..."
        >
          Analyze
        </Button>
      </div>

      {result && (
        <Card className="mt-6">
          <Title>Analysis Results</Title>
          <pre className="mt-2 whitespace-pre-wrap">
            {JSON.stringify(result, null, 2)}
          </pre>
        </Card>
      )}
    </main>
  );
}
