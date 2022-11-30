from typing import List
from .. DataOrganizer import DataPoint, DataPoints


class ZigZag(DataPoints) :
    """Subclass of 'DataPoints' for representing zigzag."""

    
    def __init__(self, list_of_data_point:List[DataPoint], upper_symbol:str, lower_symbol:str) :
        super().__init__(list_of_data_point)
        self._upper_symbol = upper_symbol
        self._lower_symbol = lower_symbol


    @property
    def params(self) :
        return {
            'upper_symbol' : self._upper_symbol,
            'lower_symbol' : self._lower_symbol
        }


    @property
    def upper_points(self) :
        return DataPoints([ dp for dp in self if dp.symbol == self._upper_symbol])


    @property
    def lower_points(self) :
        return DataPoints([ dp for dp in self if dp.symbol == self._lower_symbol])
