import streamlit as st
import sqlite3
import yfinance as yf
import plotly.graph_objects as go
from deep_translator import GoogleTranslator

# Verbindung zur SQLite-Datenbank
def get_db_connection():
    conn = sqlite3.connect('watchlist.db')  # Dateiname der SQLite-Datenbank
    return conn

# Tabelle für die Watchlist erstellen, falls sie nicht existiert
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

# Funktion zum Hinzufügen eines Tickers zur Datenbank
def add_to_watchlist(ticker):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT OR IGNORE INTO watchlist (ticker) VALUES (?);", (ticker,))
    conn.commit()
    conn.close()

# Funktion zum Entfernen eines Tickers aus der Datenbank
def remove_from_watchlist(ticker):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM watchlist WHERE ticker = ?;", (ticker,))
    conn.commit()
    conn.close()

# Funktion zum Abrufen der Watchlist aus der Datenbank
def get_watchlist():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT ticker FROM watchlist;")
    tickers = cursor.fetchall()
    conn.close()
    return [ticker[0] for ticker in tickers]

# 🌐 Seitenlayout & Titel
st.set_page_config(page_title="📈 Aktienkurs App", layout="centered")

# 📌 App-Titel
st.title('📈 Aktienkurs Watchlist')

# 📚 Datenbank und Watchlist initialisieren
create_watchlist_table()

# 📬 Eingabe für neue Aktie
ticker_input = st.text_input('Geben Sie das Ticker Symbol ein (z. B. TSLA für Tesla):')

if st.button("➕ Zur Watchlist hinzufügen"):
    if ticker_input:
        add_to_watchlist(ticker_input)
        st.success(f"'{ticker_input}' wurde zur Watchlist hinzugefügt!")

# 📋 Tabelle anzeigen
watchlist = get_watchlist()
if watchlist:
    st.subheader("📋 Ihre Watchlist:")
    for ticker in watchlist:
        try:
            aktie = yf.Ticker(ticker)
            info = aktie.info
            unternehmen = info.get("longName", "Unbekannt")
            preis = info.get("currentPrice", "—")
            
            st.write(f"{ticker.upper()} - {unternehmen} - {preis} USD")

            # Daten entfernen (Papierkorb)
            if st.button(f"🗑️ Entfernen", key=f"remove_{ticker}"):
                remove_from_watchlist(ticker)
                st.success(f"'{ticker}' wurde aus der Watchlist entfernt!")

        except Exception as e:
            st.error(f"⚠️ Fehler bei {ticker}")
            st.exception(e)
else:
    st.info("🔍 Fügen Sie Aktien zur Watchlist hinzu, um sie hier anzuzeigen.")
