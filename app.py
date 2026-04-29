import streamlit as st
from pytrends.request import TrendReq
import pandas as pd
import time

# 1. Setup Page
st.set_page_config(page_title="Teemill Trend Scout", layout="wide")
st.title("🚀 Teemill Trend Scout")
st.write("Spotting high-velocity niches for Rapanui & Shirtbox.")

# 2. Connect to Google Trends
pytrends = TrendReq(hl='en-GB', tz=360)

# 3. Your Watchlist (You can add as many as you like now!)
watchlist = [
    "Capybara", "Axolotl", "90s Surf", "Cottagecore", 
    "Sustainable Fashion", "Retro Hiking", "Checkered Print", "Tufting"
]

@st.cache_data(ttl=86400)
def get_all_trends(keywords):
    all_data = pd.DataFrame()
    
    for kw in keywords:
        try:
            # Fetching 1 by 1 to avoid the 'Rule of 5' and 400 errors
            pytrends.build_payload([kw], timeframe='now 7-d', geo='GB')
            df = pytrends.interest_over_time()
            if not df.empty:
                all_data[kw] = df[kw]
            time.sleep(1) # A tiny pause to be polite to Google's servers
        except:
            continue
    return all_data

# 4. Run the Engine
with st.spinner('Scouting the latest trends...'):
    data = get_all_trends(watchlist)

if not data.empty:
    results = []
    for kw in data.columns:
        start_val = data[kw].iloc[0]
        end_val = data[kw].iloc[-1]
        
        # Velocity calculation
        velocity = (end_val - start_val) / (start_val + 1)
        results.append({"Niche": kw, "Current Interest": end_val, "Velocity": round(velocity, 2)})

    # Sort by highest velocity
    rankings = pd.DataFrame(results).sort_values(by="Velocity", ascending=False)
    
    # 5. Display Dashboard
    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.subheader("Velocity Rankings")
        # Style the dataframe to highlight high velocity
        st.dataframe(rankings.style.background_gradient(subset=['Velocity'], cmap='Greens'))
        
    with col2:
        st.subheader("Trend Lines (Last 7 Days)")
        st.line_chart(data)
else:
    st.error("Google is being a bit shy right now. Try refreshing in a minute!")
