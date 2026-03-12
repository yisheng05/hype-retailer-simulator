# 👟 Hype Retailer Workflow Simulator

A high-fidelity **Streamlit** application designed to simulate the complex, high-pressure operational lifecycle of a "Hype Retailer"—businesses like Supreme, Nike, or StockX that thrive on artificial scarcity, viral marketing, and explosive "drop" events.

---

## 📖 Project Concept
This simulator replicates the business model of modern high-demand retail, where success is measured in milliseconds and "Hype" is a quantifiable metric driven by data intelligence, social velocity, and supply manipulation.

---

## 🕹️ Detailed Simulation Logic & Formulas

### 1. Market Intelligence & Curation Strategy
The simulation prioritizes **TikTok** as the primary intelligence signal due to its superior **viral discovery velocity** (hashtag growth and audio trends) compared to follower-based platforms like Instagram.

*   **Intelligence Score ($I$):**
    $$I = Trend\_Multiplier \times Influencer\_Multiplier \times (1 + \frac{Search\_Volume}{100})$$
    *   *Trend Multipliers:* Low (0.8x) to Explosive (2.5x).
    *   *Influencer Multipliers:* Organic (1.0x) to Elite (2.0x).
    *   *Search Intent:* A linear factor (0-100 index).

### 2. The Hype Equation ($H$)
The final **Aggregate Hype Score** is a product of supply, investment, and curation intelligence:
$$H = \left( \frac{Marketing\_Budget}{500} + \frac{2000}{Scarcity} \right) \times I \times Activity\_Boosts$$
*   **Scarcity Rule:** Lower supply exponentially increases the base hype.
*   **Activity Boosts:** Execute Influencer Campaign (1.5x), SMS Waitlist (1.2x), Social Teasers (1.3x).

### 3. Traffic & Bot Modeling
*   **Traffic Spike:** Uses **Stochastic Poisson modeling** to simulate 100x traffic surges based on the final waitlist size.
*   **Bot Detection:** Filters traffic based on selected "Edge AI" protection levels:
    *   *None:* 80% Bots
    *   *Standard:* 30% Bots
    *   *Advanced (Akamai-style):* 5% Bots

### 4. Financial P&L Breakdown
The simulator calculates profitability using a standard retail model:
*   **Actual Revenue:** $Units\_Sold \times Unit\_Price$
*   **COGS (Cost of Goods Sold):** Modeled at **40% of the Unit Price** per unit sold.
*   **Net Profit:** $Actual\ Revenue - Marketing\ Budget - COGS$

### 5. StockX Prediction Model
The "StockX Prediction" is a heuristic proxy mimicking real-world secondary market behavior:
$$Predicted\ Resale = Unit\_Price \times \left(1.0 + \frac{Hype\ Score}{100}\right)$$
This reflects how high social demand ($H$) and limited supply ($Scarcity$) drive market premiums on platforms like StockX.

---

## 📊 User Interface Features
- **Large Number Formatting:** All metrics are rounded to the nearest Million (M), Hundred Thousand, or Thousand (K) for high-fidelity readability.
- **Full-Width Analytics:** The "Drop" results switch to a wide-screen dashboard view to prevent metric truncation and simulate a command center.
- **Dynamic Charting:** Interactive Plotly charts show waitlist accumulation and millisecond-level traffic spikes.

---

## 📦 Installation & Setup (Safe Mode)

To ensure a clean environment, use the provided virtual environment setup:

1.  **Clone the Repository:**
    ```bash
    git clone <repository-url>
    cd hype-retailer-simulator
    ```

2.  **Create and Activate Virtual Environment:**
    ```bash
    python3 -m venv venv
    source venv/bin/activate  # On Windows: venv\Scripts\activate
    ```

3.  **Install Dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Launch the Simulator:**
    ```bash
    streamlit run app.py
    ```

---

## 🚀 Future Roadmap
- [ ] **Multi-Product Drops:** Manage a portfolio of products simultaneously.
- [ ] **Dynamic Pricing AI:** Adjust prices in real-time based on waitlist growth.
- [ ] **Global Region Support:** Simulate latency across different continents.

---

*Built by Gemini CLI.*
