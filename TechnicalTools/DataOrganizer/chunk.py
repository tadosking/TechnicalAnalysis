from typing import Optional, Union, List

from . datapoint import DataPoint
from . datapoints import DataPoints



class Chunk() :
    """Datapoints chunk. 'Chunk' object is list like object which support slicing.
    """
    
    def __init__(self,list_of_data_point:Union[DataPoints,List[DataPoint]],symbol:Optional[str]=None) :
        
        if isinstance(list_of_data_point, DataPoints) :
            list_of_data_point = [ dp for dp in DataPoints ]
        self._data = list_of_data_point
        self._symbol = symbol

        
    def __iter__(self) :
        for dp in self._data :
            yield dp

            
    def __repr__(self) :
        s = 'Chunk([{}], symbol=\'{}\')'.format(
            ','.join([ repr(dp) for dp in self ]), self.symbol )
        return s


    def __str__(self) :
        s = 'Chunk( symbol:\'{}\',\n[{}])'.format(
            self.symbol,
            '\n,'.join([ str(dp) for dp in self]) )
        return s
    
    
    def __len__(self) :
        return len(self._data)


    @property
    def symbol(self) :
        return self._symbol
    
    
    def __getitem__(self,idx):
        
        if hasattr(idx,'__iter__') :
            return self.__class__([ self._data[i] for i in idx ], self.symbol )
        elif isinstance(idx,slice) :
            return self.__class__( self._data[idx], self.symbol )
        else :
            return self._data[idx]


    def append(self,dp) :
        if not isinstance(dp,DataPoint) :
            raise Exception("variable 'dp' is not 'DataPoint' object but {}".format(dp) )
        self._data.append(dp)


    def to_datapoints(self) :
        return DataPoints(self._data)


    def copy(self) :
        """Returns copy of 'Chunk' objects."""
        return self.__class__(self, self.symbol)
