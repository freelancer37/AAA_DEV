import streamlit as st
import sqlite3
import yfinance as yf
import plotly.graph_objects as go
from deep_translator import GoogleTranslator

# 🌐 Seitenlayout & Titel
st.set_page_config(page_title="📈 Aktienkurs App", layout="centered")

# 📌 App-Titel
st.title('📈 Aktienkurs Watchlist')

# 📚 Datenbank und Watchlist initialisieren
def get_db_connection():
    conn = sqlite3.connect('watchlist.db')  # SQLite-Datenbank
    return conn

def create_watchlist_table():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS watchlist (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            ticker TEXT UNIQUE NOT NULL
        );
    """)
    conn.commit()
    conn.close()

def add_to_watchlist(ticker):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT OR IGNORE INTO watchlist (ticker) VALUES (?);", (ticker,))
    conn.commit()
    conn.close()

def remove_from_watchlist(ticker):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM watchlist WHERE ticker = ?;", (ticker,))
    conn.commit()
    conn.close()

def get_watchlist():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT ticker FROM watchlist;")
    tickers = cursor.fetchall()
    conn.close()
    return [ticker[0] for ticker in tickers]

def delete_invalid_ticker(ticker):
    """ Entfernt ungültige Ticker aus der Watchlist """
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM watchlist WHERE ticker = ?;", (ticker,))
    conn.commit()
    conn.close()

def clear_watchlist():
    """ Löscht alle Ticker in der Watchlist """
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM watchlist;")
    conn.commit()
    conn.close()

# 🌐 Seite und Eingabe für Ticker
create_watchlist_table()

# Eingabe für neue Aktie
ticker_input = st.text_input('Geben Sie das Ticker Symbol ein (z. B. TSLA für Tesla):')

if st.button("➕ Zur Watchlist hinzufügen"):
    if ticker_input:
        add_to_watchlist(ticker_input)
        st.success(f"'{ticker_input}' wurde zur Watchlist hinzugefügt!")

# 📋 Anzeige der Watchlist
st.markdown("---")

# Hinzufügen des Buttons zum Löschen der Watchlist oben rechts
if st.button("🗑️ Watchlist löschen", key="clear_watchlist"):
    clear_watchlist()
    st.success("Die gesamte Watchlist wurde gelöscht!")
    st.experimental_rerun()  # Seite neu laden nach dem Löschen

watchlist = get_watchlist()

if watchlist:
    st.subheader("📋 Ihre Watchlist:")
    for ticker in watchlist:
        try:
            aktie = yf.Ticker(ticker)
            info = aktie.info
            
            if info is None:
                st.error(f"⚠️ Keine Daten verfügbar für {ticker}. Entferne aus der Watchlist...")
                delete_invalid_ticker(ticker)  # Ungültigen Ticker entfernen
                continue

            unternehmen = info.get("longName", "Unbekannt")
            preis = info.get("currentPrice", "—")
            
            # Anzeige in einer Tabelle mit clickable Ticker
            row = st.columns([1, 3, 4, 3, 1])

            # View-Auge-Symbol für "View"
            with row[0]:
                if st.button(f"👁️", key=f"view_{ticker}"):
                    st.session_state.selected_ticker = ticker

            with row[1]:
                st.write(ticker.upper())

            with row[2]:
                st.write(unternehmen)

            with row[3]:
                st.write(f"{preis} USD")

            # Entfernen-Button
            with row[4]:
                if st.button(f"🗑️", key=f"remove_{ticker}"):
                    remove_from_watchlist(ticker)
                    st.rerun()  # Seite neu laden nach dem Entfernen der Aktie

        except Exception as e:
            st.error(f"⚠️ Fehler bei {ticker}")
            st.exception(e)

else:
    st.info("🔍 Fügen Sie Aktien zur Watchlist hinzu, um sie hier anzuzeigen.")

# 📊 Details für ausgewählte Aktie anzeigen
if "selected_ticker" in st.session_state:
    ticker = st.session_state.selected_ticker
    try:
        # Daten von der API
        aktie = yf.Ticker(ticker)
        info = aktie.info
        
        if info is None:
            st.error(f"⚠️ Keine Daten verfügbar für {ticker}. Bitte überprüfen Sie das Ticker-Symbol.")
        else:
            unternehmen = info.get("longName", ticker)
            beschreibung = info.get("longBusinessSummary", "Keine Beschreibung verfügbar.")
            preis = info.get("currentPrice", "—")

            st.markdown("---")
            st.subheader(f"📌 {unternehmen} ({ticker.upper()}) — Aktueller Kurs: {preis} USD")

            # Kursgrafik für das letzte Jahr
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

            # Unternehmensbeschreibung übersetzen
            beschreibung_de = GoogleTranslator(source='auto', target='de').translate(beschreibung)
            with st.expander("📄 Unternehmensbeschreibung anzeigen"):
                st.write(beschreibung_de)

    except Exception as e:
        st.error(f"⚠️ Fehler beim Abrufen der Daten für {ticker}.")
        st.exception(e)

