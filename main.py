import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime
import time
from data_processor import MarketDataProcessor
from utils import format_large_number, create_price_chart, get_color

# Page config
st.set_page_config(
    page_title="Market Indices Tracker",
    page_icon="📈",
    layout="wide"
)

# Initialize data processor
data_processor = MarketDataProcessor("attached_assets/MW-All-Indices-01-Mar-2025.csv")

def main():
    # Header
    st.title("📈 Market Indices Real-Time Tracker")
    
    # Auto-refresh
    refresh_interval = st.sidebar.slider("Auto-refresh interval (seconds)", 30, 300, 60)
    
    # Load data
    df = data_processor.load_data()
    stats = data_processor.get_summary_stats(df)
    
    # Market Summary
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Total Indices", stats['total_indices'])
    with col2:
        st.metric("Advancing", stats['positive_change'], "🟢")
    with col3:
        st.metric("Declining", stats['negative_change'], "🔴")
    with col4:
        st.metric("Last Updated", datetime.now().strftime("%H:%M:%S"))
    
    # Top Gainers/Losers
    st.subheader("Top Performers")
    col1, col2 = st.columns(2)
    
    with col1:
        st.success(f"Top Gainer: {stats['top_gainer']} ({stats['top_gainer_change']:.2f}%)")
    with col2:
        st.error(f"Top Loser: {stats['top_loser']} ({stats['top_loser_change']:.2f}%)")
    
    # Main indices table
    st.subheader("Major Market Indices")
    
    # Filter major indices
    major_indices = ['NIFTY 50', 'NIFTY BANK', 'NIFTY IT', 'NIFTY AUTO', 'NIFTY PHARMA']
    major_df = df[df['INDEX'].isin(major_indices)]
    
    # Create charts for major indices
    for index, row in major_df.iterrows():
        col1, col2 = st.columns([2, 1])
        with col1:
            fig = create_price_chart(
                row['INDEX'],
                row['CURRENT'],
                row['HIGH'],
                row['LOW'],
                row['PREV. CLOSE']
            )
            st.plotly_chart(fig, use_container_width=True)
        with col2:
            st.metric(
                "Day's Change",
                f"{row['CURRENT']:,.2f}",
                f"{row['%CHNG']:+.2f}%"
            )
    
    # All indices table
    st.subheader("All Market Indices")
    
    # Format DataFrame for display
    display_df = df[['INDEX', 'CURRENT', '%CHNG', 'OPEN', 'HIGH', 'LOW', 'PREV. CLOSE']]
    
    # Style the dataframe
    styled_df = display_df.style.applymap(get_color, subset=['%CHNG'])
    st.dataframe(styled_df, height=400)
    
    # Auto-refresh
    time.sleep(refresh_interval)
    st.experimental_rerun()

if __name__ == "__main__":
    main()
