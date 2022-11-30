import numpy as np
from typing import List
from . datapoint import DataPoint

class DataPoints() :
    """'DataPoints' objects stores 'DataPoint' objects and then provides many utilities.
    'DataPoints' object supports slicing.
    Use like : datapoints[1], datapoints[1:3:2]
    You can also use like : datapoints[[0,2,5]], to extract arbitral datapoint data.
    """
    
    DATA_POINT_CLASS = DataPoint
    
    def __init__(self,list_of_data_point:List[type(DataPoint)]) :
        """Init.
        
        Args :
            list_of_datapoint : list of 'DataPoint' objects.
                                list elements must be ordered by x.
        """
        self._data_points = list_of_data_point


    def __iter__(self) :
        for dp in self._data_points :
            yield dp

            
    def __repr__(self) :
        s = '{}([{}])'.format(self.__class__.__name__, ','.join([ repr(dp) for dp in self] ))
        return s

        
    def __str__(self) :
        s = '[{}]'.format('\n,'.join([ '(x={},y={})'.format(dp.x,dp.y) for dp in self ]))
        return s

    
    def __len__(self) :
        cnt = 0
        for _ in self :
            cnt += 1
        return cnt

    
    def __getitem__(self,idx) :
        tmp = [ dp for dp in self ]
        if hasattr(idx,'__iter__') :
            return self.__class__([ tmp[i] for i in idx ])
        elif isinstance(idx,slice) :
            return self.__class__(tmp[idx])
        else :
            return tmp[idx]

    
    @classmethod
    def create_from_xsys(cls,xs,ys,indices=None,symbols=None) :
        """Returns new 'DataPoints' objects from x-coordinate and y-coodinate values.
        
        Args :
            xs : x-coodinate values.
            ys : y-coodinate values.
            indices : index values. (optional)
            symbols : symbol strings. (optional)
        """
        
        if indices is not None and symbols is not None :
            return cls([cls.DATA_POINT_CLASS(x,y,index=i,symbol=symbol) for x,y,i,symbol in zip(xs,ys,indices,symbols) ])
        elif indices is not None :
            return cls([cls.DATA_POINT_CLASS(x,y,index=i) for x,y,i in zip(xs,ys,indices) ])
        elif symbols is not None :
            return cls([cls.DATA_POINT_CLASS(x,y,symbol=symbol) for x,y,symbol in zip(xs,ys,symbols) ])
        else :
            return cls([cls.DATA_POINT_CLASS(x,y) for x,y in zip(xs,ys) ])


    @classmethod
    def create_from_coords(cls,coords,indices=None,symbols=None) :
        """Returns new 'DataPoints' objects from (x,y)-coodinate values.
        
        Args :
            coords : (x,y)-coodinate values.
            indices : index values. (optional)
            symbols : symbol strings. (optional)
        """
        
        xs = ( c[0] for c in coords)
        ys = ( c[1] for c in coords)
        
        return cls.create_from_xsys(xs,ys,indices=indices,symbols=symbols)
        
        
    @classmethod
    def create_from_candles(cls,candles,ohlcv) :
        """This class method is used as a convertor from 'Candles' objects to 'DataPoints' objects. 
        You must specify 'ohlcv' to convert.
        
        Args :
            candles : 'Candles' objects.
            ohlcvs : ohlcv to convert. choose within :
                'O' -- open
                'H' -- high
                'L' -- low
                'C' -- close
                'V' -- volume
                'CT' -- candle top
                'CB' -- candle bottom
        """

        xs = np.arange(len(candles))
        
        if ohlcv == 'O' :
            values = candles.opens
        elif ohlcv == 'H' :
            values = candles.highs
        elif ohlcv == 'L' :
            values = candles.lows
        elif ohlcv == 'C' :
            values = candles.closes
        elif ohlcv == 'V' :
            values = candles.volumes
        elif ohlcv == 'CT' :
            values = candles.candle_tops
        elif ohlcv == 'CB' :
            values = candles.candle_bottoms
        else :
            raise Exception("incorrect 'ohlcv' value : '{}'.".format(ohlcv))

        try :
            indices = candles.indices
            return cls([ cls.DATA_POINT_CLASS(x,y,index=i,symbol=ohlcv) for x,y,i in zip(xs,values,indices)])
        except :
            return cls([ cls.DATA_POINT_CLASS(x,y,symbol=ohlcv) for x,y in zip(xs,values)])

        
    @property
    def xs(self) :
        return np.array([ dp.x for dp in self ])
      
        
    @property
    def ys(self) :
        return np.array([ dp.y for dp in self ])

    
    @property
    def coords(self) :
        return np.array([ c for c in zip(self.xs,self.ys)])

    
    @property
    def indices(self) :
        return np.array([ dp.index for dp in self])

    
    @property
    def symbols(self) :
        return np.array([ dp.symbol for dp in self])

    
    def copy(self) :
        """Returns copy of 'DataPoints' objects."""
        return self.__class__([ v.copy() for v in self])
