# Engulfing_candle_backtester
This project is a Python-based backtesting engine for a custom crypto trading strategy that uses RSI, volume EMA, and engulfing candlestick patterns. It calculates risk-managed entries and simulates trades over historical data loaded in either CSV file or from binance.

## Strategy logic
* Bullish signal == 1
* * Bullish engulfing pattern over the last two candles.
  * RSI between 30 and 40.
  * Volume higher than 14-period EMA of volume.
    
* Bearish signal == 2
* * Bearish engulfing pattern over the last two candles.
  * RSI between 60 and 70.
  * Volume higher than 99-period EMA of volume.
