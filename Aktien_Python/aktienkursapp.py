import streamlit as st
import yfinance as yf
import plotly.graph_objects as go
import pandas as pd
from deep_translator import GoogleTranslator

# 🌐 Seitenlayout & Titel
st.set_page_config(page_title="📈 Aktienkurs App", layout="centered")

# 📌 App-Titel
st.title('📈 Aktienkurs Watchlist')

# 📚 Session Watchlist initialisieren
if "watchlist" not in st.session_state:
    st.session_state.watchlist = []

# 📬 Eingabe für neue Aktie
ticker_input = st.text_input('Geben Sie das Ticker Symbol ein (z. B. TSLA für Tesla):')

if st.button("➕ Zur Watchlist hinzufügen"):
    if ticker_input and ticker_input not in st.session_state.watchlist:
        if len(st.session_state.watchlist) < 10:
            st.session_state.watchlist.append(ticker_input)
            st.success(f"'{ticker_input}' wurde zur Watchlist hinzugefügt!")
        else:
            st.warning("Maximal 10 Aktien erlaubt.")
    elif ticker_input in st.session_state.watchlist:
        st.warning(f"'{ticker_input}' ist bereits in der Watchlist.")

# 📋 Tabelle anzeigen
if st.session_state.watchlist:
    st.subheader("📋 Ihre Watchlist:")

    # Tabellenähnliche Darstellung mit klickbaren Elementen
    header_cols = st.columns([2, 4, 5, 2])  # View | Ticker | Name | Kurs
    header_cols[0].markdown("**Aktion**")
    header_cols[1].markdown("**TickerSymbol**")
    header_cols[2].markdown("**Aktienname**")
    header_cols[3].markdown("**Aktueller Kurs**")

    for ticker in st.session_state.watchlist:
        try:
            aktie = yf.Ticker(ticker)
            info = aktie.info
            unternehmen = info.get("longName", "Unbekannt")
            preis = info.get("currentPrice", "—")

            row = st.columns([2, 4, 5, 2])

            # Leicht grauer View-Button
            with row[0]:
                if st.button("View", key=f"view_{ticker}"):
                    st.session_state.selected_ticker = ticker

            with row[1]:
                if st.button(ticker.upper(), key=f"symbol_{ticker}"):
                    st.session_state.selected_ticker = ticker

            with row[2]:
                if st.button(unternehmen, key=f"name_{ticker}"):
                    st.session_state.selected_ticker = ticker

            with row[3]:
                st.write(f"{preis} USD")

        except Exception as e:
            st.error(f"⚠️ Fehler bei {ticker}")
            st.exception(e)

    # CSS für hellgrauen Button (nur "View")
    st.markdown("""
        <style>
        div.stButton > button {
            background-color: #f0f0f0;
            color: black;
            border: 1px solid #ccc;
            padding: 0.25rem 0.5rem;
        }
        div.stButton > button:hover {
            background-color: #e0e0e0;
        }
        </style>
    """, unsafe_allow_html=True)

    # 📊 Details anzeigen, falls ausgewählt
    if "selected_ticker" in st.session_state:
        ticker = st.session_state.selected_ticker
        try:
            aktie = yf.Ticker(ticker)
            info = aktie.info
            unternehmen = info.get("longName", ticker)
            beschreibung = info.get("longBusinessSummary", "Keine Beschreibung verfügbar.")
            preis = info.get("currentPrice", "—")

            st.markdown("---")
            st.subheader(f"📌 {unternehmen} ({ticker.upper()}) — Aktueller Kurs: {preis} USD")

            daten = aktie.history(period='1y')
            angezeigte_daten = daten.loc[daten.index > '2024-01-01']

            fig = go.Figure()
            fig.add_trace(go.Scatter(x=angezeigte_daten.index, y=angezeigte_daten['Close'], name='Kurs'))
            fig.update_layout(
                title=f'{unternehmen} ({ticker.upper()})',
                xaxis_title='Datum',
                yaxis_title='Kurs in USD'
            )
            st.plotly_chart(fig, use_container_width=True)

            # Beschreibung übersetzen
            beschreibung_de = GoogleTranslator(source='auto', target='de').translate(beschreibung)
            with st.expander("📄 Unternehmensbeschreibung anzeigen"):
                st.write(beschreibung_de)

        except
