import streamlit as st
import yfinance as yf
import plotly.graph_objects as go
import pandas as pd
from deep_translator import GoogleTranslator

# 🌐 Seitenlayout & Titel
st.set_page_config(page_title="📈 Aktienkurs App", layout="centered")

# 📌 App-Titel
st.title('📈 Aktienkurs Abfrage')

# 📚 Watchlist speichern
if "watchlist" not in st.session_state:
    st.session_state.watchlist = []

# 📬 Eingabe Aktienticker und Hinzufügen zur Watchlist
ticker_input = st.text_input('Geben Sie das Ticker Symbol ein: (z.B. TSLA für Tesla)')

# 🚀 Hinzufügen Button für Watchlist (max. 10)
if st.button("🚀 Zur Watchlist hinzufügen"):
    if ticker_input and ticker_input not in st.session_state.watchlist:
        if len(st.session_state.watchlist) < 10:
            st.session_state.watchlist.append(ticker_input)
            st.success(f"'{ticker_input}' wurde zur Watchlist hinzugefügt!")
        else:
            st.warning("Sie können nur bis zu 10 Aktien in der Watchlist speichern.")
    elif ticker_input in st.session_state.watchlist:
        st.warning(f"'{ticker_input}' ist bereits in der Watchlist.")

# 📋 Anzeige der aktuellen Watchlist als Tabelle
if st.session_state.watchlist:
    st.subheader("📋 Ihre Watchlist:")

    # Erstellen eines leeren DataFrames
    watchlist_data = []

    # Abrufen der Daten für die Watchlist
    for ticker in st.session_state.watchlist:
        try:
            aktie = yf.Ticker(ticker)
            info = aktie.info
            unternehmen = info['longName']
            preis = info['currentPrice']

            # Hinzufügen der Daten zur Liste
            watchlist_data.append([ticker, unternehmen, preis])

        except Exception as e:
            st.error(f"⚠️ Fehler beim Abrufen der Daten für {ticker}.")
            st.exception(e)

    # Erstellen eines DataFrames für die Tabelle
    watchlist_df = pd.DataFrame(watchlist_data, columns=["TickerSymbol", "Aktienname", "Aktueller Kurs"])

    # Anzeige der Tabelle in Streamlit
    st.dataframe(watchlist_df)

    # 📌 Option zum Anzeigen der Details einer Aktie
    ticker_selected = st.selectbox("Wählen Sie eine Aktie aus der Watchlist, um mehr Details anzuzeigen:", st.session_state.watchlist)

    if ticker_selected:
        try:
            aktie = yf.Ticker(ticker_selected)
            info = aktie.info
            unternehmen = info['longName']
            beschreibung = info['longBusinessSummary']
            preis = info['currentPrice']

            st.subheader(f"{unternehmen} ({ticker_selected.upper()}) — Aktueller Kurs: {preis} USD")

            # 📊 Kursverlauf (Plotly-Grafik
