"""
Fetch historical price data for Nifty 500 stocks
"""

import pandas as pd
import yfinance as yf
from fetch_nifty500 import get_nifty500_tickers
import os
import time


def fetch_stock_data(ticker, start_date='2000-01-01', end_date='2025-12-31'):
    """
    Fetch historical data for a single stock.
    """
    try:
        print(f"  Downloading {ticker}...", end=' ')
        
        stock = yf.Ticker(ticker)
        data = stock.history(start=start_date, end=end_date)
        
        if data.empty:
            print("❌ No data found")
            return None
        
        print(f"✓ Got {len(data)} rows")
        return data
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return None


def save_stock_data(data, ticker, output_dir='data/stocks'):
    """
    Save stock data to a CSV file.
    """
    os.makedirs(output_dir, exist_ok=True)
    
    filename = f"{ticker.replace('.', '_')}.csv"
    filepath = os.path.join(output_dir, filename)
    
    data.to_csv(filepath)
    print(f"  Saved to {filepath}")


def fetch_all_stocks(start_date='2000-01-01', end_date='2025-12-31', delay=0.5):
    """
    Fetch historical data for all Nifty 500 stocks.
    """
    print("=" * 70)
    print("Fetching Historical Data for Nifty 500 Stocks")
    print("=" * 70)
    
    print("\nLoading stock list...")
    stocks_df = get_nifty500_tickers()
    total_stocks = len(stocks_df)
    
    print(f"\nFound {total_stocks} stocks to download")
    print(f"Date range: {start_date} to {end_date}")
    print("\nStarting downloads...\n")
    
    successful = []
    failed = []
    
    for idx, row in stocks_df.iterrows():
        ticker = row['Ticker']
        company = row['Company']
        
        print(f"[{idx + 1}/{total_stocks}] {company} ({ticker})")
        
        data = fetch_stock_data(ticker, start_date, end_date)
        
        if data is not None and not data.empty:
            save_stock_data(data, ticker)
            successful.append(ticker)
        else:
            failed.append(ticker)
        
        if idx < total_stocks - 1:
            time.sleep(delay)
    
    print("\n" + "=" * 70)
    print("Download Complete!")
    print("=" * 70)
    print(f"✓ Successful: {len(successful)} stocks")
    print(f"✗ Failed: {len(failed)} stocks")
    
    if failed:
        print(f"\nFailed tickers: {', '.join(failed)}")
    
    return {
        'successful': successful,
        'failed': failed,
        'total': total_stocks
    }


if __name__ == "__main__":
    results = fetch_all_stocks(
        start_date='2000-01-01',
        end_date='2025-12-31',
        delay=0.5
    )
    
    print(f"\nData saved to: data/stocks/")
    print(f"Total files created: {len(results['successful'])}")