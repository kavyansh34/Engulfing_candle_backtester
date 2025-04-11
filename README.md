# Engulfing_candle_backtester
This project is a Python-based backtesting engine for a custom crypto trading strategy that uses RSI, volume EMA, and engulfing candlestick patterns. It calculates risk-managed entries and simulates trades over historical data loaded in either CSV file or from binance.

## Strategy logic
* Bullish signal (signal == 1)
  * Bullish engulfing pattern over the last two candles.
  * RSI between 30 and 40.
  * Volume higher than 14-period EMA of volume.
* Bearish signal (signal == 2)
  * Bearish engulfing pattern over the last two candles.
  * RSI between 60 and 70.
  * Volume higher than 99-period EMA of volume.

## Capital Managemant
* Initial Capital: $10,000
* Risk per trade: $100 (1% of capital)
* Risk-Reward Ratio: Configurable (default = 1:5)
The backtester adjusts the capital after each trade, depending on win or loss, based on risk-to-reward ratio.

## Note
1) All the dependencies are mentioned in 'Requirements.txt'
2) Sample data set of BTCUSDT past 1 year in 5m timeframe is provided in 'BTCUSDT_5m_365.csv'
3) Sample data format is {timestamp, open, high, low, close, volume}
4) No slippage or fees modeled — pure backtest.
5) Risk-reward ratio is static and can be optimized.

## Future enhancement
* Trailing stoploss and dynamic position sizing
* Add visualization with Matplotlib or Plotly
  


    
