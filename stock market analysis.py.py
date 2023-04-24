# Import necessary libraries
import streamlit as st
import pandas as pd
import yfinance as yf
import plotly.graph_objs as go
import plotly.express as px
from datetime import date, timedelta

# Set app title
st.title("Stock Market Analysis Tool")

# Define function to download stock data
@st.cache
def download_data(ticker, start_date, end_date):
    data = yf.download(ticker, start=start_date, end=end_date)
    data.reset_index(inplace=True)
    return data

# Define function to plot stock data
def plot_data(data, ticker):
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=data['Date'], y=data['Close'], name="Close"))
    fig.add_trace(go.Scatter(x=data['Date'], y=data['Open'], name="Open"))
    fig.add_trace(go.Scatter(x=data['Date'], y=data['High'], name="High"))
    fig.add_trace(go.Scatter(x=data['Date'], y=data['Low'], name="Low"))
    fig.update_layout(title=ticker + " Stock Prices",
                      xaxis_title="Date",
                      yaxis_title="Price (USD)",
                      template="plotly_dark")
    st.plotly_chart(fig)

# Define function to calculate simple moving average
def simple_moving_average(data, window):
    sma = data['Close'].rolling(window=window).mean()
    return sma

# Define function to plot simple moving average
def plot_sma(data, ticker, window):
    sma = simple_moving_average(data, window)
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=data['Date'], y=data['Close'], name="Close"))
    fig.add_trace(go.Scatter(x=data['Date'], y=sma, name="SMA (" + str(window) + " days)"))
    fig.update_layout(title=ticker + " Stock Prices",
                      xaxis_title="Date",
                      yaxis_title="Price (USD)",
                      template="plotly_dark")
    st.plotly_chart(fig)

# Define function to calculate relative strength index
def relative_strength_index(data, window):
    delta = data['Close'].diff()
    gain = delta.copy()
    loss = delta.copy()
    gain[gain < 0] = 0
    loss[loss > 0] = 0
    avg_gain = gain.rolling(window=window).mean().abs()
    avg_loss = loss.rolling(window=window).mean().abs()
    rs = avg_gain / avg_loss
    rsi = 100 - (100 / (1 + rs))
    return rsi

# Define function to plot relative strength index
def plot_rsi(data, ticker, window):
    rsi = relative_strength_index(data, window)
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=data['Date'], y=rsi, name="RSI (" + str(window) + " days)"))
    fig.update_layout(title=ticker + " Relative Strength Index",
                      xaxis_title="Date",
                      yaxis_title="RSI",
                      template="plotly_dark")
    fig.add_shape(type='line',
                  x0=data['Date'].min(),
                  y0=30,
                  x1=data['Date'].max(),
                  y1=30,
                  line=dict(color='red', width=1, dash='dot'))
    fig.add_shape(type='line',
                  x0=data['Date'].min(),
                  y0=70,
                  x1=data['Date'].max(),
                  y1=70)
