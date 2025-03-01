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

def create_price_chart(index_name, current_price, high, low, prev_close):
    fig = go.Figure()
    
    # Add price line
    fig.add_trace(go.Indicator(
        mode = "number+delta",
        value = float(current_price),
        delta = {"reference": float(prev_close), "relative": True},
        title = {"text": index_name},
        domain = {'x': [0, 1], 'y': [0, 1]}
    ))
    
    # Add range slider for high/low
    fig.add_trace(go.Indicator(
        mode = "number+gauge",
        value = float(current_price),
        gauge = {
            'axis': {'range': [float(low), float(high)]},
            'bar': {'color': "darkblue"},
            'steps': [
                {'range': [float(low), float(high)], 'color': "lightgray"}
            ],
        },
        domain = {'x': [0.1, 0.9], 'y': [0, 0.3]}
    ))
    
    fig.update_layout(
        height=300,
        margin=dict(l=10, r=10, t=60, b=10)
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
