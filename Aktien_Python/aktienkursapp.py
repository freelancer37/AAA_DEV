import streamlit as st
import yfinance as yf
import plotly.graph_objects as go
from deep_translator import GoogleTranslator

st.title('Aktienkurs Abfrage')

#Eingabe Aktienticker
ticker = st.text_input('Geben Sie das Ticker Symbol ein: (z.b. TSLA für Tesla)')

#Button Suche 
if st.button('Suche starten'):
    #Daten Lesen
    aktie = yf.Ticker(ticker)

    #Aktien Informationen aufbereiten
    info = aktie.info
    unternehmen = info['longName']
    beschreibung = info['longBusinessSummary']
    preis = info['currentPrice']

    #Anzeige Aktienname und aktueller Kurs
    st.subheader(f"{unternehmen} ({ticker}) ---  Aktueller Kurs: {preis}")
                      
    #Information für Grafik
    daten = aktie.history(period='1y')
    angezeigte_daten = daten.loc[daten.index > '2024-01-01']

    #Erstellung der Grafik
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=angezeigte_daten.index, y=angezeigte_daten['Close'], name='Kurs'))
    fig.update_layout(title=f'{unternehmen} ({ticker})', xaxis_title='Datum', yaxis_title='Kurs in Landeswährung')
    st.plotly_chart(fig)

    #Übersetzung der Beschreibung
    beschreibung_de = GoogleTranslator(source='auto', target='de').translate(beschreibung)

    #Zeige die Informationen an
    st.subheader(f"{unternehmen}")
    st.write(beschreibung_de)
 



