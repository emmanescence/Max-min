import streamlit as st
import yfinance as yf
import pandas as pd

# Define los grupos de tickers
tickers_adrs = [
    'BBAR', 'BMA', 'CEPU', 'CRESY', 'EDN', 'GGAL', 'IRS', 'LOMA', 'PAM', 'SUPV', 'TEO',
    'TGS', 'YPF', 'MELI', 'DESP', 'GLOB', 'BIOX', 'ARCO', 'TX', 'TS', 'AGRO'
]

tickers_cedears = [
    'SHPW.BA', 'AABA.BA', 'AOCA.BA', 'BA.C.BA', 'CAJ.BA', 'LFC.BA', 'SNP.BA', 'CBRD.BA', 'CS.BA', 'AKO.B.BA',
    'F.BA', 'HNPIY.BA', 'MBT.BA', 'NTCO.BA', 'NLM.BA', 'UN.BA', 'PCRF.BA', 'PTR.BA', 'OGZD.BA', 'LKOD.BA',
    'ATAD.BA', 'SMSN.BA', 'SI.BA', 'TTM.BA', 'RCTB4.BA', 'TWTR.BA', 'AUY.BA', 'AMZN.BA', 'NVDA.BA', 'GOOGL.BA',
    'KO.BA', 'SPY.BA', 'VIST.BA', 'COIN.BA', 'AAPL.BA', 'JMIA.BA', 'SHOP.BA', 'BBD.BA', 'TSLA.BA', 'INTC.BA',
    'MELI.BA', 'MSTR.BA', 'NKE.BA', 'WMT.BA', 'GOLD.BA', 'MSFT.BA', 'AMD.BA', 'BABA.BA', 'VALE.BA', 'QQQ.BA',
    'GLOB.BA', 'LAC.BA', 'RIOT.BA', 'DISN.BA', 'DIA.BA', 'AVGO.BA', 'PFE.BA', 'MCD.BA', 'META.BA', 'AAL.BA',
    'SATL.BA', 'SBUX.BA', 'JNJ.BA', 'IWM.BA', 'BITF.BA', 'BRKB.BA', 'PYPL.BA', 'PEP.BA', 'STLA.BA', 'JD.BA',
    'ZM.BA', 'ARKK.BA', 'UPST.BA', 'WBA.BA', 'DESP.BA', 'EEM.BA', 'HMY.BA', 'XLE.BA', 'MMM.BA', 'EWZ.BA',
    'V.BA', 'PAAS.BA', 'BIDU.BA', 'CVX.BA', 'QCOM.BA', 'SQ.BA', 'XOM.BA', 'T.BA', 'PLTR.BA', 'PG.BA', 'ROKU.BA',
    'NFLX.BA', 'JPM.BA', 'ABNB.BA', 'TEN.BA', 'MU.BA', 'IBM.BA', 'AAP.BA', 'SNOW.BA', 'XP.BA', 'TXR.BA',
    'ADBE.BA', 'BB.BA', 'TM.BA', 'SE.BA', 'HL.BA', 'XLF.BA', 'GM.BA', 'OXY.BA', 'FSLR.BA', 'LYG.BA', 'VZ.BA',
    'BIOX.BA', 'SNAP.BA', 'SPOT.BA', 'ETSY.BA', 'BA.BA', 'BP.BA', 'CSCO.BA', 'PANW.BA', 'ABEV.BA', 'ACN.BA',
    'ADGO.BA', 'MUX.BA', 'AXP.BA', 'DE.BA', 'CVS.BA', 'WFC.BA', 'HD.BA', 'C.BA', 'MA.BA', 'TRIP.BA', 'GE.BA',
    'CAT.BA', 'WBO.BA', 'MO.BA', 'TXN.BA', 'RACE.BA', 'MRVL.BA', 'TEFO.BA', 'TWLO.BA', 'SONY.BA', 'MRNA.BA',
    'NEM.BA', 'DOCU.BA', 'LRCX.BA', 'ABBV.BA', 'TV.BA', 'UBER.BA', 'ITUB.BA', 'ARCO.BA', 'MDLZ.BA', 'BRFS.BA',
    'COST.BA', 'PBR.BA', 'LMT.BA', 'SPGI.BA', 'X.BA', 'BAK.BA', 'PBI.BA', 'STNE.BA', 'GLW.BA', 'CAR.BA',
    'CX.BA', 'HAPV3.BA', 'UL.BA', 'MRK.BA', 'GPRK.BA', 'UAL.BA', 'DAL.BA', 'AMAT.BA', 'AEM.BA', 'BKNG.BA',
    'ERJ.BA', 'SLB.BA', 'AMGN.BA', 'PAGS.BA', 'BBV.BA', 'ERIC.BA', 'BBAS3.BA', 'HSBC.BA', 'PKS.BA', 'GILD.BA',
    'BSBR.BA', 'SPCE.BA', 'NOKA.BA', 'SHEL.BA', 'ORCL.BA', 'RBLX.BA', 'DEO.BA', 'CL.BA', 'SDA.BA', 'GS.BA',
    'PCAR.BA', 'AZN.BA', 'HAL.BA', 'LVS.BA', 'MGLU3.BA', 'INFY.BA', 'UNP.BA', 'EA.BA', 'BHP.BA', 'ASR.BA',
    'GGB.BA', 'RENT3.BA', 'VIV.BA', 'CCL.BA', 'KGC.BA', 'XROX.BA', 'BIIB.BA', 'AMX.BA', 'PHG.BA', 'NTES.BA',
    'ADI.BA', 'GSK.BA', 'USB.BA', 'RTX.BA', 'HWM.BA', 'AIG.BA', 'HON.BA', 'NUE.BA', 'HOG.BA', 'SID.BA',
    'SAN.BA', 'SYY.BA', 'MOS.BA', 'FDX.BA', 'UGP.BA', 'SAP.BA', 'BCS.BA', 'KOFM.BA', 'NG.BA', 'YY.BA',
    'MFG.BA', 'PAC.BA', 'NMR.BA', 'EBAY.BA', 'BK.BA', 'MUFG.BA', 'HDB.BA', 'LND.BA', 'AEG.BA', 'PM.BA',
    'ORAN.BA', 'GFI.BA', 'MSI.BA', 'KMB.BA', 'IP.BA', 'FMX.BA', 'ROST.BA', 'TTE.BA', 'PRIO3.BA', 'LREN3.BA',
    'EFX.BA', 'PINS.BA', 'DD.BA', 'CAH.BA', 'CAAP.BA', 'SUZ.BA', 'SCCO.BA', 'AVY.BA', 'TIMB.BA', 'E.BA',
    'HMC.BA', 'VRSN.BA', 'SNA.BA', 'ING.BA', 'IBN.BA', 'HPQ.BA', 'ADP.BA', 'GRMN.BA', 'KEP.BA', 'EBR.BA',
    'MMC.BA', 'TRVV.BA', 'TCOM.BA', 'ELP.BA', 'IFF.BA', 'URBN.BA', 'SBS.BA', 'KB.BA', 'YELP.BA', 'NEC1.BA',
    'LLY.BA', 'FCX.BA'
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

