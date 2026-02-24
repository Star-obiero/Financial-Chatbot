# chatbot.py
import os
from groq import Groq
from dotenv import load_dotenv
from finance_data import get_stock_price, get_crypto_price, get_market_summary
from prompts import SYSTEM_PROMPT, build_user_message
from utils import format_stock_info, clean_ticker

load_dotenv()
client = Groq(api_key=os.getenv('GROQ_API_KEY'))

STOCK_KEYWORDS = ['price', 'stock', 'share', 'trading', 'ticker']
CRYPTO_KEYWORDS = ['bitcoin', 'btc', 'ethereum', 'eth', 'crypto', 'coin']
MARKET_KEYWORDS = ['market', 'index', 'indices', 's&p', 'dow', 'nasdaq']

def detect_intent(user_input: str) -> tuple:
    """Detect if user is asking about a specific stock, crypto, or market."""
    text = user_input.lower()
    if any(kw in text for kw in CRYPTO_KEYWORDS):
        return 'crypto', extract_ticker(user_input, crypto=True)
    if any(kw in text for kw in STOCK_KEYWORDS):
        return 'stock', extract_ticker(user_input)
    if any(kw in text for kw in MARKET_KEYWORDS):
        return 'market', None
    return 'general', None

def extract_ticker(text: str, crypto: bool = False) -> str:
    """Extract stock ticker symbol from user message."""
    import re
    matches = re.findall(r'\b[A-Z]{2,5}\b', text)
    return matches[0] if matches else ('BTC' if crypto else 'AAPL')

def get_market_context(user_input: str) -> str:
    """Fetch relevant market data based on user intent."""
    intent, ticker = detect_intent(user_input)
    if intent == 'stock' and ticker:
        data = get_stock_price(clean_ticker(ticker))
        return format_stock_info(data)
    elif intent == 'crypto' and ticker:
        data = get_crypto_price(clean_ticker(ticker))
        return format_stock_info(data)
    elif intent == 'market':
        return str(get_market_summary())
    return None


def chat(messages: list, user_input: str) -> str:
    """Send message to Groq and return the AI response."""
    market_data = get_market_context(user_input)
    enriched_input = build_user_message(user_input, market_data)

    messages.append({'role': 'user', 'content': enriched_input})

    response = client.chat.completions.create(
        model='llama-3.3-70b-versatile',
        messages=[{'role': 'system', 'content': SYSTEM_PROMPT}] + messages,
        temperature=0.5,
        max_tokens=600
    )

    reply = response.choices[0].message.content
    messages.append({'role': 'assistant', 'content': reply})
    return reply
