import streamlit as st
from pytrends.request import TrendReq
import pandas as pd
import time
import feedparser # We'll need to add this to requirements.txt

st.set_page_config(page_title="Teemill Trend Scout", layout="wide")
pytrends = TrendReq(hl='en-GB', tz=360)

st.title("🚀 Teemill Trend Scout: Discovery Mode")

tab1, tab2 = st.tabs(["Manual Watchlist", "Auto-Discovery (Live UK Feed)"])

# --- TAB 1: WATCHLIST (Keep your existing code here) ---
with tab1:
    st.write("Monitor your specific brand niches here.")
    # (Your previous Watchlist logic)

# --- TAB 2: THE NEW DISCOVERY ENGINE ---
with tab2:
    st.header("What's Spiking in the UK Right Now?")
    st.write("This pulls from the live Google Trends RSS feed. Highly reliable.")
    
    if st.button('Scan Live UK Feed'):
        try:
            # We use feedparser to read the public RSS feed instead of the broken API
            url = "https://trends.google.com/trends/trendingsearches/daily/rss?geo=GB"
            feed = feedparser.parse(url)
            
            trends_list = []
            for entry in feed.entries:
                trends_list.append({
                    "Trend": entry.title,
                    "Search Volume": entry.get('ht_approx_traffic', 'N/A'),
                    "News Link": entry.link
                })
            
            discovery_df = pd.DataFrame(trends_list)
            
            if not discovery_df.empty:
                st.success(f"Found {len(discovery_df)} breakout trends!")
                st.dataframe(discovery_df, use_container_width=True)
                
                st.info("💡 TIP: If you see a topic you like, copy it back into the 'Watchlist' tab to see its 7-day velocity.")
            else:
                st.warning("No trends found in the feed right now. Try again in 10 minutes.")

        except Exception as e:
            st.error(f"Discovery error: {e}. The RSS feed might be momentarily down.")
