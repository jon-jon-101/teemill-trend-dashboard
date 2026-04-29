import streamlit as st
from pytrends.request import TrendReq
import pandas as pd
import time

st.set_page_config(page_title="Teemill Trend Scout", layout="wide")
pytrends = TrendReq(hl='en-GB', tz=360)

st.title("🚀 Teemill Trend Scout: Discovery Mode")

# --- TABS FOR DIFFERENT MODES ---
tab1, tab2 = st.tabs(["Manual Watchlist", "Auto-Discovery (UK Daily)"])

# --- TAB 1: YOUR EXISTING WATCHLIST ---
with tab1:
    st.sidebar.header("Watchlist Settings")
    user_keywords = st.sidebar.text_area("Watchlist (one per line)", "Capybara\nAxolotl\n90s Surf")
    target_keywords = [kw.strip() for kw in user_keywords.split('\n') if kw.strip()]
    
    if st.button('Refresh Watchlist'):
        st.cache_data.clear()

    # (Insert the same logic from before here to show the watchlist chart)

# --- TAB 2: THE DISCOVERY ENGINE ---
with tab2:
    st.header("What's Spiking in the UK Right Now?")
    st.write("These are the top 20 trending searches in the UK today. Great for 'Quick-Strike' Shirtbox designs.")
    
    if st.button('Scan for New Trends'):
        try:
            # This is the "Discovery" magic line:
            trending_df = pytrends.trending_searches(pn='united_kingdom')
            trending_df.columns = ["Trending Topic"]
            
            # We then get "Related" queries for a broad category like 'T-shirt'
            pytrends.build_payload(['t shirt'], timeframe='now 7-d', geo='GB')
            related = pytrends.related_queries()
            rising_queries =相关['t shirt']['rising']

            col_a, col_b = st.columns(2)
            with col_a:
                st.subheader("Daily Trending Searches")
                st.dataframe(trending_df, use_container_width=True)
            
            with col_b:
                st.subheader("Rising 'T-Shirt' Niche Searches")
                if not rising_queries.empty:
                    st.dataframe(rising_queries, use_container_width=True)
                else:
                    st.write("No specific niche spikes detected in the last hour.")
                    
        except Exception as e:
            st.error(f"Discovery error: {e}")
