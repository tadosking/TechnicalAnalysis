from typing import Callable
from . zigzag import ZigZag


class ZigZagDetector() :

    
    def __init__(self,
                 upper_symbol:str='H',lower_symbol:str='L', 
                 upper_select_func:Callable=None, lower_select_func:Callable=None) :
        """Init detector and set parameters.
        
        Args :
            upper_symbol : str to identify upper datapoints of zigzag.
            lower_symbol : str to identify lower datapoints of zigzag.
            upper_select_func : function('Chunk') -> 'DataPoint'.
                                select one datapoint from each chunks with upper symbol. 
                                (optional, if not set, select datapoint with highest value.)
            lower_select_func : function('Chunk') -> 'DataPoint'.
                                select one datapoint from each chunks with lower symbol.
                                (optional, if not set, select datapoint with lowest value.)
        """
        self._upper_symbol = upper_symbol
        self._lower_symbol = lower_symbol
        
        self._upper_select_func = self._default_upper_select_func
        if upper_select_func is not None :
            self._upper_select_func = upper_select_func
        
        self._lower_select_func = self._default_lower_select_func
        if lower_select_func is not None :
            self._lower_select_func = lower_select_func
            
    
    @property
    def params(self) :
        return { 
            'upper_symbol' : self._upper_symbol,
            'lower_symbol' : self._lower_symbol,
            'upper_select_func' : self._upper_select_func,
            'lower_select_func' : self._lower_select_func
        }

    
    @staticmethod
    def _default_upper_select_func(chunk) :
        return max(chunk,key=lambda c:c.y)  
        
        
    @staticmethod
    def _default_lower_select_func(chunk) :
        return min(chunk,key=lambda c:c.y)
            
        
    def detect_from_chunks(self,chunks) :
        """Create 'ZigZag' object from 'Chunks' object, selecting one datapoint from each chunks.
        Default selecting functions are which returns max or min data point from a chunk.
        
        Args :
            chunks : 'Chunks' object.
        """
            
        dps = []
        for c in chunks :
            if c.symbol == self._upper_symbol :
                dps.append(self._upper_select_func(c))
            elif c.symbol == self._lower_symbol :
                dps.append(self._lower_select_func(c))
                
        return ZigZag(dps, upper_symbol=self._upper_symbol, lower_symbol=self._lower_symbol)
    
    
