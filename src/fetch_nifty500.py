"""
Fetch Nifty 500 constituent stocks

This module loads the list of Nifty 500 companies 
and prepares their ticker symbols for data fetching.
"""

import pandas as pd
import os


def load_from_csv(csv_path='data/nifty500_constituents.csv'):
    """
    Load Nifty 500 constituents from a local CSV file.
    
    Args:
        csv_path (str): Path to the CSV file
    
    Returns:
        pd.DataFrame: DataFrame with Company, Symbol, and Ticker columns
    """
    print(f"Reading from CSV file: {csv_path}")
    
    if not os.path.exists(csv_path):
        raise FileNotFoundError(f"CSV file not found: {csv_path}")
    
    df = pd.read_csv(csv_path)
    
    # Validate CSV has required columns
    required_cols = ['Company', 'Symbol', 'Ticker']
    missing_cols = [col for col in required_cols if col not in df.columns]
    
    if missing_cols:
        raise ValueError(f"CSV missing required columns: {missing_cols}")
    
    print(f"✓ Loaded {len(df)} stocks from CSV")
    return df


def get_nifty500_tickers(csv_path='data/nifty500_constituents.csv'):
    """
    Load Nifty 500 constituents from CSV.
    
    Args:
        csv_path (str): Path to the CSV file
    
    Returns:
        pd.DataFrame: DataFrame with columns:
            - Company: Company name
            - Symbol: Stock symbol (without exchange)
            - Ticker: Full ticker with .NS suffix (for yfinance)
    
    Example:
        >>> df = get_nifty500_tickers()
        >>> print(df.head())
    """
    return load_from_csv(csv_path)


# This part runs ONLY when you execute this file directly
if __name__ == "__main__":
    print("=" * 70)
    print("Fetching Nifty 500 Constituents")
    print("=" * 70)
    
    # Load the data
    df = get_nifty500_tickers()
    
    print("\n" + "=" * 70)
    print("Summary Statistics")
    print("=" * 70)
    print(f"Total stocks: {len(df)}")
    
    print(f"\nFirst 10 stocks:")
    print(df.head(10).to_string(index=False))
    
    print(f"\nLast 5 stocks:")
    print(df.tail(5).to_string(index=False))
    
    print(f"\nSample tickers for yfinance:")
    print(df['Ticker'].head(10).tolist())