import streamlit as st
from pytrends.request import TrendReq
import pandas as pd
import time
import feedparser

# 1. Setup Page
st.set_page_config(page_title="Teemill Trend Scout", layout="wide")

# 2. Initialize Google Trends Connection
pytrends = TrendReq(hl='en-GB', tz=360)

st.title("🚀 Teemill Trend Scout")

# Create the two separate tabs
tab1, tab2 = st.tabs(["📊 Brand Watchlist", "🔍 Discovery Mode"])

# --- TAB 1: BRAND WATCHLIST (For Rapanui, Shirtbox, etc.) ---
with tab1:
    st.subheader("Velocity Rankings for Your Known Niches")
    
    # Sidebar inputs for the Watchlist
    st.sidebar.header("Watchlist Settings")
    user_keywords = st.sidebar.text_area(
        "Enter Keywords (one per line)", 
        "Capybara\nAxolotl\n90s Surf\nCottagecore\nRetro Hiking"
    )
    target_keywords = [kw.strip() for kw in user_keywords.split('\n') if kw.strip()]

    if st.sidebar.button('Clear Cache & Refresh Watchlist'):
        st.cache_data.clear()

    @st.cache_data(ttl=3600)
    def get_watchlist_data(keywords):
        all_data = pd.DataFrame()
        missing_data = []
        for kw in keywords:
            try:
                pytrends.build_payload([kw], timeframe='now 7-d', geo='GB')
                df = pytrends.interest_over_time()
                if not df.empty:
                    all_data[kw] = df[kw]
                else:
                    missing_data.append(kw)
                time.sleep(1.1) 
            except:
                missing_data.append(kw)
        return all_data, missing_data

    if target_keywords:
        with st.spinner('Calculating Velocity...'):
            data, missing = get_watchlist_data(target_keywords)

        if not data.empty:
            results = []
            for kw in data.columns:
                start_val = data[kw].iloc[0]
                end_val = data[kw].iloc[-1]
                # Velocity Formula: (Growth over 7 days)
                velocity = (end_val - start_val) / (start_val + 1)
                results.append({"Niche": kw, "Interest Score": end_val, "Velocity": round(velocity, 2)})

            rankings = pd.DataFrame(results).sort_values(by="Velocity", ascending=False)
            
            col1, col2 = st.columns([1, 2])
            with col1:
                st.dataframe(
                    rankings.style.background_gradient(subset=['Velocity'], cmap='Greens'), 
                    use_container_width=True,
                    hide_index=True
                )
                if missing:
                    st.warning(f"No recent data found for: {', '.join(missing)}")
            with col2:
                st.line_chart(data)
        else:
            st.info("Add keywords in the sidebar to start tracking velocity.")

# --- TAB 2: DISCOVERY MODE (Spotting the "Unknowns") ---
with tab2:
    st.subheader("Live Discovery: What's Spiking in the UK?")
    st.write("These are breakout searches from the last 24 hours. Copy interesting ones back to your Watchlist!")

    if st.button('Scan Live Google Trends Feed'):
        try:
            # RSS Feed provides a more stable way to get trending data
            url = "https://trends.google.com/trends/trendingsearches/daily/rss?geo=GB"
            feed = feedparser.parse(url)
            
            discovery_list = []
            for entry in feed.entries:
                discovery_list.append({
                    "Daily Trend": entry.title,
                    "Approx. Search Volume": entry.get('ht_approx_traffic', 'N/A'),
                    "Context": entry.description
                })
            
            discovery_df = pd.DataFrame(discovery_list)
            
            if not discovery_df.empty:
                st.success(f"Found {len(discovery_df)} breakout topics!")
                st.dataframe(discovery_df, use_container_width=True, hide_index=True)
            else:
                st.warning("No trends found in the feed right now. Try again in a few minutes.")
        except Exception as e:
            st.error(f"Discovery Feed Error: {e}")
