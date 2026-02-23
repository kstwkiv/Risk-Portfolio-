import streamlit as st
import requests
import matplotlib.pyplot as plt

API_URL = "http://127.0.0.1:8000"

st.title("Live Portfolio Risk Dashboard")
    
# ---- Portfolio Creation ----

st.header("Create Portfolio")

portfolio_name = st.text_input("Portfolio Name")
tickers_input = st.text_input("Tickers (comma separated)", "AAPL,MSFT,GOOGL")
weights_input = st.text_input("Weights (comma separated)", "0.4,0.4,0.2")

if st.button("Create Portfolio"):
    tickers = [t.strip() for t in tickers_input.split(",")]
    weights = [float(w.strip()) for w in weights_input.split(",")]

    assets = [{"ticker": t, "weight": w} for t, w in zip(tickers, weights)]

    response = requests.post(
        f"{API_URL}/portfolio",
        json={"name": portfolio_name, "assets": assets}
    )

    if response.status_code == 200:
        st.success(f"Portfolio Created! ID: {response.json()['portfolio_id']}")
    else:
        st.error("Error creating portfolio")


# ---- Risk Calculation ----

st.header("Calculate Risk")

portfolio_id = st.number_input("Portfolio ID", min_value=1, step=1)

if st.button("Calculate Risk Metrics"):
    response = requests.get(f"{API_URL}/risk/{int(portfolio_id)}")

    if response.status_code == 200:
        data = response.json()

        st.metric("Annualized Volatility", data["volatility"])
        st.metric("Historical VaR (95%)", data["var_95"])
        st.metric("Monte Carlo VaR (95%)", data["monte_carlo_var"])
        st.metric("Beta vs S&P 500", data["beta"])
    else:
        st.error("Error fetching risk metrics")


# ---- Rolling Risk ----

st.header("Rolling Risk (Last 30 Days)")

if st.button("Show Rolling Risk"):
    response = requests.get(f"{API_URL}/rolling-risk/{int(portfolio_id)}")

    if response.status_code == 200:
        data = response.json()

        vol_values = list(data["rolling_volatility"].values())
        var_values = list(data["rolling_var"].values())

        fig, ax = plt.subplots()
        ax.plot(vol_values, label="Rolling Volatility")
        ax.plot(var_values, label="Rolling VaR")
        ax.legend()
        st.pyplot(fig)
    else:
        st.error("Error fetching rolling risk")