# --- Do not remove these libs ---
import numpy as np  # noqa
import pandas as pd  # noqa
from pandas import DataFrame

from freqtrade.strategy import (BooleanParameter, CategoricalParameter, DecimalParameter,IStrategy, IntParameter)

# --- Add your lib to import here ---
import talib.abstract as ta
import freqtrade.vendor.qtpylib.indicators as qtpylib

# --- Generic strategy settings ---

class SmaRsiStrategy(IStrategy):
    INTERFACE_VERSION = 2
    
    # Determine timeframe and # of candles before strategysignals becomes valid
    timeframe = '1d'
    startup_candle_count: int = 25

    # Determine roi take profit and stop loss points
    minimal_roi = {"0": 0.99}
    stoploss = -0.10
    trailing_stop = False
    use_sell_signal = True
    sell_profit_only = False
    sell_profit_offset = 0.0
    ignore_roi_if_buy_signal = False

# --- Plotting ---

# --- Used indicators of strategy code ----

    def populate_indicators(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        # Populate this section with the indicators you want to use in your strategy
        dataframe['rsi'] = ta.RSI(dataframe)
        dataframe['sma21'] = ta.SMA(dataframe, timeperiod=21)
        dataframe['sma50'] = ta.SMA(dataframe, timeperiod=50)

#        print(metadata)
#        print(dataframe)
        return dataframe

# --- Buy settings ---

    def populate_buy_trend(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        # Enter the conditions for buying
        dataframe.loc[
            (
                (dataframe['rsi'] > 50) &
                (qtpylib.crossed_above(dataframe['close'], dataframe['sma21']))
            ),
            'buy'] = 1

        return dataframe

# --- Sell settings ---

    def populate_sell_trend(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        # Enter the conditions for selling (besides ROI TP if available)
        dataframe.loc[
            (
                (dataframe['rsi'] < 50) &
                (qtpylib.crossed_below(dataframe['close'], dataframe['sma21']))
            ),
            'sell'] = 1
        return dataframe
