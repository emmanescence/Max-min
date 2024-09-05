import streamlit as st
import yfinance as yf
import pandas as pd

def get_max_drawdown(ticker):
    try:
        data = yf.download(ticker, period='max', auto_adjust=True)
        max_price = data['Close'].max()
        latest_price = data['Close'].iloc[-1]
        if max_price == 0:
            return 0
        drawdown = ((max_price - latest_price) / max_price) * 100
        return drawdown
    except Exception as e:
        st.error(f"Error fetching data for {ticker}: {e}")
        return None

def display_tickers(tickers):
    drawdowns = {}
    for ticker in tickers:
        drawdown = get_max_drawdown(ticker)
        if drawdown is not None:
            drawdowns[ticker] = drawdown

    df = pd.DataFrame(list(drawdowns.items()), columns=['Ticker', 'Drawdown (%)'])
    df_sorted = df.sort_values(by='Drawdown (%)', ascending=False)

    top_10_farthest = df_sorted.head(10)
    top_10_closest = df_sorted.tail(10)

    st.subheader('Top 10 tickers farthest from their historical max')
    st.dataframe(top_10_farthest)

    st.subheader('Top 10 tickers closest to their historical max')
    st.dataframe(top_10_closest)

def search_ticker():
    ticker = st.text_input("Enter a ticker symbol:")
    if ticker:
        drawdown = get_max_drawdown(ticker)
        if drawdown is not None:
            st.write(f"The ticker {ticker} is {drawdown:.2f}% away from its historical maximum price.")

def main():
    st.title('Ticker Maximum Drawdown Finder')
    
    st.sidebar.header('Select a group of tickers:')
    group = st.sidebar.selectbox(
        'Group',
        ['ADRs', 'CEDEARs', 'Panel Líder', 'Panel General']
    )

    if group == 'ADRs':
        tickers = tickers_adrs
    elif group == 'CEDEARs':
        tickers = tickers_cedears
    elif group == 'Panel Líder':
        tickers = tickers_panel_lider
    elif group == 'Panel General':
        tickers = tickers_panel_general

    display_tickers(tickers)
    st.sidebar.subheader('Search for a ticker:')
    search_ticker()

if __name__ == "__main__":
    main()
