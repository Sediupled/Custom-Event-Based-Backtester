import datetime
import collections

from abc import ABCMeta, abstractmethod

from events import FillEvent, OrderEvent


class ExecutionHandler(metaclass=ABCMeta):

    @abstractmethod
    def execute_order(self, event):
        raise NotImplementedError("execute order not made")


class SimulatedExecutionHandler(ExecutionHandler):
    def __init__(self, events):
        self.events = events

    def execute_order(self, event):
        if event.type == "ORDER":
            fill_event = FillEvent(
                datetime.datetime.utcnow(),
                event.symbol,
                "ARCA",
                event.quantity,
                event.direction,
                None,
            )
            self.events.put(fill_event)
