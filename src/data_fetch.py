"""
data_fetch.py
This script downloads Indian stock market data for our analysis.
We're replicating the Bessembinder (2018) study with Indian stocks.
"""

# First, let's import the tools we need
import yfinance as yf    # This downloads stock data from Yahoo Finance

ticker = "RELIANCE.NS"   # .NS means NSE (National Stock Exchange)

# Download the historical data
print(f"Downloading data for {ticker}...")
data = yf.download(ticker, start="2000-01-01")

# Show the first few rows
print(data.head())
