# app.py
import streamlit as st
import yfinance as yf
import datetime
import pandas as pd

st.set_page_config(page_title="Multi-Ticker US Stock Tracker", layout="wide")

# Sidebar Settings
st.sidebar.header("🔍 Watchlist Settings")
tickers_input = st.sidebar.text_input("Enter tickers (comma-separated)", "BBAI, PLTR, AI")
tickers = [t.strip().upper() for t in tickers_input.split(",") if t.strip()]
days = st.sidebar.slider("Days of historical data", 7, 180, 30)

start_date = datetime.date.today() - datetime.timedelta(days=days)
end_date = datetime.date.today()

st.title("📊 US Stock Tracker")

# Loop through each ticker
for ticker in tickers:
    try:
        stock = yf.Ticker(ticker)
        hist = stock.history(start=start_date, end=end_date)
        info = stock.info

        if hist.empty:
            st.warning(f"No historical data found for {ticker}")
            continue

        st.subheader(f"💹 {ticker} — {info.get('shortName', '')}")

        # KPI cards
        col1, col2, col3 = st.columns(3)
        col1.metric("Current Price", f"${info.get('regularMarketPrice', 0):.2f}")
        col2.metric("52-Week High", f"${info.get('fiftyTwoWeekHigh', 0):.2f}")
        col3.metric("Market Cap", f"${info.get('marketCap', 0) / 1e9:.2f}B")

        # Sector / Industry
        st.caption(f"**Sector**: {info.get('sector', 'N/A')} | **Industry**: {info.get('industry', 'N/A')}")

        # Price trend chart
        import plotly.graph_objects as go

candlestick = go.Figure(data=[
    go.Candlestick(
        x=hist.index,
        open=hist["Open"],
        high=hist["High"],
        low=hist["Low"],
        close=hist["Close"],
        increasing_line_color='green',
        decreasing_line_color='red'
    )
])
candlestick.update_layout(
    title=f'{ticker} Candlestick Chart',
    yaxis_title='Price (USD)',
    xaxis_rangeslider_visible=False,
    height=400,
    margin=dict(t=30, b=30)
)
st.plotly_chart(candlestick, use_container_width=True)
st.divider()

    except Exception as e:
        st.error(f"❌ Error loading {ticker}: {e}")


        # Alerts
        pe = info.get("forwardPE")
        if pe and pe < 20:
            st.success(f"Valuation Alert: Forward PE < 20 ({pe:.2f})")
        elif pe:
            st.info(f"Forward PE: {pe:.2f}")
        else:
            st.warning("No forward PE data available")

        st.divider()

    except Exception as e:
        st.error(f"❌ Error loading {ticker}: {e}")
