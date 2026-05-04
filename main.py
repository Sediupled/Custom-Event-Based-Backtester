from pathlib import Path
import yfinance as yf
import collections
from datahandler import HistoricCSVHandler
from portfolio import NaivePortfolio
from strategy import BuyAndHoldStrategy
from execution import SimulatedExecutionHandler


# pre 2018
top_cryptos = [
    "BTC-USD",
    "ETH-USD",
    "USDT-USD",
    "XRP-USD",
    "BNB-USD",
    "TRX-USD",
    "DOGE-USD",
    "ADA-USD",
    "BCH-USD",
    "XMR-USD",
    "ZEC-USD",
    "LINK-USD",
    "XLM-USD",
    "LTC-USD",
]
events = collections.deque()
cur_csv_dir = Path('data')
symbol_list = [child.stem for child in cur_csv_dir.iterdir()]

for c in top_cryptos:
    if c not in symbol_list:
        cur_df = yf.download(c, start="2024-01-01", end="2026-01-01")
        cur_df.to_csv(cur_csv_dir / f"{c}.csv")

# recalculate symbol_list
symbol_list = [child.stem for child in cur_csv_dir.iterdir()]

bars = HistoricCSVHandler(events, cur_csv_dir, symbol_list)
strategy = BuyAndHoldStrategy(bars,events)
port = NaivePortfolio(bars, events, "2024-01-01")
broker = SimulatedExecutionHandler(events)

while True:
    if bars.continue_backtest == True:
        bars.update_bars()
    else:
        break

    while True:
        try:
            event = events.get(False)
        except Queue.Empty:
            break
        else:
            if event is not None:
                if event.type == "MARKET":
                    strategy.calculate_signals(event)
                    port.update_timeindex(event)

                elif event.type == "SIGNAL":
                    port.update_signal(event)

                elif event.type == "ORDER":
                    broker.execute_order(event)

                elif event.type == "FILL":
                    port.update_fill(event)

    time.sleep(10 * 60)
