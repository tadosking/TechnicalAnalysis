from ... DataOrganizer import DataPoints
from .sampler_datapoint import SamplerDataPoint

class SamplerDataPoints(DataPoints) :

    DATA_POINT_CLASS = SamplerDataPoint
    
    def __init__(self,list_of_data_point):
        
        list_of_data_point[ 0]._right = list_of_data_point[ 1]
        list_of_data_point[-1]._left  = list_of_data_point[-2]
        for pl,p,pr in zip(list_of_data_point,list_of_data_point[1:],list_of_data_point[2:]) :
            p._left  = pl
            p._right = pr
        
        self._data_points = list_of_data_point
        
    def __iter__(self) :
        for dp in self._data_points :
            if dp.deleted :
                continue
            yield dp
            
    @classmethod
    def create_from_data_points(cls,datapoints) :
        return cls([cls.DATA_POINT_CLASS(dp.x,dp.y,index=dp.index,symbol=dp.symbol) for dp in datapoints])
        
    def update(self) :
        for dp in self._data_points :
            dp.update()
