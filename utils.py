import pandas as pd
import plotly.graph_objects as go
from datetime import datetime

def format_large_number(number):
    if pd.isna(number):
        return "-"
    if isinstance(number, str):
        try:
            number = float(number.replace(",", ""))
        except:
            return number
    if number >= 1000000:
        return f"{number/1000000:.2f}M"
    elif number >= 1000:
        return f"{number/1000:.2f}K"
    return f"{number:.2f}"

def create_price_chart(index_name, current_price, prev_close):
    # Calculate percentage change
    pct_change = ((float(current_price) - float(prev_close)) / float(prev_close)) * 100 if prev_close else 0

    # Create a simple card-like display
    fig = go.Figure()

    # Add price and change indicators
    fig.add_trace(go.Indicator(
        mode="number+delta",
        value=float(current_price),
        delta={"reference": float(prev_close), 
               "relative": True,
               "valueformat": ".2%"},
        title={"text": index_name},
        number={"valueformat": ".2f"},
        domain={'y': [0, 1], 'x': [0, 1]}
    ))

    # Update layout for a cleaner look
    fig.update_layout(
        height=150,  # Reduced height
        margin=dict(l=10, r=10, t=30, b=10),  # Reduced margins
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)'
    )

    return fig

def get_color(value):
    try:
        value = float(value)
        if value > 0:
            return "color: green"
        elif value < 0:
            return "color: red"
        return "color: black"
    except:
        return "color: black"