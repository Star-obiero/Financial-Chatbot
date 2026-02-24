# finance_data.py
import yfinance as yf
import pandas as pd

def get_stock_price(ticker: str) -> dict:
    """Fetch current price and key info for a stock ticker."""
    try:
        stock = yf.Ticker(ticker.upper())
        info = stock.info
        return {
            "ticker": ticker.upper(),
            "name": info.get("longName", "N/A"),
            "price": info.get("currentPrice", info.get("regularMarketPrice", "N/A")),
            "currency": info.get("currency", "USD"),
            "market_cap": info.get("marketCap", "N/A"),
            "pe_ratio": info.get("trailingPE", "N/A"),
            "52_week_high": info.get("fiftyTwoWeekHigh", "N/A"),
            "52_week_low": info.get("fiftyTwoWeekLow", "N/A"),
        }
    except Exception as e:
        return {"error": str(e)}

def get_crypto_price(symbol: str) -> dict:
    """Fetch current price for a cryptocurrency (e.g. BTC)."""
    ticker = f"{symbol.upper()}-USD"
    return get_stock_price(ticker)

def get_historical_data(ticker: str, period: str = '1mo') -> pd.DataFrame:
    """Fetch historical data. Period options: 1d, 5d, 1mo, 3mo, 1y"""
    try:
        stock = yf.Ticker(ticker.upper())
        hist = stock.history(period=period)
        return hist
    except Exception as e:
        return pd.DataFrame()

def get_market_summary() -> dict:
    """Fetch summary of major market indices."""
    indices = {
        "S&P 500": "^GSPC",
        "Dow Jones": "^DJI",
        "NASDAQ": "^IXIC",
        "Bitcoin": "BTC-USD"
    }
    summary = {}
    for name, ticker in indices.items():
        data = get_stock_price(ticker)
        summary[name] = data.get('price', 'N/A')
    return summary
