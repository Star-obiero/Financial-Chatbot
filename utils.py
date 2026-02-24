# utils.py

def format_currency(value, currency="USD") -> str:
    """Format a number as currency."""
    try:
        return f"{currency} {float(value):,.2f}"
    except:
        return "N/A"

def format_market_cap(value) -> str:
    """Convert large market cap numbers to readable format."""
    try:
        value = float(value)
        if value >= 1_000_000_000_000:
            return f"${value / 1_000_000_000_000:.2f}T"
        elif value >= 1_000_000_000:
            return f"${value / 1_000_000_000:.2f}B"
        elif value >= 1_000_000:
            return f"${value / 1_000_000:.2f}M"
        else:
            return f"${value:,.2f}"
    except:
        return "N/A"

def format_stock_info(data: dict) -> str:
    """Format stock data into a clean readable string for the chatbot."""
    if "error" in data:
        return f"Could not fetch data: {data['error']}"
    return f"""
    📊 {data.get('name', 'N/A')} ({data.get('ticker', 'N/A')})
    💰 Price: {format_currency(data.get('price'), data.get('currency', 'USD'))}
    📈 52-Week High: {format_currency(data.get('52_week_high'), data.get('currency', 'USD'))}
    📉 52-Week Low: {format_currency(data.get('52_week_low'), data.get('currency', 'USD'))}
    🏢 Market Cap: {format_market_cap(data.get('market_cap'))}
    📊 P/E Ratio: {data.get('pe_ratio', 'N/A')}
    """

def is_crypto_ticker(ticker: str) -> bool:
    """Check if a ticker is a cryptocurrency."""
    crypto_list = ['BTC', 'ETH', 'BNB', 'XRP', 'ADA', 'SOL', 'DOGE', 'DOT']
    return ticker.upper() in crypto_list

def clean_ticker(ticker: str) -> str:
    """Clean and validate a ticker symbol."""
    return ticker.strip().upper().replace("$", "")