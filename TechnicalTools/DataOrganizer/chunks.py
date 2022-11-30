from typing import List

from . chunk import Chunk
from . datapoints import DataPoints


class Chunks() :
    """list of 'Chunk' objects and its utility methods.
    'Chunks' object is list like object which support slicing.
    """
    
    def __init__(self,list_of_chunks:List[Chunk]) :
        
        self._data = list_of_chunks
    
    
    def __iter__(self) :
        for c in self._data :
            yield c
    
    
    def __repr__(self) :
        s = 'Chunks([{}])'.format(','.join([ repr(c) for c in self ]))
        return s
    
    
    def __str__(self) :
        s = 'Chunks(\n[{}])'.format('\n,'.join([ str(c) for c in self ]))
        return s


    def __len__(self) :
        return len(self._data)

    
    def __getitem__(self,idx):
        
        if hasattr(idx,'__iter__') :
            return self.__class__([ self._data[i] for i in idx])
        elif isinstance(idx,slice) :
            return self.__class__( self._data[idx] )
        else :
            return self._data[idx]
    

    def append(self,chunk:Chunk) :
        if not isinstance(chunk,Chunk) :
            raise Exception("variable 'chunk' is not 'Chunk' object but {}.".format(chunk) )
        self._data.append(chunk)


    def to_datapoints(self) :
        tmp = []
        for chunk in self :
            tmp.extend(chunk._data)        
        return DataPoints(tmp)

 
    def get_chunks_by_symbol(self,symbol) :
        return self.__class__([c for c in self if c._symbol==symbol])


    def copy(self) :
        """Returns copy of 'Chunks' objects."""
        return self.__class__([c.copy() for c in self])
