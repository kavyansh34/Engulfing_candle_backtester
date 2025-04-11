import numpy as np
import pandas as pd
import requests
import ta.momentum

capital = 10000
riskpt = 100 # risk per trade (only 1%) 

def load_csv_data(filepath):
    df = pd.read_csv(filepath)
    df["timestamp"] = pd.to_datetime(df["timestamp"])

    df[["open", "high", "low", "close","volume"]] = df[["open", "high", "low", "close","volume"]].astype(float)
    return df

def fetch_binance_data(symbol="BTCUSDT", interval = "1m", limit=1000):
    url = f"https://api.binance.com/api/v3/klines?symbol={symbol}&interval={interval}&limit={limit}"
    response = requests.get(url)
    data = response.json()
    
    df = pd.DataFrame(data, columns=["timestamp", "open", "high", "low", "close", "volume", "close_time", 
                                     "quote_asset_volume", "number_of_trades", "taker_buy_base_asset_volume", 
                                     "taker_buy_quote_asset_volume", "ignore"])
    
    df = df[["timestamp", "open", "high", "low", "close","volume"]]
    df["timestamp"] = pd.to_datetime(df["timestamp"], unit='ms')
    df[["open", "high", "low", "close","volume"]] = df[["open", "high", "low", "close","volume"]].astype(float)
    return df

def calculate_ema(df, period, column="close"):
    return df[column].ewm(span=period, adjust=False).mean()

def backtest_ema_strategy(df_5m, risk_reward=5):
    global capital, riskpt                    
    df_5m['rsi'] = ta.momentum.rsi(df_5m['close'], window =14).astype(float)
    df_5m['volumeMA'] = calculate_ema(df_5m, 14, "volume").shift(1)
    
    df_5m["signal"] = 0 #marked 0 for all 
    for i in range(1, len(df_5m)):
        timestamp = df_5m["timestamp"].iloc[i]

        if df_5m['open'].iloc[i-1] < df_5m['close'].iloc[i-2] and  df_5m['open'].iloc[i-2] < df_5m['close'].iloc[i-1] and df_5m['volume'].iloc[i-1] > df_5m['volumeMA'].iloc[i-1] and 40 > df_5m['rsi'].iloc[i-1]  :
            df_5m.loc[i,'signal'] = 1 #bullsih trade

        if df_5m['close'].iloc[i-1] < df_5m['open'].iloc[i-2] and  df_5m['close'].iloc[i-2] < df_5m['open'].iloc[i-1] and df_5m['volume'].iloc[i-1] > df_5m['volumeMA'].iloc[i-1] and 60 < df_5m['rsi'].iloc[i-1] :
            df_5m.loc[i,'signal'] = 2 #bearish trade

       
    entry_prices = []
    sl_prices = []
    tp_prices = []
    wins = 0
    losses = 0
    
    for i in range(len(df_5m)):
        if df_5m["signal"].iloc[i] == 1 :
            entry_price =df_5m["open"].iloc[i]
            sl_price =max(df_5m["low"].iloc[i-2],df_5m["low"].iloc[i-1])
            tp_price = entry_price + (entry_price - sl_price) * risk_reward
            
            entry_prices.append(entry_price)
            sl_prices.append(sl_price)
            tp_prices.append(tp_price)
            
            for j in range(i+1, len(df_5m)):
                if df_5m["high"].iloc[j] >= tp_price:
                    wins += 1
                    capital += (riskpt*risk_reward  ) 
                    position = False
                    break
                elif df_5m["low"].iloc[j] <= sl_price:
                    losses += 1
                    capital -= (riskpt )
                    position = False
                    break
                

        elif df_5m["signal"].iloc[i] == 2 :
            entry_price = df_5m["open"].iloc[i]
            sl_price =min(df_5m["high"].iloc[i-2], df_5m["high"].iloc[i-1])
            tp_price = entry_price - (sl_price - entry_price ) * risk_reward
            
            entry_prices.append(entry_price)
            sl_prices.append(sl_price)
            tp_prices.append(tp_price)
            
            for j in range(i+1, len(df_5m)):
                if df_5m["low"].iloc[j] <= tp_price:
                    wins += 1
                    capital += (riskpt*risk_reward ) 
                    break
                elif df_5m["high"].iloc[j] >= sl_price:
                    losses += 1
                    capital -= (riskpt )
                    break
                       
    
    win_rate = (wins / (wins + losses)) * 100 if (wins + losses) > 0 else 0
    return {
        "Total Trades": wins + losses,
        "Wins": wins,
        "Losses": losses,
        "Win Rate": win_rate,
        "capital + return " : capital
    }

# Fetch Data
df_5m = load_csv_data("BTCUSDT_5m_365.csv") #use 'fetch_binance_data' to check trades for past few hours.

result = backtest_ema_strategy(df_5m)
print(result)