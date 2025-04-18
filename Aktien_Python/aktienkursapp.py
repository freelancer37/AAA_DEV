import streamlit as st
import yfinance as yf
import plotly.graph_objects as go
from deep_translator import GoogleTranslator

# 🌐 Seitenlayout & Titel
st.set_page_config(page_title="Aktienkurs App", layout="centered")
st.title('📈 Aktienkurs Abfrage')

# 🌗 Hell-/Dunkelmodus mit Session-State
if "theme_mode" not in st.session_state:
    st.session_state.theme_mode = "Hell"

with st.sidebar:
    st.session_state.theme_mode = st.selectbox("🌗 Darstellungsmodus:", ["Hell", "Dunkel"], 
                                               index=["Hell", "Dunkel"].index(st.session_state.theme_mode))

# 💡 Funktion: CSS für Dunkelmodus anwenden
def apply_dark_mode():
    st.markdown("""
        <style>
            body, .stApp {
                background-color: #0e1117;
                color: #fafafa;
            }
            .stTextInput > div > div > input {
                background-color: #1e222b;
                color: #fafafa;
            }
            .css-1v3fvcr, .css-1d391kg, .stMarkdown {
                color: #fafafa !important;
            }
            .stButton button {
                background-color: #444;
                color: white;
            }
        </style>
        """, unsafe_allow_html=True)

if st.session_state.theme_mode == "Dunkel":
    apply_dark_mode()

# 📬 Eingabe Aktienticker
ticker = st.text_input('Geben Sie das Ticker Symbol ein: (z.B. TSLA für Tesla)')

# 🔍 Button Suche starten
if st.button('🔎 Suche starten') and ticker:
    try:
        aktie = yf.Ticker(ticker)
        info = aktie.info
        unternehmen = info['longName']
        beschreibung = info['longBusinessSummary']
        preis = info['currentPrice']

        st.subheader(f"{unternehmen} ({ticker.upper()}) — Aktueller Kurs: {preis} USD")

        # 📊 Kursverlauf (responsive)
        daten = aktie.history(period='1y')
        angezeigte_daten = daten.loc[daten.index > '2024-01-01']

        fig = go.Figure()
        fig.add_trace(go.Scatter(x=angezeigte_daten.index, y=angezeigte_daten['Close'], name='Kurs'))
        fig.update_layout(title=f'{unternehmen} ({ticker.upper()})', 
                          xaxis_title='Datum', 
                          yaxis_title='Kurs in USD')
        st.plotly_chart(fig, use_container_width=True)

        # 🌍 Übersetzung mit deep_translator
        beschreibung_de = GoogleTranslator(source='auto', target='de').translate(beschreibung)

        # 📄 Unternehmensbeschreibung als aufklappbarer Text
        with st.expander("📄 Unternehmensbeschreibung anzeigen"):
            st.write(beschreibung_de)

    except Exception as e:
        st.error("


