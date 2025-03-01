import yfinance as yf
import pandas as pd
from datetime import datetime, timedelta

class MarketDataProcessor:
    def __init__(self):
        self.indices = {
            'Nifty 50': '^NSEI',
            'Nifty Bank': '^NSEBANK',
            'FinNifty': 'FINNIFTY.NS',
            'BSE Sensex': '^BSESN',
            'Nifty Midcap Select': 'NIFTY_MIDCAP_SELECT.NS',
            'BSE Bankex': '^BANKEX',
            'India VIX': '^INDIAVIX',
            'Nifty Total Market': 'NIFTY_TOTAL_MARKET.NS',
            'Nifty Next 50': 'NIFTY_NEXT_50.NS',
            'Nifty 100': 'NIFTY_100.NS'
        }

    def load_data(self):
        data = []
        for name, symbol in self.indices.items():
            try:
                ticker = yf.Ticker(symbol)
                info = ticker.info
                hist = ticker.history(period='1y')

                current_price = info.get('regularMarketPrice', 0)
                prev_close = info.get('previousClose', 0)

                data.append({
                    'INDEX': name,
                    'CURRENT': current_price,
                    '%CHNG': ((current_price - prev_close) / prev_close * 100) if prev_close else 0,
                    'OPEN': info.get('regularMarketOpen', 0),
                    'HIGH': info.get('dayHigh', 0),
                    'LOW': info.get('dayLow', 0),
                    'PREV. CLOSE': prev_close,
                    'PREV. DAY': hist.iloc[-2]['Close'] if len(hist) > 1 else 0,
                    '1W AGO': hist.iloc[-6]['Close'] if len(hist) > 5 else 0,
                    '1M AGO': hist.iloc[-22]['Close'] if len(hist) > 21 else 0,
                    '1Y AGO': hist.iloc[-252]['Close'] if len(hist) > 251 else 0,
                    '52W H': hist['High'].max(),
                    '52W L': hist['Low'].min()
                })
            except Exception as e:
                print(f"Error fetching data for {name}: {e}")

        return pd.DataFrame(data)

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