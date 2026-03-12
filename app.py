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
if 'unit_price' not in st.session_state:
    st.session_state.unit_price = 220
if 'marketing_budget' not in st.session_state:
    st.session_state.marketing_budget = 5000
if 'hype_score' not in st.session_state:
    st.session_state.hype_score = 0
if 'waitlist' not in st.session_state:
    st.session_state.waitlist = []
if 'drop_results' not in st.session_state:
    st.session_state.drop_results = None

# --- Helper Functions ---
def format_large_number(num):
    if num >= 1_000_000:
        return f"{num / 1_000_000:.1f}M".replace('.0M', 'M')
    elif num >= 1_000:
        return f"{num / 1_000:.1f}K".replace('.0K', 'K')
    return str(num)

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
    
    # --- Trend Monitoring & Curation Section ---
    with st.expander("🔍 Trend Monitoring & Curation Dashboard", expanded=True):
        st.subheader("Market Intelligence Signals")
        t1, t2, t3 = st.columns(3)
        
        with t1:
            st.markdown("### 📱 TikTok Velocity")
            tiktok_trend = st.select_slider("TikTok Trend Strength", options=["Low", "Growing", "Viral", "Explosive"], value="Growing")
            st.caption("Monitoring hashtag velocity and audio clip usage.")
            
        with t2:
            st.markdown("### 🤝 Influencer Pulse")
            influencer_tier = st.selectbox("Curation Strategy", ["Organic/Micro", "Boutique/Seed", "Elite/A-List"])
            st.caption("Tracking engagement rates vs follower counts.")
            
        with t3:
            st.markdown("### 🔎 Search Intent")
            search_volume = st.slider("Search Index (Google/Pinterest)", 0, 100, 45)
            st.caption("Analyzing intent-based search queries.")

        # Intelligence Multiplier Logic
        trend_mult = {"Low": 0.8, "Growing": 1.2, "Viral": 1.8, "Explosive": 2.5}[tiktok_trend]
        influencer_mult = {"Organic/Micro": 1.0, "Boutique/Seed": 1.3, "Elite/A-List": 2.0}[influencer_tier]
        search_mult = 1 + (search_volume / 100)
        
        intelligence_score = round(trend_mult * influencer_mult * search_mult, 2)
        st.info(f"**Curation Intelligence Score:** {intelligence_score}x (Affects hype effectiveness)")

    st.markdown("---")
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Configure Product")
        st.session_state.product_name = st.text_input("Product Name", st.session_state.product_name)
        st.session_state.scarcity = st.slider("Scarcity (Total Units)", 50, 2000, 500)
        st.session_state.unit_price = st.number_input("Unit Price ($)", 50, 2000, st.session_state.unit_price)
        st.session_state.marketing_budget = st.slider("Marketing Budget ($)", 1000, 50000, 5000)
        
        # Projected Revenue
        projected_rev = st.session_state.scarcity * st.session_state.unit_price
        st.write(f"**Projected Sell-out Revenue:** ${format_large_number(projected_rev)}")
        
        st.markdown("### 📈 Marketing Activities")
        m_influencer = st.checkbox("Execute Influencer Campaign", value=True)
        m_waitlist = st.checkbox("Launch SMS Waitlist", value=True)
        m_social = st.checkbox("Social Media Teaser Ads", value=True)
        
        # Calculate Hype with Intelligence Score
        base_hype = ((st.session_state.marketing_budget / 500) + (2000 / st.session_state.scarcity)) * intelligence_score
        if m_influencer: base_hype *= 1.5
        if m_waitlist: base_hype *= 1.2
        if m_social: base_hype *= 1.3
        
        st.session_state.hype_score = round(base_hype, 2)
        st.metric("Aggregate Hype Score", st.session_state.hype_score, delta=f"{intelligence_score}x intelligence")

    with col2:
        st.subheader("Waitlist Growth Simulation")
        # Generate some mock waitlist data based on hype
        days = np.arange(1, 15)
        waitlist_growth = np.exp(days * (st.session_state.hype_score / 20)) * 10
        df_waitlist = pd.DataFrame({"Day": days, "Signups": waitlist_growth.astype(int)})
        
        fig = px.line(df_waitlist, x="Day", y="Signups", title="Waitlist Accumulation")
        st.plotly_chart(fig, use_container_width=True)
        
        st.session_state.waitlist_count = int(df_waitlist["Signups"].iloc[-1])
        st.success(f"Waitlist: {format_large_number(st.session_state.waitlist_count)} potential customers ready.")

    if st.button("🚀 Proceed to The Drop"):
        st.session_state.phase = "The Drop"
        st.rerun()

# --- Phase 2: The Drop ---
elif st.session_state.phase == "The Drop":
    st.header("2. The Launch: 'The Drop'")
    
    # Configuration Section (Only show if not dropped, or in smaller column)
    if not st.session_state.drop_results:
        col1, col2 = st.columns([1, 2])
        with col1:
            st.subheader("Launch Configuration")
            anti_bot = st.select_slider("Anti-Bot Protection Level", options=["None", "Standard", "Advanced (Akamai Style)"])
            sale_type = st.radio("Sale Model", ["FCFS (First-Come, First-Served)", "Raffle"])
            
            if st.button("🔥 START DROP"):
                with st.spinner("Processing surge traffic and filtering bots..."):
                    progress_bar = st.progress(0)
                    total_req = st.session_state.waitlist_count * 5
                    bot_percentage = 0.8 if anti_bot == "None" else (0.3 if anti_bot == "Standard" else 0.05)
                    
                    traffic_data = []
                    for i in range(100):
                        time.sleep(0.01)
                        traffic_data.append(np.random.poisson(total_req/100))
                        progress_bar.progress(i + 1)
                    
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
                st.rerun()

        with col2:
            st.info("Configure your launch settings and press 'START DROP' to simulate the event.")
    else:
        # Full-Width Results Display
        st.subheader("🚀 Drop Analytics Dashboard")
        res = st.session_state.drop_results
        
        # Key Metrics Row
        with st.container(border=True):
            m1, m2, m3, m4 = st.columns(4)
            m1.metric("Total Requests", format_large_number(res['total_traffic']))
            m2.metric("Bots Filtered", format_large_number(res['bots_blocked']))
            # Formatted units for extra safety
            sold_f = format_large_number(res['units_sold'])
            total_f = format_large_number(st.session_state.scarcity)
            m3.metric("Inventory Cleared", f"{sold_f} / {total_f}")
            m4.metric("Sell-out Status", "SUCCESS" if res['units_sold'] == st.session_state.scarcity else "PARTIAL")

        col_left, col_right = st.columns([2, 1])
        with col_left:
            st.markdown("### 📊 Real-Time Traffic Spike (ms)")
            fig = px.area(y=res["traffic_history"])
            fig.update_layout(xaxis_title="Time Interval", yaxis_title="Requests", margin=dict(l=0, r=0, t=20, b=0))
            st.plotly_chart(fig, use_container_width=True)
            
        with col_right:
            st.markdown("### ⚡ Infrastructure Status")
            st.success("Edge Network: Stable")
            st.success("DB Connection: Normal")
            st.write(f"**Final Sell-out Time:** {res['sell_out_time']}")
            
            if st.button("📈 View Financial Analysis"):
                st.session_state.phase = "Post-Drop"
                st.rerun()

# --- Phase 3: Post-Drop ---
elif st.session_state.phase == "Post-Drop":
    st.header("3. Post-Drop Phase: Fulfillment & Data Analysis")
    
    if not st.session_state.drop_results:
        st.warning("Please complete 'The Drop' phase first.")
    else:
        res = st.session_state.drop_results
        
        # Financial Summary
        actual_revenue = res["units_sold"] * st.session_state.unit_price
        # Profit for context (optional, but moved down)
        profit = actual_revenue - st.session_state.marketing_budget - (res["units_sold"] * (st.session_state.unit_price * 0.4)) # COGS ~40%
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("Financial Performance")
            st.metric("Actual Revenue", f"${format_large_number(actual_revenue)}")
            st.write(f"*Calculation: {format_large_number(res['units_sold'])} units sold @ ${st.session_state.unit_price} each*")
            
            # StockX Prediction
            resale_mult = 1.0 + (st.session_state.hype_score / 100)
            predicted_resale = st.session_state.unit_price * resale_mult
            st.markdown(f"### 📈 Secondary Market (StockX Prediction)")
            st.info(f"Predicted Resale Value: **${predicted_resale:,.2f}**")
            
        with col2:
            st.subheader("Business Metrics")
            st.metric("Net Profit", f"${format_large_number(profit)}")
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
