import pandas as pd
from datetime import datetime

class MarketDataProcessor:
    def __init__(self, csv_path):
        self.csv_path = csv_path
        
    def load_data(self):
        df = pd.read_csv(self.csv_path)
        
        # Clean column names
        df.columns = [col.strip().replace('"', '').replace('\n', ' ').strip() for col in df.columns]
        
        # Clean data values
        for col in df.columns:
            if df[col].dtype == object:
                df[col] = df[col].str.replace('"', '').str.strip()
        
        # Convert numeric columns
        numeric_cols = ['CURRENT', '%CHNG', 'OPEN', 'HIGH', 'LOW', 'PREV. CLOSE']
        for col in numeric_cols:
            df[col] = pd.to_numeric(df[col], errors='coerce')
            
        return df
    
    def get_summary_stats(self, df):
        return {
            'total_indices': len(df),
            'positive_change': len(df[df['%CHNG'] > 0]),
            'negative_change': len(df[df['%CHNG'] < 0]),
            'top_gainer': df.nlargest(1, '%CHNG')['INDEX'].iloc[0],
            'top_gainer_change': df.nlargest(1, '%CHNG')['%CHNG'].iloc[0],
            'top_loser': df.nsmallest(1, '%CHNG')['INDEX'].iloc[0],
            'top_loser_change': df.nsmallest(1, '%CHNG')['%CHNG'].iloc[0]
        }
