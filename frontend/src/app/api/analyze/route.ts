import { NextRequest, NextResponse } from 'next/server';
import axios from 'axios';

export const runtime = 'edge';

export async function POST(req: NextRequest) {
  try {
    const { ticker, startDate, endDate, portfolio, selectedAnalysts } = await req.json();

    // Call Python backend
    const response = await axios.post('http://localhost:8000/analyze', {
      ticker,
      start_date: startDate,
      end_date: endDate,
      portfolio,
      selected_analysts: selectedAnalysts,
    });

    return NextResponse.json(response.data);
  } catch (error) {
    console.error('Error:', error);
    return NextResponse.json(
      { error: 'Failed to process request' },
      { status: 500 }
    );
  }
} 