Bessembinder 2018: Replication of Do Stocks Outperform Treasury Bills?
Key Findings
- Sample: 48 large-cap Indian stocks from major indices
- Time Period: 2000-2025 (25 years)
- Result:94% of stocks outperformed T-bills**
- Compare to Bessembinder's US finding: Only 42.6% beat T-bills
- Median Return: 6,167% vs T-bill return of ~480%

The primary driver of our different result:
- Our sample: Current Nifty 500 constituents (all survivors)
- Bessembinder's sample: ALL 26,000+ US stocks since 1926, including:
  - 14,661 companies (58%) that failed completely
  - Thousands of delisted, bankrupt, and penny stocks

## Project Structure

├── src/
│   ├── fetch_nifty500.py          # Fetches stock list from Wikipedia/CSV
│   ├── fetch_historical_data.py   # Downloads historical price data via yfinance
│   └── calculate_returns.py       # Calculates buy-and-hold returns & T-bill comparison
├── data/
│   ├── nifty500_constituents.csv  # List of 50 stocks analyzed
│   ├── returns_summary.csv        # Complete results with returns & comparisons
│   └── stocks/                    # Individual stock price CSVs (not in repo)
└── ssrn_id3186246_code667.pdf    # Original Bessembinder (2018) paper

## How To Run

### Step 1: Download Stock Data
```bash
python src/fetch_historical_data.py
```
This downloads 25 years of daily price data for all stocks in `nifty500_constituents.csv`.

### Step 2: Calculate Returns
```bash
python src/calculate_returns.py
```
This calculates:
- Buy-and-hold returns for each stock
- Matched T-bill returns (using 7% avg annual rate)
- Comparison statistics

### Results
Output saved to `data/returns_summary.csv` with columns:
- `Ticker`, `Start_Date`, `End_Date`, `Years`
- `Stock_Return_Pct`, `Tbill_Return_Pct`
- `Excess_Return_Pct`, `Beat_Tbills` (True/False)

## 📊 Methodology

### Buy-and-Hold Returns
```
Return = (Final Price / Initial Price - 1) × 100%
```
Uses adjusted close prices (accounts for dividends and splits).

### T-Bill Benchmark
Simplified model using 7% average annual rate for Indian government securities (2000-2025):
```
T-bill Return = (1.07)^years - 1
```

### Stock Selection
Sample consists of 48 major Indian stocks from Nifty indices, including:
- Reliance Industries, TCS, HDFC Bank, Infosys
- Large-cap companies across sectors
- Only currently listed stocks (survivorship bias inherent)

## ⚠️ Limitations & Caveats

1. **Survivorship Bias (Critical)**
   - Sample includes only current index constituents
   - Excludes thousands of delisted/failed Indian companies
   - Artificially inflates the % beating T-bills
   - This is the PRIMARY reason for different results vs Bessembinder

2. **T-Bill Simplification**
   - Uses constant 7% rate vs actual monthly RBI T-bill rates
   - More accurate approach: match actual rates to each stock's time period

3. **Sample Size**
   - 48 stocks vs Bessembinder's 26,000+
   - All large-cap (Bessembinder included micro-cap)

4. **Time Period**
   - 2000-2025: Strong Indian economic growth period
   - Bessembinder: 1926-2016 (includes Great Depression, multiple crashes)

## Key Insights

### What This Replication Teaches:

1. **Survivorship bias is powerful** - Excluding failed companies changes results from 43% to 94%

2. **Positive skewness matters** - Even among survivors, a few massive winners (Bajaj Finance: 251,898% return!) drive overall market gains

3. **Diversification is critical** - Most individual stocks underperform when failures are included

4. **Mean ≠ Median** - Mean return heavily influenced by extreme winners; median tells different story

### Comparison Summary

| Metric | Bessembinder (US) | This Study (India) |
|--------|-------------------|-------------------|
| **Sample** | 26,000 stocks (all) | 48 stocks (survivors) |
| **Period** | 1926-2016 | 2000-2025 |
| **% Beat T-bills** | 42.6% | 94% |
| **Median Return** | Negative | 6,167% |
| **Key Factor** | Includes failures | Survivorship bias |

## Technologies Used

- **Python 3.9+**
- **pandas** - Data manipulation and analysis
- **yfinance** - Historical stock price data from Yahoo Finance
- **Git/GitHub** - Version control and collaboration

## References

Bessembinder, H. (2018). "Do Stocks Outperform Treasury Bills?" *Journal of Financial Economics*, 129(3), 440-457.
- Paper: https://papers.ssrn.com/sol3/papers.cfm?abstract_id=2900447


This project was completed as a learning exercise to understand:
- Empirical finance research methodology
- Survivorship bias in financial data
- Return distribution skewness
- Python for quantitative finance

This project is for educational purposes. Original research by Hendrik Bessembinder.
