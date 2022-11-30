from typing import Literal

from .. DataOrganizer import DataPoint,DataPoints
from . utils.sampler_datapoint import SamplerDataPoint
from . utils.sampler_datapoints import SamplerDataPoints



##########################################
#### LOCAL MIN MAX SAMPLER DATA POINT ####
##########################################

class LocalMinMaxSamplerDataPoint(SamplerDataPoint) :
    
    
    def _get_neighbors(self, d) :
        
        neighbors = [self]
        
        v = self
        while True :
            v = v.left
            if v is None or self.x - v.x > d :
                break
                
            neighbors.append(v)
            
        v = self
        while True :
            v = v.right
            if v is None or v.x - self.x > d :
                break
            
            neighbors.append(v)

        return neighbors
    
    
    def is_localmin(self, d) :
        
        neighbors = self._get_neighbors(d)
        dp_localmin, *_ = sorted(neighbors, key=lambda dp:dp.y, reverse=False)
        
        if self is dp_localmin :
            return True
        else :
            return False
 

    def is_localmax(self, d) :
        
        neighbors = self._get_neighbors(d)
        dp_localmax, *_ = sorted(neighbors, key=lambda dp:dp.y, reverse=True)
        
        if self is dp_localmax :
            return True
        else :
            return False



###########################################
#### LOCAL MIN MAX SAMPLER DATA POINTS ####
###########################################

class LocalMinMaxSamplerDataPoints(SamplerDataPoints) :
    
    DATA_POINT_CLASS = LocalMinMaxSamplerDataPoint            



##########################################
#### LOCAL MIN MAX SAMPLER DATA POINT ####
##########################################

class LocalMinMaxSampler() :
    """Data Sampler using local min/max method. (swing low/high method)
    """ 

    def __init__(self, method:Literal['min','max'], d=6) :
        """Init and set parameters.

        Args :
            method : 'min' or 'max', for sampling only local 'min' or 'max' data points.
            d : evaluate if a datapoint is local min/max among left and right neighbors within 'd'-distance. 
                default=6.
        """

        self._method = method
        self._d = d


    @property
    def params(self) :
        return {
            'method' : 'local_{}'.format(self._method),
            'd' : self._d
        }

    
    def sample(self, data:DataPoints ) :
        """Returns sampled datapoints using local min/max (also called as swing high/low) method.
        
        Args :
            data : 'DataPoints' objects.
            
        Returns : 'DataPoints' objects.
        """
    
        lmmdps = LocalMinMaxSamplerDataPoints.create_from_data_points(data)
        
        sampled_dps = []
        for dp in lmmdps :
            if ( self._method == 'min' and dp.is_localmin(self._d) ) \
                or (self._method == 'max' and dp.is_localmax(self._d) ) :
                sampled_dps.append(dp)

        return DataPoints([ DataPoint(dp.x,dp.y,index=dp.index,symbol=dp.symbol) for dp in sampled_dps])
        
        
