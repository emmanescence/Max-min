import streamlit as st
import yfinance as yf
import pandas as pd

# Define los grupos de tickers
tickers_adrs = [
    'BBAR', 'BMA', 'CEPU', 'CRESY', 'EDN', 'GGAL', 'IRS', 'LOMA', 'PAM', 'SUPV', 'TEO',
    'TGS', 'YPF', 'MELI', 'DESP', 'GLOB', 'BIOX', 'ARCO', 'TX', 'TS', 'AGRO'
]

tickers_panel_lider = [
    'ALUA.BA', 'BBAR.BA', 'BMA.BA', 'BYMA.BA', 'CEPU.BA', 'COME.BA', 'CRES.BA', 'CVH.BA', 'EDN.BA',
    'GGAL.BA', 'HARG.BA', 'LOMA.BA', 'MIRG.BA', 'PAMP.BA', 'SUPV.BA', 'TECO2.BA', 'TGNO4.BA', 'TGSU2.BA',
    'TRAN.BA', 'TXAR.BA', 'VALO.BA', 'YPFD.BA'
]

tickers_panel_general = [
    'AGRO.BA','AUSO.BA','BHIP.BA','BOLT.BA','BPAT.BA','CADO.BA','CAPX.BA','CARC.BA','CECO2.BA','CELU.BA','CGPA2.BA','CTIO.BA','DGCE.BA',
    'DGCU2.BA','DOME.BA','DYCA.BA','FERR.BA','FIPL.BA','GARO.BA','GBAN.BA','GCDI.BA','GCLA.BA','GRIM.BA','HAVA.BA','INTR.BA','INVJ.BA',
    'IRSA.BA','LEDE.BA','LONG.BA','METR.BA','MOLA.BA','MOLI.BA','MORI.BA','OEST.BA','PATA.BA','RIGO.BA','ROSE.BA','SAMI.BA','SEMI.BA'
]

# Tickers con cálculos especiales
special_tickers = {'AGRO.BA'}

# Función para obtener la información del ticker
def get_ticker_info(ticker):
    try:
        ticker_data = yf.Ticker(ticker)
        historical_data = ticker_data.history(period='max')
        latest_data = ticker_data.history(period='1d')['Close']

        if latest_data.empty:
            return None, None, None, None, None

        latest_price = latest_data.iloc[-1]
        
        if ticker in special_tickers:
            # Para tickers especiales, usar el máximo del año en curso
            this_year = pd.Timestamp.now().year
            year_data = historical_data[historical_data.index.year == this_year]
            if year_data.empty:
                return None, None, None, None, None
            max_price = year_data['Close'].max()
            max_price_date = year_data['Close'].idxmax()
        else:
            # Para otros tickers, usar el máximo histórico
            max_price = historical_data['Close'].max()
            max_price_date = historical_data['Close'].idxmax()

        if max_price == 0:
            return None, None, None, None, None

        drawdown = round(((max_price - latest_price) / max_price) * 100, 1)
        potential_rise = round(((max_price - latest_price) / latest_price) * 100, 1)

        return drawdown, potential_rise, max_price, max_price_date, latest_price
    except Exception as e:
        st.error(f"Error fetching data for {ticker}: {e}")
        return None, None, None, None, None

# Función para mostrar los tickers
def display_tickers(tickers):
    results = []
    for ticker in tickers:
        drawdown, potential_rise, max_price, max_price_date, latest_price = get_ticker_info(ticker)
        if drawdown is not None:
            results.append({
                'Ticker': ticker,
                'Drawdown (%)': drawdown,  # Mantén un solo decimal
                'Potential Rise (%)': potential_rise,
                'Max Price': max_price,
                'Max Price Date': max_price_date.strftime('%d-%m-%Y'),  # Formateo de la fecha
                'Current Price': latest_price
            })

    df = pd.DataFrame(results)
    df_sorted = df.sort_values('Drawdown (%)', ascending=False)
    top_10_farthest = df_sorted.head(10)
    top_10_closest = df_sorted.tail(10)

    # Formateo de la tabla
    def format_table(df):
        df = df.style.format("{:.1f}", subset=['Drawdown (%)', 'Potential Rise (%)', 'Max Price', 'Current Price', 'Max Price Date'])
        df = df.set_properties(**{'text-align': 'center'}, subset=['Drawdown (%)', 'Potential Rise (%)', 'Max Price', 'Current Price'])
        df = df.set_table_styles([{'selector': 'th', 'props': [('text-align', 'center')]}])  # Centrar títulos
        df = df.hide(axis='index')  # Eliminar el índice
        return df

    st.write("### Top 10 con Mayor Drawdown")
    st.write(format_table(top_10_farthest).to_html(), unsafe_allow_html=True)

    st.write("### Top 10 con Menor Drawdown")
    st.write(format_table(top_10_closest).to_html(), unsafe_allow_html=True)

# Interfaz principal
st.title('Información de Tickers')
tab1, tab2, tab3 = st.tabs(["ADR", "Panel Líder", "Panel General"])

with tab1:
    st.write("### ADRs")
    display_tickers(tickers_adrs)

with tab2:
    st.write("### Panel Líder")
    display_tickers(tickers_panel_lider)

with tab3:
    st.write("### Panel General")
    display_tickers(tickers_panel_general)
