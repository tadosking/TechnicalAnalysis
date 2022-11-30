from typing import Optional, Any

class DataPoint() :
    """'DataPoint' object stores datapoint's coodinate (x,y).
    Optionally has : 
        - index : arbitral value.
        - symbol : arbitral string.
    """

    
    def __init__(self,x:float,y:float,index:Optional[Any]=None,symbol:Optional[str]=None) :
        """Init.
        
        Args : 
            x : x-coodinate of datapoint.
            y : y-coodinate of datapoint.
            index : arbitral value. (optional)
            symbol : arbitral string, i.e. use 'H' for high value's datapoint. (optonal)
        """
        
        self._x = x
        self._y = y
        
        self._index = index
        self._symbol = symbol
    

    def __repr__(self) :
        if self.index is not None and self.symbol is not None :
            s = '{}({},{},index={},symbol=\'{}\')'.format(
                self.__class__.__name__, self.x, self.y, self.index,self.symbol)
        elif self.index is not None :
            s = '{}({},{},index={})'.format(
                self.__class__.__name__, self.x, self.y, self.index)
        elif self.symbol is not None :
            s = '{}({},{},symbol=\'{}\')'.format(
                self.__class__.__name__, self.x, self.y, self.symbol)
        else :
            s = '{}({},{})'.format(self.__class__.__name__, self.x, self.y)
            
        return s
        

    def __str__(self) :
        if self.index is not None and self.symbol is not None :
            s = '( x: {}, y: {}, index: {}, symbol: \'{}\')'.format(
                self.x,self.y,self.index,self.symbol)
        elif self.index is not None :
            s = '( x: {}, y: {}, index: {})'.format(self.x,self.y,self.index)
        elif self.symbol is not None :
            s = '( x: {}, y: {}, symbol: \'{}\')'.format(self.x,self.y,self.symbol)
        else :
            s = '( x: {}, y: {} )'.format(self.x,self.y)
        return s
    

    @property
    def x(self) :
        return self._x
    

    @property
    def y(self) :
        return self._y
    

    @property
    def index(self) :
        return self._index
    

    @property
    def symbol(self) :
        return self._symbol
    

    @property
    def coord(self) :
        return (self.x, self.y)
    

    def copy(self) :
        """Returns copy of datapoint.
        """
        return self.__class__(self.x,self.y,index=self.index,symbol=self.symbol)
