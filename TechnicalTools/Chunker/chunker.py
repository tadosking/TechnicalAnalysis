from typing import Optional, List

from .. DataOrganizer import DataPoints, Chunk, Chunks

class UpperLowerChunker() :
    """
    Utility class to chunk down sampled high/low data points.
    """
    
    def __init__(self,upper_symbol:str,lower_symbol:str) :
        """Init.
        
        Args :
            upper_symbol : symbol for upper chunks.
            lower_symbol : symbol for lower_chunks.
        """
        self._upper_symbol = upper_symbol
        self._lower_symbol = lower_symbol

    
    @property
    def params(self) :
        return { 'upper_symbol' : self._upper_symbol,
                 'lower_symbol' : self._lower_symbol }


    def chunk_down(self,
                   upper_data:DataPoints,
                   lower_data:DataPoints,
                   upper_black_or_whites:Optional[List[str]]=None,
                   lower_black_or_whites:Optional[List[str]]=None) :
        """Chunk down sampled high/low datapoints.
        First, high and low datapoints is concatenated and sorted by x-order.
        Second, contiguous high or low datapoints will be grouped in a chunk.
        
        Args :
            upper_data            : upper 'DataPoints' object for '^'s of zigzag detection.
            lower_data            : lower 'DataPoints' object for 'v's of zigzag detection.
            upper_black_or_whites : 'black' or 'white' data of high_data_points.
            lower_black_or_whites : 'black' or 'white' data of high_data_points.
        
        Returns : 'Chunks' objects.
        """
        
        def gen_sortkey(p,bw) :
            
            symbol = p.symbol
            x = p.x
            if (symbol == self._upper_symbol and bw == 'white') \
                or (symbol == self._lower_symbol and bw == 'black') :
                order = 1
            else :
                order = 2
            return (x,order)
        
        if upper_black_or_whites is None or lower_black_or_whites is None :
            sorted_data_points = [ dp for dp in upper_data ] + [ dp for dp in lower_data ]
            sorted_data_points.sort(key=lambda dp:dp.x)
        else :
            tmp = \
                [ (dp,bw) for dp,bw in zip(upper_data, upper_black_or_whites ) ] \
                + [ (dp,bw) for dp,bw in zip(lower_data, lower_black_or_whites ) ]
            
            tmp.sort(key=lambda dp : gen_sortkey(*dp))
            sorted_data_points = [ dp for (dp,bw) in tmp]
            
        chunks = Chunks([])
        symbol_old = None
        for dp in sorted_data_points :
             
            if dp.symbol != symbol_old :
                chunk = Chunk([],symbol=dp.symbol)
                chunks.append(chunk)
                symbol_old = dp.symbol
            
            chunk.append(dp)
            
        return chunks
