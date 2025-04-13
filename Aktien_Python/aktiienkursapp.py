import streamlit as st
import yfinance as yf
import plotly.graph_objects as go
from googletrans import Translator

st.title('Aktienkurs Abfrage')

ticker = st.text_input('Geben Sie das Ticker Symbol ein:')

