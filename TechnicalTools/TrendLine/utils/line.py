import numpy as np
from ... DataOrganizer import DataPoint


class Line() :
    """Represents a line and provides utilities.
    A line is represented by 'slope' and 'intercept' parameter.
    """
    
    def __init__(self,slope,intercept) :
        """Init.
        
        Args :
            slope : slope value.
            intercept : intercept value.
        """
        
        self._slope = slope
        self._intercept = intercept
        
        
    @property
    def slope(self) :
        return self._slope
    
    
    @property
    def intercept(self) :
        return self._intercept
    
    
    def __repr__(self) :
        s = '{}(slope={},intercept={})'.format(
            self.__class__.__name__,self.slope,self.intercept)
        return s
    
    
    def __str__(self) :
        s = 'l(x) := {} * x + {}'.format(self._slope, self._intercept)
        return self.__repr__() 
        
        
    def x2y(self,x) :
        """Returns l(x).
        """            
        if hasattr(x,'__iter__') :
            return np.array([ self.intercept + self.slope * x_ for x_ in x ])
        else :
            return self.intercept + self.slope * x    

    
    def calc_ydistance(self,x,y) :
        """Returns y - l(x).
        """
        
        if hasattr(x,'__iter__') and hasattr(y,'__iter__') :
            return np.array([ y_ - self.x2y(x_) for x_,y_ in zip(x,y)])
        else :
            return y - self.x2y(x)

    
    @classmethod
    def create_from_points(cls,p1,p2) :
        """Returns 'Line' object from two points.
        """
        
        if p1.x == p2.x :
            raise Exception('must be p1.x != p2.x .')
        
        if p1.x > p2.x :
            p1,p2 = p2,p1
        
        slope = (p2.y-p1.y) / (p2.x-p1.x)
            
        intercept = p1.y - slope * p1.x    
        return cls(slope,intercept)
        
    @classmethod
    def create_from_xsys(cls,xs,ys) :
        """Returns 'Line' object from x & y.
        """

        x1,x2 = xs
        y1,y2 = ys
       
        if x1 == x2 :
            raise Exception('must be xs[0] != xs[1].')
 
        slope = (y2-y1)/(x2-x1)
        intercept = y1 - slope*x1

        return cls(slope,intercept) 
