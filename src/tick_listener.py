class TickListener:

    def close_event(tickPrice : float):
        raise NotImplementedError

    def tick_event(closePrice : float):
        raise NotImplementedError