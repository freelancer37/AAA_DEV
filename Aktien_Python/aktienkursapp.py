import streamlit as st
import yfinance as yf
import plotly.graph_objects as go
from deep_translator import GoogleTranslator

# 🌐 Seitenlayout & Titel
st.set_page_config(page_title="📈 Aktienkurs App", layout="centered")

# 🎨 Initialisiere Theme-Session
if "theme_mode" not in st.session_state:
    st.session_state.theme_mode = "Hell"

# 🌗 Kleiner Umschaltbutton oben rechts
col1, col2 = st.columns([9, 1])
with col2:
    toggle_label = "🌞" if st.session_state.theme_mode == "Dunkel" else "🌙"
    if st.button(toggle_label, help="Darstellungsmodus wechseln"):
        st.session_state.theme_mode = "Hell" if st.session_state.theme_mode == "Dunkel" else "Dunkel"

# 💡 CSS für Dunkelmodus
def apply_dark_mode():
    st.markdown("""
        <style>
            html, body, [class^="css"] {
                background-color: #0e1117 !important;
                color: #fafafa !important;
            }
            .stTextInput > div > div > input {
                background-color: #1e222b !important;
                color: #fafafa !important;
            }
            .stButton button {
                background-color: #444 !important;
                color: white !important;
            }
            .stSelectbox > div {
                background-color: #1e222b !important;
                color: #fafafa !important;
            }
            .stSidebar {
                background-color: #0e1117 !important;
            }
        </style>
        """, unsafe_allow_html=True)

if st.session_state.theme_mode == "Dunkel":
    apply_dark_mode()

# 📌 App-Titel
st.title('📈 Aktienkurs Abfrage')

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

        # 📊 Kursverlauf mit passendem Plotly-Theme
        daten = aktie.history(period='1y')
        angezeigte_daten = daten.loc[daten.index > '2024-01-01']

        fig = go.Figure(layout=dict(template='plotly_dark' if st.session_state.theme_mode == 'Dunkel' else 'plotly'))
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
        st.error("⚠️ Leider konnten die Daten nicht abgerufen werden. Bitte überprüfe das Ticker-Symbol.")
        st.exception(e)
