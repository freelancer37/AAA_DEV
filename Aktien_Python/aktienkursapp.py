import streamlit as st
import yfinance as yf
import plotly.graph_objects as go
import pandas as pd
from deep_translator import GoogleTranslator

# 🌐 Seitenlayout & Titel
st.set_page_config(page_title="📈 Aktienkurs App", layout="centered")

# 📌 App-Titel
st.title('📈 Aktienkurs Watchlist')

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

# 📋 Anzeige der aktuellen Watchlist als interaktive Tabelle
if st.session_state.watchlist:
    st.subheader("📋 Ihre Watchlist:")

    for ticker in st.session_state.watchlist:
        try:
            aktie = yf.Ticker(ticker)
            info = aktie.info
            unternehmen = info.get('longName', 'Unbekannt')
            preis = info.get('currentPrice', '—')

            # 🟩 Zeile mit Klickoptionen
            cols = st.columns([2, 4, 4, 2])  # Spaltenaufteilung: Button, Ticker, Name, Preis

            with cols[0]:
                if st.button("View", key=f"view_{ticker}"):
                    st.session_state.selected_ticker = ticker

            with cols[1]:
                if st.button(ticker.upper(), key=f"symbol_{ticker}"):
                    st.session_state.selected_ticker = ticker

            with cols[2]:
                if st.button(unternehmen, key=f"name_{ticker}"):
                    st.session_state.selected_ticker = ticker

            with cols[3]:
                st.write(f"{preis} USD")

            # Grüner Button-Style
            st.markdown("""
                <style>
                    div.stButton > button {
                        background-color: #28a745;
                        color: white;
                        border: none;
                        padding: 0.25rem 0.5rem;
                        font-weight: bold;
                    }
                    div.stButton > button:hover {
                        background-color: #218838;
                        color: white;
                    }
                </style>
            """, unsafe_allow_html=True)

        except Exception as e:
            st.error(f"⚠️ Fehler beim Abrufen der Daten für {ticker}.")
            st.exception(e)

    # 📊 Details zur ausgewählten Aktie anzeigen
    if "selected_ticker" in st.session_state:
        ticker = st.session_state.selected_ticker
        try:
            aktie = yf.Ticker(ticker)
            info = aktie.info
            unternehmen = info.get('longName', ticker)
            beschreibung = info.get('longBusinessSummary', 'Keine Beschreibung verfügbar.')
            preis = info.get('currentPrice', '—')

            st.markdown("---")
            st.subheader(f"📌 {unternehmen} ({ticker.upper()}) — Aktueller Kurs: {preis} USD")

            # 📈 Kursverlauf anzeigen
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

            # 🌍 Übersetzung mit deep_translator
            beschreibung_de = GoogleTranslator(source='auto', target='de').translate(beschreibung)

            # 📄 Unternehmensbeschreibung als aufklappbarer Text
            with st.expander("📄 Unternehmensbeschreibung anzeigen"):
                st.write(beschreibung_de)

        except Exception as e:
            st.error(f"⚠️ Fehler beim Abrufen der Daten für {ticker}.")
            st.exception(e)

else:
    st.info("🔍 Fügen Sie Aktien zur Watchlist hinzu und klicken Sie auf eine Zeile, um Details anzuzeigen.")
