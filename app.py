# app.py
import streamlit as st
from chatbot import chat

# ── Page Config ──────────────────────────────────────────────────
st.set_page_config(
    page_title='FinBot - Stock & Investment Advisor',
    page_icon='📈',
    layout='centered'
)

# ── Header ───────────────────────────────────────────────────────
st.title('📈 FinBot - Stock & Investment Advisor')
st.caption('AI-powered chatbot for stocks, crypto, mutual funds & investing')
st.warning('⚠️ For educational purposes only. Not financial advice.')
st.divider()

# ── Session State (conversation memory) ──────────────────────────
if 'messages' not in st.session_state:
    st.session_state.messages = []
if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []

# ── Display Chat History ─────────────────────────────────────────
for msg in st.session_state.chat_history:
    with st.chat_message(msg['role']):
        st.markdown(msg['content'])

# ── Chat Input ───────────────────────────────────────────────────
if prompt := st.chat_input('Ask about stocks, crypto, or investments...'):
    # Show user message
    with st.chat_message('user'):
        st.markdown(prompt)
    st.session_state.chat_history.append({'role': 'user', 'content': prompt})

    # Get AI response
    with st.chat_message('assistant'):
        with st.spinner('Fetching data & generating response...'):
            response = chat(st.session_state.messages, prompt)
        st.markdown(response)
    st.session_state.chat_history.append({'role': 'assistant', 'content': response})

# ── Sidebar ──────────────────────────────────────────────────────
with st.sidebar:
    st.header('💡 Sample Questions')
    st.write("• What is Apple's current stock price?")
    st.write("• What is the price of Bitcoin today?")
    st.write("• What is dollar-cost averaging?")
    st.write("• How do mutual funds work?")
    st.write("• Compare stocks vs crypto risk")
    st.write("• What is a P/E ratio?")
    st.divider()
    if st.button('🗑️ Clear Chat'):
        st.session_state.messages = []
        st.session_state.chat_history = []
        st.rerun()

