from typing import Optional

class Candle():
    """Represents stock price candle.
    """
    
    def __init__(self,open:float,high:float,low:float,close:float,
                 date:Optional=None,volume:Optional[float]=None,
                 index:Optional=None):
        """
        Init.
        
        Args:
            open: open price
            high: high price
            low: low price
            close: close price
            date: date (optional)
            volume: volume (optional)
            index: index (optional)
        """

        self._open = open
        self._high = high
        self._low  = low
        self._close = close
        
        self._date   = date
        self._volume = volume
        self._index  = index
        
        if open < close:
            self._black_or_white = 'white'
            self._candle_top    = close
            self._candle_bottom = open
        else:
            self._black_or_white = 'black'
            self._candle_top    = open
            self._candle_bottom = close
            
            
    def __repr__(self):
        
        s = 'Candle(open={}, high={}, low={}, close={}, date={}, volume={}, index={})'.format(
            self.open, self.high, self.low, self.close, self.date, self.volume, self.index )
        return s
    
    
    def __str__(self):
        s = """Candle( O: {},
        H: {},
        L: {},
        C: {},
        Vol: {}, 
        Date: {}, 
        Index: {} )""".format(
            self.open, self.high, self.low, self.close, self.volume, self.date, self.index )
        
        return s
            
    
    @property
    def open(self):
        return self._open

    
    @property
    def high(self):
        return self._high

    
    @property
    def low(self):
        return self._low

    
    @property
    def close(self):
        return self._close

    
    @property
    def volume(self):
        return self._volume

    
    @property
    def index(self):
        return self._index

    
    @property
    def date(self):
        return self._date
    

    @property
    def candle_top(self):
        return self._candle_top
    

    @property
    def candle_bottom(self):
        return self._candle_bottom
    
    
    @property
    def black_or_white(self):
        return self._black_or_white
    

    @property
    def is_black(self):
        
        if self.black_or_white == 'black':
            return True
        else:
            return False
        

    @property
    def is_white(self):
        if self.black_or_white == 'white':
            return True
        else:
            return False
