import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime
import time
from data_processor import MarketDataProcessor
from utils import format_large_number, create_price_chart, get_color

# Page config
st.set_page_config(
    page_title="Market Indices Real-Time Tracker",
    page_icon="📈",
    layout="wide"
)

# Initialize data processor
data_processor = MarketDataProcessor()

def main():
    # Header
    st.title("📈 Market Indices Real-Time Tracker")

    # Auto-refresh
    refresh_interval = st.sidebar.slider("Auto-refresh interval (seconds)", 5, 60, 10)

    # Load data
    df = data_processor.load_data()
    stats = data_processor.get_summary_stats(df)

    # Market Summary in a single row
    st.write("Market Overview")
    cols = st.columns([1, 1, 1, 1])
    with cols[0]:
        st.metric("Advancing", stats['positive_change'], "🟢")
    with cols[1]:
        st.metric("Declining", stats['negative_change'], "🔴")
    with cols[2]:
        st.metric(
            "Top Gainer", 
            f"{stats['top_gainer_change']:.2f}%",
            stats['top_gainer']
        )
    with cols[3]:
        st.metric(
            "Top Loser", 
            f"{stats['top_loser_change']:.2f}%",
            stats['top_loser']
        )

    # Major indices in a grid
    st.write("Major Indices")

    # Create a grid of cards for indices
    col_count = 2  # Number of columns in the grid
    for i in range(0, len(df), col_count):
        cols = st.columns(col_count)
        for j in range(col_count):
            if i + j < len(df):
                with cols[j]:
                    row = df.iloc[i + j]
                    fig = create_price_chart(
                        row['INDEX'],
                        row['CURRENT'],
                        row['PREV. CLOSE']
                    )
                    st.plotly_chart(fig, use_container_width=True)

    # Historical data table
    st.write("Historical Data")
    display_cols = ['INDEX', 'CURRENT', '%CHNG', 'PREV. CLOSE', 
                   'PREV. DAY', '1W AGO', '1M AGO']
    display_df = df[display_cols].copy()

    # Format the numbers
    for col in ['CURRENT', 'PREV. CLOSE', 'PREV. DAY', '1W AGO', '1M AGO']:
        display_df[col] = display_df[col].apply(format_large_number)

    # Style the dataframe
    styled_df = display_df.style.map(get_color, subset=['%CHNG'])
    st.dataframe(styled_df, height=400)

    # Add last updated timestamp
    st.caption(f"Last Updated: {datetime.now().strftime('%H:%M:%S')}")

    # Auto-refresh
    time.sleep(refresh_interval)
    st.rerun()

if __name__ == "__main__":
    main()