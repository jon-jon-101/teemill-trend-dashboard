import streamlit as st
from pytrends.request import TrendReq
import pandas as pd

# 1. Setup Page
st.set_page_config(page_title="Teemill Trend Scout", layout="wide")
st.title("🚀 Teemill Trend Scout")
st.write("Identifying high-velocity niches for Rapanui & Shirtbox.")

# 2. Connect to Google Trends
pytrends = TrendReq(hl='en-GB', tz=360)

# 3. Define your "Watchlist" (You can edit these names!)
watchlist = ["Capybara", "Axolotl", "90s Surf", "Cottagecore", "Sustainable Fashion", "Retro Hiking"]

@st.cache_data(ttl=86400) # Only refresh data once a day to stay fast
def get_trend_data(keywords):
    pytrends.build_payload(keywords, timeframe='now 7-d', geo='GB')
    df = pytrends.interest_over_time()
    return df

# 4. Calculate Velocity
try:
    data = get_trend_data(watchlist)
    
    st.subheader("Weekly Trend Velocity")
    
    # Logic: Compare the start of the week to the end
    results = []
    for kw in watchlist:
        start_val = data[kw].iloc[0]
        end_val = data[kw].iloc[-1]
        # Using the Velocity Formula: (End - Start) / (Start + 1)
        velocity = (end_val - start_val) / (start_val + 1)
        results.append({"Niche": kw, "Current Interest": end_val, "Velocity": round(velocity, 2)})

    # Sort by highest velocity
    rankings = pd.DataFrame(results).sort_values(by="Velocity", ascending=False)
    
    # 5. Display Dashboard
    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.dataframe(rankings, use_container_width=True)
        
    with col2:
        st.line_chart(data[watchlist])

except Exception as e:
    st.error(f"Waiting for trend data... (Error: {e})")
