from abc import ABC, abstractmethod
from pathlib import Path
import datetime
import os
import pandas as pd


class DataHandler(ABC):

    @abstractmethod
    def get_latest_bars(self, ticker, N=1):
        return NotImplementedError("Function Not Implemented")

    @abstractmethod
    def update_bars(self):
        return NotImplementedError("Function Not Implemented")


class HistoricCSVHandler(DataHandler):

    def __init__(self, events, csv_dir, ticker_list):
        self.events = events
        self.csv_dir = csv_dir
        self.ticker_list = ticker_list
        self.ticker_data = {}
        self.latest_ticker_data = {}
        self.continue_backtest = True
        self._open_convert_csv()

    def get_latest_bars(self, ticker, N=1):
        try:
            bars_list = self.latest_symbol_data[symbol]
        except KeyError:
            print("That symbol is not available in the historical data set.")
        else:
            return bars_list[-N:]

    def update_bars(self):
        for s in self.symbol_list:
            try:
                bar = self._get_new_bar(s).next()
            except StopIteration:
                self.continue_backtest = False
            else:
                if bar is not None:
                    self.latest_symbol_data[s].append(bar)
        self.events.put(MarketEvent())

    def _open_convert_csv(self):
        comb_index = None

        for ticker in self.ticker_list:
            file_path = (Path(self.csv_dir) / Path(ticker)).with_suffix(".csv")
            self.ticker_data[ticker] = pd.read_csv(
                file_path,
                header=None,
                skiprows=3,
                index_col=0,
                parse_dates=True,
                names=[
                    "datetime",
                    "close",
                    "high",
                    "low",
                    "open",
                    "volume",
                ],
            )
            self.ticker_data[ticker].sort_index(inplace=True)

            if comb_index is None:
                comb_index = self.ticker_data[ticker].index
            else:
                comb_index.union(self.ticker_data[ticker].index)

            self.latest_ticker_data[ticker] = []

        for ticker in self.ticker_list:
            self.ticker_data[ticker] = self.ticker_data[ticker].reindex(
                index=comb_index, method="pad"
            )
            self.ticker_data[ticker]["returns"] = (
                self.ticker_data[ticker]["close"].pct_change().dropna()
            )
            self.ticker_data[ticker] = self.ticker_data[ticker].iterrows()


    def _get_new_bar(self, symbol):
        for b in self.symbol_data[symbol]:
            yield tuple(
                [
                    symbol,
                    datetime.datetime.strptime(b[0], "%Y-%m-%d %H:%M:%S"),
                    b[1][0],
                    b[1][1],
                    b[1][2],
                    b[1][3],
                    b[1][4],
                ]
            )
