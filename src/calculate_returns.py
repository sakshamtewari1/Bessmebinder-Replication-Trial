"""
Calculate buy-and-hold returns for all stocks

This script:
1. Loads each stock's historical data
2. Calculates lifetime buy-and-hold returns
3. Compares to T-bill benchmark
4. Creates a summary CSV with results
"""

import pandas as pd
import os
from datetime import datetime


def calculate_stock_return(csv_filepath):
    """
    Calculate buy-and-hold return for a single stock.
    
    Args:
        csv_filepath (str): Path to stock CSV file
    
    Returns:
        dict: Stock information and returns
    """
    try:
        # Read the stock data
        df = pd.read_csv(csv_filepath)
        
        if df.empty or len(df) < 2:
            return None
        
        # Get stock ticker from filename
        ticker = os.path.basename(csv_filepath).replace('.csv', '').replace('_', '.')
        
        # Get first and last dates
        df['Date'] = pd.to_datetime(df['Date'])
        start_date = df['Date'].iloc[0]
        end_date = df['Date'].iloc[-1]
        
        # Calculate buy-and-hold return using Close price
        # Close price is already adjusted for dividends and splits
        first_price = df['Close'].iloc[0]
        last_price = df['Close'].iloc[-1]
        
        # Buy-and-hold return (as percentage)
        stock_return = ((last_price / first_price) - 1) * 100
        
        # Calculate number of years
        years = (end_date - start_date).days / 365.25
        
        # Calculate annualized return
        annualized_return = (((last_price / first_price) ** (1/years)) - 1) * 100
        
        return {
            'Ticker': ticker,
            'Start_Date': start_date.strftime('%Y-%m-%d'),
            'End_Date': end_date.strftime('%Y-%m-%d'),
            'Years': round(years, 2),
            'First_Price': round(first_price, 2),
            'Last_Price': round(last_price, 2),
            'Stock_Return_Pct': round(stock_return, 2),
            'Annualized_Return_Pct': round(annualized_return, 2)
        }
        
    except Exception as e:
        print(f"Error processing {csv_filepath}: {e}")
        return None


def calculate_tbill_return(years, start_year=2000):
    """
    Calculate approximate T-bill return for Indian market.
    
    This is a simplified model using historical average rates:
    - 2000-2010: ~7% average
    - 2010-2020: ~7% average  
    - 2020-2025: ~6% average
    
    Args:
        years (float): Number of years
        start_year (int): Starting year
    
    Returns:
        float: Compound T-bill return percentage
    """
    # Simplified: Use average Indian T-bill rate of ~7% per year
    avg_tbill_rate = 0.07
    
    # Compound return: (1 + rate)^years - 1
    compound_return = ((1 + avg_tbill_rate) ** years - 1) * 100
    
    return round(compound_return, 2)


def analyze_all_stocks(stocks_dir='data/stocks', output_file='data/returns_summary.csv'):
    """
    Analyze all stocks and create summary report.
    
    Args:
        stocks_dir (str): Directory containing stock CSV files
        output_file (str): Output CSV filepath
    
    Returns:
        pd.DataFrame: Summary of all stock returns
    """
    print("=" * 70)
    print("Calculating Returns for All Stocks")
    print("=" * 70)
    
    # Get all CSV files
    csv_files = [f for f in os.listdir(stocks_dir) if f.endswith('.csv')]
    total_stocks = len(csv_files)
    
    print(f"\nFound {total_stocks} stock files")
    print("\nProcessing...\n")
    
    results = []
    
    for idx, filename in enumerate(csv_files, 1):
        filepath = os.path.join(stocks_dir, filename)
        
        print(f"[{idx}/{total_stocks}] Processing {filename}...", end=' ')
        
        result = calculate_stock_return(filepath)
        
        if result:
            # Add T-bill comparison
            start_year = int(result['Start_Date'][:4])
            tbill_return = calculate_tbill_return(result['Years'], start_year)
            
            result['Tbill_Return_Pct'] = tbill_return
            result['Excess_Return_Pct'] = round(result['Stock_Return_Pct'] - tbill_return, 2)
            result['Beat_Tbills'] = result['Stock_Return_Pct'] > tbill_return
            
            results.append(result)
            print(f"✓ Return: {result['Stock_Return_Pct']}%")
        else:
            print("✗ Failed")
    
    # Create DataFrame
    df = pd.DataFrame(results)
    
    # Sort by stock return (descending)
    df = df.sort_values('Stock_Return_Pct', ascending=False).reset_index(drop=True)
    
    # Save to CSV
    df.to_csv(output_file, index=False)
    
    print("\n" + "=" * 70)
    print("Analysis Complete!")
    print("=" * 70)
    
    # Print summary statistics
    print(f"\nTotal stocks analyzed: {len(df)}")
    print(f"\nStocks that beat T-bills: {df['Beat_Tbills'].sum()} ({df['Beat_Tbills'].sum()/len(df)*100:.1f}%)")
    print(f"Stocks that lost to T-bills: {(~df['Beat_Tbills']).sum()} ({(~df['Beat_Tbills']).sum()/len(df)*100:.1f}%)")
    
    print(f"\nMean stock return: {df['Stock_Return_Pct'].mean():.2f}%")
    print(f"Median stock return: {df['Stock_Return_Pct'].median():.2f}%")
    print(f"Best performer: {df.iloc[0]['Ticker']} ({df.iloc[0]['Stock_Return_Pct']:.2f}%)")
    print(f"Worst performer: {df.iloc[-1]['Ticker']} ({df.iloc[-1]['Stock_Return_Pct']:.2f}%)")
    
    print(f"\nResults saved to: {output_file}")
    
    return df


if __name__ == "__main__":
    # Run the analysis
    df_results = analyze_all_stocks()
    
    # Show top 10 and bottom 10
    print("\n" + "=" * 70)
    print("Top 10 Performers")
    print("=" * 70)
    print(df_results.head(10)[['Ticker', 'Years', 'Stock_Return_Pct', 'Tbill_Return_Pct', 'Beat_Tbills']].to_string(index=False))
    
    print("\n" + "=" * 70)
    print("Bottom 10 Performers")
    print("=" * 70)
    print(df_results.tail(10)[['Ticker', 'Years', 'Stock_Return_Pct', 'Tbill_Return_Pct', 'Beat_Tbills']].to_string(index=False))