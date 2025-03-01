import yfinance as yf
import pandas as pd
from datetime import datetime, timedelta

class MarketDataProcessor:
    def __init__(self):
        self.indices = {
            'NIFTY 50': '^NSEI',
            'NIFTY BANK': '^NSEBANK',
            'NIFTY MIDCAP 100': '^CNXMC',
            'NIFTY NEXT 50': '^NFTY',
            'NIFTY 100': '^CNX100',
            'NIFTY 200': '^CNX200',
            'NIFTY 500': '^CRSLDX',
            'NIFTY SMALLCAP 100': '^CNXSC',
            'NIFTY MIDCAP 50': '^NIFMDCP50',
            'NIFTY SMALLCAP 50': '^NIFSMCP50',
            'BSE SENSEX': '^BSESN',
            'INDIA VIX': '^INDIAVIX'
        }

    def load_data(self):
        try:
            # Try loading from yfinance first
            data = []
            for name, symbol in self.indices.items():
                try:
                    ticker = yf.Ticker(symbol)
                    info = ticker.info
                    hist = ticker.history(period='1y')

                    current_price = info.get('regularMarketPrice', 0)
                    prev_close = info.get('previousClose', 0)

                    if current_price and prev_close:
                        data.append({
                            'INDEX': name,
                            'CURRENT': current_price,
                            '%CHNG': ((current_price - prev_close) / prev_close * 100),
                            'PREV. CLOSE': prev_close,
                            'PREV. DAY': hist.iloc[-2]['Close'] if len(hist) > 1 else prev_close,
                            '1W AGO': hist.iloc[-6]['Close'] if len(hist) > 5 else prev_close,
                            '1M AGO': hist.iloc[-22]['Close'] if len(hist) > 21 else prev_close
                        })
                except Exception as e:
                    print(f"Error fetching data for {name}: {e}")
                    continue

            if not data:  # If no data was fetched from yfinance
                raise Exception("No data fetched from yfinance")

            return pd.DataFrame(data)

        except Exception as e:
            print(f"Error loading live data: {e}. Using CSV file as fallback.")
            # Fallback to CSV file
            try:
                df = pd.read_csv("attached_assets/MW-All-Indices-01-Mar-2025.csv")
                # Clean column names
                df.columns = [col.strip().replace('"', '').replace('\n', ' ').strip() for col in df.columns]
                # Only keep the indices we're interested in
                df = df[df['INDEX'].isin(self.indices.keys())]
                # Convert numeric columns
                for col in ['CURRENT', '%CHNG', 'PREV. CLOSE']:
                    df[col] = pd.to_numeric(df[col].str.replace(',', ''), errors='coerce')
                return df[['INDEX', 'CURRENT', '%CHNG', 'PREV. CLOSE', 'PREV. DAY', '1W AGO', '1M AGO']]
            except Exception as csv_error:
                print(f"Error loading CSV file: {csv_error}")
                # Return empty DataFrame with required columns
                return pd.DataFrame(columns=['INDEX', 'CURRENT', '%CHNG', 'PREV. CLOSE', 'PREV. DAY', '1W AGO', '1M AGO'])

    def get_summary_stats(self, df):
        # Add error handling for empty DataFrame
        if df.empty:
            return {
                'total_indices': 0,
                'positive_change': 0,
                'negative_change': 0,
                'top_gainer': 'N/A',
                'top_gainer_change': 0,
                'top_loser': 'N/A',
                'top_loser_change': 0
            }

        return {
            'total_indices': len(df),
            'positive_change': len(df[df['%CHNG'] > 0]),
            'negative_change': len(df[df['%CHNG'] < 0]),
            'top_gainer': df.nlargest(1, '%CHNG')['INDEX'].iloc[0],
            'top_gainer_change': df.nlargest(1, '%CHNG')['%CHNG'].iloc[0],
            'top_loser': df.nsmallest(1, '%CHNG')['INDEX'].iloc[0],
            'top_loser_change': df.nsmallest(1, '%CHNG')['%CHNG'].iloc[0]
        }