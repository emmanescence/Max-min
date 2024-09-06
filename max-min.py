import streamlit as st
import yfinance as yf
import pandas as pd

# Define los grupos de tickers
tickers_adrs = [
    'BBAR', 'BMA', 'CEPU', 'CRESY', 'EDN', 'GGAL', 'IRS', 'LOMA', 'PAM', 'SUPV', 'TEO',
    'TGS', 'YPF', 'MELI', 'DESP', 'GLOB', 'BIOX', 'ARCO', 'TX', 'TS', 'AGRO'
]

tickers_cedears = [
    'SHPW', 'AABA', 'AOCA', 'BA.C', 'CAJ', 'LFC', 'SNP', 'CBRD', 'CS', 'AKO.B',
    'F', 'HNPIY', 'MBT', 'NTCO', 'NLM', 'UN', 'PCRF', 'PTR', 'OGZD', 'LKOD',
    'ATAD', 'SMSN', 'SI', 'TTM', 'RCTB4', 'TWTR', 'AUY', 'AMZN', 'NVDA', 'GOOGL',
    'KO', 'SPY', 'VIST', 'COIN', 'AAPL', 'JMIA', 'SHOP', 'BBD', 'TSLA', 'INTC',
    'MELI', 'MSTR', 'NKE', 'WMT', 'GOLD', 'MSFT', 'AMD', 'BABA', 'VALE', 'QQQ',
    'GLOB', 'LAC', 'RIOT', 'DISN', 'DIA', 'AVGO', 'PFE', 'MCD', 'META', 'AAL',
    'SATL', 'SBUX', 'JNJ', 'IWM', 'BITF', 'BRKB', 'PYPL', 'PEP', 'STLA', 'JD',
    'ZM', 'ARKK', 'UPST', 'WBA', 'DESP', 'EEM', 'HMY', 'XLE', 'MMM', 'EWZ',
    'V', 'PAAS', 'BIDU', 'CVX', 'QCOM', 'SQ', 'XOM', 'T', 'PLTR', 'PG', 'ROKU',
    'NFLX', 'JPM', 'ABNB', 'TEN', 'MU', 'IBM', 'AAP', 'SNOW', 'XP', 'TXR',
    'ADBE', 'BB', 'TM', 'SE', 'HL', 'XLF', 'GM', 'OXY', 'FSLR', 'LYG', 'VZ',
    'BIOX', 'SNAP', 'SPOT', 'ETSY', 'BA', 'BP', 'CSCO', 'PANW', 'ABEV', 'ACN',
    'ADGO', 'MUX', 'AXP', 'DE', 'CVS', 'WFC', 'HD', 'C', 'MA', 'TRIP', 'GE',
    'CAT', 'WBO', 'MO', 'TXN', 'RACE', 'MRVL', 'TEFO', 'TWLO', 'SONY', 'MRNA',
    'NEM', 'DOCU', 'LRCX', 'ABBV', 'TV', 'UBER', 'ITUB', 'ARCO', 'MDLZ', 'BRFS',
    'COST', 'PBR', 'LMT', 'SPGI', 'X', 'BAK', 'PBI', 'STNE', 'GLW', 'CAR',
    'CX', 'HAPV3', 'UL', 'MRK', 'GPRK', 'UAL', 'DAL', 'AMAT', 'AEM', 'BKNG',
    'ERJ', 'SLB', 'AMGN', 'PAGS', 'BBV', 'ERIC', 'BBAS3', 'HSBC', 'PKS', 'GILD',
    'BSBR', 'SPCE', 'NOKA', 'SHEL', 'ORCL', 'RBLX', 'DEO', 'CL', 'SDA', 'GS',
    'PCAR', 'AZN', 'HAL', 'LVS', 'MGLU3', 'INFY', 'UNP', 'EA', 'BHP', 'ASR',
    'GGB', 'RENT3', 'VIV', 'CCL', 'KGC', 'XROX', 'BIIB', 'AMX', 'PHG', 'NTES',
    'ADI', 'GSK', 'USB', 'RTX', 'HWM', 'AIG', 'HON', 'NUE', 'HOG', 'SID',
    'SAN', 'SYY', 'MOS', 'FDX', 'UGP', 'SAP', 'BCS', 'KOFM', 'NG', 'YY',
    'MFG', 'PAC', 'NMR', 'EBAY', 'BK', 'MUFG', 'HDB', 'LND', 'AEG', 'PM',
    'ORAN', 'GFI', 'MSI', 'KMB', 'IP', 'FMX', 'ROST', 'TTE', 'PRIO3', 'LREN3',
    'EFX', 'PINS', 'DD', 'CAH', 'CAAP', 'SUZ', 'SCCO', 'AVY', 'TIMB', 'E',
    'HMC', 'VRSN', 'SNA', 'ING', 'IBN', 'HPQ', 'ADP', 'GRMN', 'KEP', 'EBR',
    'MMC', 'TRVV', 'TCOM', 'ELP', 'IFF', 'URBN', 'SBS', 'KB', 'YELP', 'NEC1',
    'LLY', 'FCX'
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

# Función para obtener la información del ticker
def get_ticker_info(ticker):
    try:
        ticker_data = yf.Ticker(ticker)
        max_price = ticker_data.history(period='max')['Close'].max()
        latest_data = ticker_data.history(period='1d')['Close']
        
        if latest_data.empty:
            return None, None, None, None, None

        latest_price = latest_data.iloc[-1]
        max_price_date = ticker_data.history(period='max')['Close'].idxmax()

        if max_price == 0:
            return None, None, None, None, None

        drawdown = ((max_price - latest_price) / max_price) * 100
        potential_rise = ((max_price - latest_price) / latest_price) * 100

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
                'Drawdown (%)': drawdown,
                'Potential Rise (%)': potential_rise,
                'Max Price': max_price,
                'Max Price Date': max_price_date,
                'Current Price': latest_price
            })

    df = pd.DataFrame(results)
    df_sorted = df.sort_values('Drawdown (%)', ascending=False)
    top_10_farthest = df_sorted.head(10)
    top_10_closest = df_sorted.tail(10)

    st.write("### Top 10 con Mayor Drawdown")
    st.dataframe(top_10_farthest)

    st.write("### Top 10 con Menor Drawdown")
    st.dataframe(top_10_closest)

# Interfaz principal
st.title('Información de Tickers')
tab1, tab2, tab3, tab4 = st.tabs(["ADR", "CEDEAR", "Panel Líder", "Panel General"])

with tab1:
    st.write("### ADRs")
    display_tickers(tickers_adrs)

with tab2:
    st.write("### CEDEARs")
    display_tickers(tickers_cedears)

with tab3:
    st.write("### Panel Líder")
    display_tickers(tickers_panel_lider)

with tab4:
    st.write("### Panel General")
    display_tickers(tickers_panel_general)
