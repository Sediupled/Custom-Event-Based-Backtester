from abc import ABC, abstractmethod
from pathlib import Path
import datetime 
import os
import pandas as pd

class DataHandler(ABC):

	@abstractmethod
	def get_latest_bars(self, ticker, N = 1):
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
		self.open_convert_csv


	def get_latest_bars(self, ticker, N = 1):
		pass
	def update_bars(self):
		pass

	def _open_convert_csv(self):
		comb_index = None

        for ticker in self.ticker_list:
       		file_path = (Path(self.csv_dir) / Path(ticker)).with_suffix('.csv')
            self.ticker_date[ticker] = pd.read_csv(
                file_path,
                header=0, index_col=0, parse_dates=True,
                names=[
                    'datetime', 'open', 'high', 
                    'low', 'close', 'adj_close', 'volume'
                ]
            )
            self.ticker_data[ticker].sort_index(inplace=True)

            if comb_index is None:
                comb_index = self.ticker_data[ticker].index
            else:
                comb_index.union(self.ticker_data[ticker].index)

            self.latest_ticker_data[s] = []

        for ticker in self.ticker_list:
            self.ticker_data[ticker] = self.ticker_data[ticker].reindex(
                index=comb_index, method='pad'
            )
            self.ticker_data[ticker]["returns"] = self.ticker_data[ticker]["adj_close"].pct_change().dropna()
            self.ticker_data[ticker] = self.ticker_data[ticker].iterrows()

        for ticker in self.ticker_list:
            self.ticker_data[ticker] = self.ticker_data[ticker].reindex(index=comb_index, method='pad').iterrows()



# Hcsv = HistoricCSVHandler([], "Home/Libraries/Donker", [])

# Hcsv._open_convert_csv("APPL")
