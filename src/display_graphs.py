import matplotlib.pyplot as plt
import numpy as np


class RSIGraph:
    def __init__(self, LOWER_RSI, UPPER_RSI):
        self.no_graph = True
        self.LOWER_RSI = LOWER_RSI
        self.UPPER_RSI = UPPER_RSI
        
    def create(self, start_x, start_y):
        plt.ion()
        self.fig = plt.figure()
        self.rsi_graph = self.fig.add_subplot(111)
        self.rsi_graph.set(ylim=(0,100))
        self.rsi_graph.axhline(y=self.LOWER_RSI, color='#90ee90')
        self.rsi_graph.axhline(y=self.UPPER_RSI, color='#ff6961')
        self.rsi_line, = self.rsi_graph.plot(start_x, start_y, 'r-')
        self.fig.canvas.draw()
        self.fig.canvas.flush_events()

    def update(self, new_x, new_y):
        if self.no_graph:
            self.create(new_x, new_y)
            self.no_graph = False
            return
        self.rsi_graph.set(xlim=(new_x[0]-1,new_x[-1]+1))
        self.rsi_line.set_xdata(new_x)
        self.rsi_line.set_ydata(new_y)  
        self.fig.canvas.draw()
        self.fig.canvas.flush_events()
    
    def update_RSI_bounds(self, new_upper, new_lower):
        self.UPPER_RSI = new_upper
        self.LOWER_RSI = new_lower

class BBandGraph:
    def __init__(self):
        self.no_graph = True

    def create(self, UPPER, LOWER, TICK_TIMES, PRICE):
        self.margin = UPPER[-1]-LOWER[-1]
        plt.ion()
        self.fig = plt.figure()
        self.band_graph = self.fig.add_subplot(111)
        self.upper_line, = self.band_graph.plot(TICK_TIMES, UPPER, 'b-')
        self.lower_line, = self.band_graph.plot(TICK_TIMES, LOWER, 'b-')
        self.price_line, = self.band_graph.plot(TICK_TIMES, PRICE, 'r-')
        self.fig.canvas.draw()
        self.fig.canvas.flush_events()


    def update(self, UPPER, LOWER, TICK_TIMES, PRICE):
        if self.no_graph:
            self.create(UPPER, LOWER, TICK_TIMES, PRICE)
            self.no_graph = False
            return
        self.margin = (self.margin + (UPPER[-1]-LOWER[-1]))/2
        self.band_graph.set(xlim=(TICK_TIMES[0]-1,TICK_TIMES[-1]+1), ylim=(LOWER[-1]-self.margin, UPPER[-1]+self.margin))
        try:
            self.upper_line.set_xdata(TICK_TIMES)
            self.upper_line.set_ydata(UPPER)
            self.lower_line.set_xdata(TICK_TIMES)
            self.lower_line.set_ydata(LOWER)
            self.price_line.set_xdata(TICK_TIMES)
            self.price_line.set_ydata(PRICE)
        except:
            print("Error")

        self.fig.canvas.draw()
        self.fig.canvas.flush_events()