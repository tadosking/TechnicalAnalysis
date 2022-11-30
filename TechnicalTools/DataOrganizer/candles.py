import numpy as np
from . candle import Candle

class Candles() :
    """Represents historical candle data and then provides many utilities.
    'Candles' object is list like object which supports slicing.
    Use like : candles[1], candles[1:3:2]
    You can also use like : candles[[0,2,5]], to extract arbitral candle data.
    """
    
    def __init__(self, list_of_candles) :
        """
        Init.
        
        Args :
            list_of_candles : list of 'Candle' objects.
        """
        
        self._candles = list_of_candles

        
    def __iter__(self) :
        
        for c in self._candles :
            yield c
            
        
    def __len__(self) :
        return len(self._candles)
    
        
    def __getitem__(self, idx) :
        
        if hasattr(idx, '__iter__') :
            return self.__class__([ self._candles[int(i)] for i in idx])
        elif isinstance(idx, slice) :
            return self.__class__(self._candles[idx])
        else :
            return self._candles[idx]
        
        
    def __repr__(self) :
        s = '{}([{}])'.format(
            self.__class__.__name__,
            ','.join([ repr(c) for c in self ]))
        return s
    
    
    def __str__(self) :
        s = '{}([\n{}\n])'.format(
            self.__class__.__name__,
            '\n,'.join([ '  OHLCV = ({}, {}, {}, {}, {})'.format(c.open, c.high, c.low, c.close, c.volume) for c in self ]))
        return s
        
    
    def extract_candles_by_index(self, index) :
        if hasattr(index, '__iter__') :
            return self.__class__([ c for c in self if c.index in index ])
        else :
            for c in self :
                if c.index == index :
                    return c
    

    @property
    def indices(self):
        return np.array([c.index for c in self])
        

    @property
    def dates(self):
        return np.array([c.date for c in self])
    

    @property
    def volumes(self):
        return np.array([c.volume for c in self])
    

    @property
    def opens(self):
        return np.array([c.open for c in self])
    

    @property
    def highs(self):
        return np.array([c.high for c in self])
    

    @property
    def lows(self):
        return np.array([c.low for c in self])
    

    @property
    def closes(self):
        return np.array([c.close for c in self])
    

    @property
    def candle_tops(self):
        return np.array([c.candle_top for c in self])
    

    @property
    def candle_bottoms(self):
        return np.array([c.candle_bottom for c in self])
    

    @property
    def black_or_whites(self):
        return np.array([c.black_or_white for c in self])


    @classmethod
    def create_from_pandas(cls, pdf) :
        """
        Creates 'Candles' objects with Pandas dataframe. 
        Indexing starts from 0.
        
        Args :
            pdf : pandas dataframe. 
                dataframe must have at least these columns : 'Open', 'High', 'Low', 'Close'.
                dataframe can have these columns : 'Date', 'Volume'.
        """
        
        list_of_candles = []
        for i, r in pdf.reset_index().iterrows() :
            
            c = Candle(open=r['Open'], 
                   high=r['High'], 
                   low =r['Low'],
                   close=r['Close'], 
                   date  =r.get('Date',None),
                   volume=r.get('Volume',None),
                   index = i )
            list_of_candles.append(c)
            
        return cls(list_of_candles)
