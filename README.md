# Hype Retailer Workflow Simulator

A Streamlit-powered web application that simulates the high-stakes operational workflow of a hype-driven retailer (sneakers, streetwear, limited collectibles).

## 🚀 Overview

This simulator follows the three key phases of a "Hype Drop":
1.  **Pre-Drop:** Manage scarcity, set marketing budgets, and watch your waitlist grow.
2.  **The Drop:** Launch the product, manage high-volume traffic surges, and implement anti-bot protection (Akamai-style).
3.  **Post-Drop:** Analyze financial performance, fulfillment efficiency, and secondary market (StockX) price predictions.

## 🛠️ Tech Stack
- **Frontend/Backend:** Streamlit
- **Visualization:** Plotly, Pandas
- **Simulation Logic:** Numpy (Stochastic traffic modeling)

## 📦 Installation

1.  **Clone the repo:**
    ```bash
    git clone <repo-url>
    cd hype-retailer-simulator
    ```

2.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

3.  **Run the app:**
    ```bash
    streamlit run app.py
    ```

## 📖 Key Features
- **Hype Scoring:** Dynamic calculation based on scarcity and marketing effort.
- **Traffic Spikes:** Real-time simulation of request volume during the drop.
- **Bot Detection:** Adjustable protection levels that affect customer sentiment and sell-out success.
- **Resale Prediction:** Algorithmically estimates secondary market value based on launch hype.
