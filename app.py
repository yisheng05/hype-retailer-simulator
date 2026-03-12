import streamlit as st
import pandas as pd
import numpy as np
import time
import plotly.express as px
import plotly.graph_objects as go

# Configuration
st.set_page_config(page_title="Hype Retailer Simulator", layout="wide", page_icon="👟")

# --- Session State Initialization ---
if 'phase' not in st.session_state:
    st.session_state.phase = "Pre-Drop"
if 'product_name' not in st.session_state:
    st.session_state.product_name = "Limited Edition Sneaker v1"
if 'scarcity' not in st.session_state:
    st.session_state.scarcity = 500  # Total Units
if 'marketing_budget' not in st.session_state:
    st.session_state.marketing_budget = 5000
if 'hype_score' not in st.session_state:
    st.session_state.hype_score = 0
if 'waitlist' not in st.session_state:
    st.session_state.waitlist = []
if 'drop_results' not in st.session_state:
    st.session_state.drop_results = None

# --- Helper Functions ---
def reset_simulation():
    for key in st.session_state.keys():
        del st.session_state[key]
    st.rerun()

# --- Title and Header ---
st.title("🔥 Hype Retailer Workflow Simulator")
st.markdown("---")

# --- Navigation (Sidebar) ---
with st.sidebar:
    st.header("Simulation Control")
    st.write(f"**Current Phase:** {st.session_state.phase}")
    if st.button("Reset Simulation"):
        reset_simulation()
    
    st.info("Experience the lifecycle of a high-demand product launch.")

# --- Phase 1: Pre-Drop ---
if st.session_state.phase == "Pre-Drop":
    st.header("1. Pre-Drop Phase: Building Hype & Scarcity")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Configure Product")
        st.session_state.product_name = st.text_input("Product Name", st.session_state.product_name)
        st.session_state.scarcity = st.slider("Scarcity (Total Units)", 50, 2000, 500)
        st.session_state.marketing_budget = st.slider("Marketing Budget ($)", 1000, 50000, 5000)
        
        st.markdown("### 📈 Marketing Activities")
        m_influencer = st.checkbox("Hire Influencers", value=True)
        m_waitlist = st.checkbox("Launch SMS Waitlist", value=True)
        m_social = st.checkbox("Social Media Teaser Ads", value=True)
        
        # Calculate Hype
        base_hype = (st.session_state.marketing_budget / 500) + (2000 / st.session_state.scarcity)
        if m_influencer: base_hype *= 1.5
        if m_waitlist: base_hype *= 1.2
        if m_social: base_hype *= 1.3
        
        st.session_state.hype_score = round(base_hype, 2)
        st.metric("Estimated Hype Score", st.session_state.hype_score)

    with col2:
        st.subheader("Waitlist Growth Simulation")
        # Generate some mock waitlist data based on hype
        days = np.arange(1, 15)
        waitlist_growth = np.exp(days * (st.session_state.hype_score / 20)) * 10
        df_waitlist = pd.DataFrame({"Day": days, "Signups": waitlist_growth.astype(int)})
        
        fig = px.line(df_waitlist, x="Day", y="Signups", title="Waitlist Accumulation")
        st.plotly_chart(fig, use_container_width=True)
        
        st.session_state.waitlist_count = int(df_waitlist["Signups"].iloc[-1])
        st.success(f"Waitlist: {st.session_state.waitlist_count} potential customers ready.")

    if st.button("🚀 Proceed to The Drop"):
        st.session_state.phase = "The Drop"
        st.rerun()

# --- Phase 2: The Drop ---
elif st.session_state.phase == "The Drop":
    st.header("2. The Launch: 'The Drop'")
    
    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.subheader("Launch Configuration")
        anti_bot = st.select_slider("Anti-Bot Protection Level", options=["None", "Standard", "Advanced (Akamai Style)"])
        sale_type = st.radio("Sale Model", ["FCFS (First-Come, First-Served)", "Raffle"])
        
        if st.button("🔥 START DROP"):
            with st.spinner("Processing surge traffic and filtering bots..."):
                progress_bar = st.progress(0)
                # Traffic Simulation
                total_req = st.session_state.waitlist_count * 5
                bot_percentage = 0.8 if anti_bot == "None" else (0.3 if anti_bot == "Standard" else 0.05)
                
                # Mock high-volume traffic
                traffic_data = []
                for i in range(100):
                    time.sleep(0.02)
                    traffic_data.append(np.random.poisson(total_req/100))
                    progress_bar.progress(i + 1)
                
                # Logic for sales
                potential_buyers = st.session_state.waitlist_count
                bots_detected = int(total_req * bot_percentage)
                legit_attempts = total_req - bots_detected
                
                units_sold = min(st.session_state.scarcity, int(legit_attempts / 10))
                
                st.session_state.drop_results = {
                    "total_traffic": total_req,
                    "bots_blocked": bots_detected,
                    "units_sold": units_sold,
                    "sell_out_time": "12.4 seconds" if units_sold == st.session_state.scarcity else "N/A",
                    "traffic_history": traffic_data
                }
            st.success("Drop Complete!")

    with col2:
        if st.session_state.drop_results:
            st.subheader("Live Traffic Analysis")
            res = st.session_state.drop_results
            
            # Traffic Spike Chart
            fig = px.area(y=res["traffic_history"], title="Real-time Request Volume (ms)")
            fig.update_layout(xaxis_title="Time", yaxis_title="Requests/ms")
            st.plotly_chart(fig, use_container_width=True)
            
            c1, c2, c3 = st.columns(3)
            c1.metric("Total Requests", f"{res['total_traffic']:,}")
            c2.metric("Bots Filtered", f"{res['bots_blocked']:,}")
            c3.metric("Units Sold", f"{res['units_sold']}/{st.session_state.scarcity}")
            
            if st.button("📊 Go to Post-Drop Analysis"):
                st.session_state.phase = "Post-Drop"
                st.rerun()
        else:
            st.info("Configure your launch settings and press 'START DROP' to simulate the event.")

# --- Phase 3: Post-Drop ---
elif st.session_state.phase == "Post-Drop":
    st.header("3. Post-Drop Phase: Fulfillment & Data Analysis")
    
    if not st.session_state.drop_results:
        st.warning("Please complete 'The Drop' phase first.")
    else:
        res = st.session_state.drop_results
        
        # Financial Summary
        unit_price = 220
        total_revenue = res["units_sold"] * unit_price
        profit = total_revenue - st.session_state.marketing_budget - (res["units_sold"] * 80) # COGS 80
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("Financial Performance")
            st.metric("Total Revenue", f"${total_revenue:,}")
            st.metric("Net Profit", f"${profit:,}")
            
            # StockX Prediction
            resale_mult = 1.0 + (st.session_state.hype_score / 100)
            predicted_resale = unit_price * resale_mult
            st.markdown(f"### 📈 Secondary Market (StockX Prediction)")
            st.info(f"Predicted Resale Value: **${predicted_resale:,.2f}**")
            
        with col2:
            st.subheader("Customer Sentiment")
            sentiment = "Positive" if res["bots_blocked"] > (res["total_traffic"] * 0.5) else "Negative (Bot Complaints)"
            st.write(f"**Brand Health:** {sentiment}")
            
            # Mock shipping progress
            st.write("**Fulfillment Pipeline:**")
            st.progress(100)
            st.caption("All orders verified and pushed to warehouse API.")
            
        st.markdown("---")
        st.subheader("Workflow Insights")
        st.write("""
        1. **AI Demand Forecasting:** The waitlist size correctly predicted the 100x traffic surge.
        2. **Edge AI:** Real-time bot detection saved product for genuine customers.
        3. **Omnichannel:** Inventory successfully synced across digital and physical fulfillment centers.
        """)
        
        if st.button("🔄 Start New Cycle"):
            reset_simulation()
