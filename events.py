class Event:
    """

    Parent Class for all Event Subclasses
    we are going to be using in this project

    """

    pass


# Used to trigger Strategy to generate a new trade signal
class MarketEvent(Event):
    def __init__(self):
        self.type = "MARKET"


# Trading advice generated for the Portfolio
class SignalEvent(Event):
    def __init__(self, ticker, timestamp, direction):
        self.type = "SIGNAL"
        self.ticker = ticker
        self.timestamp = timestamp
        self.direction = direction


# Used to Execute an order
class OrderEvent(Event):
    def __init__(self, ticker, num_shares, order_type, direction):
        self.type = "ORDER"
        self.ticker = ticker
        self.order_type = order_type
        self.quantity = quantity
        self.direction = direction

    def show_order(self):
        print("-" * 20)
        print(
            f"Symbol: {self.ticker}\n"
            "Order Type: {self.order_type}\n"
            "Amount: {self.num_shares}\n"
            "Action: {self.direction}"
        )
        return


class FillEvent(Event):
    def __init__(
        self, timestamp, ticker, exchange, num_shares, price, direction, commission=None
    ):
        self.type = "FILL"
        self.datetime = datetime
        self.ticker = ticker
        self.exchange = exchange
        self.num_shares = num_shares
        self.direction = direction
        self.price = price

        self.commission = commission if commission == None else calculate_commision

    def calculate_commision(self):
        if num_shares >= 500:
            full_cost = max(1.3, 0.008 * num_shares)
        else:
            full_cost = max(1.3, 0.013 * num_shares)
        full_cost = min(full_cost, 0.5 / 100.0 * self.num_shares * self.price)
        return full_cost
