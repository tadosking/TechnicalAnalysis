import numpy as np
from . utils.line import Line


class TrendLine(Line) :
    """Represents a trendline and provides utilities."""
    
    def _set_initial_infos(self,rs,domain) :

        self._rs = rs
        
        x0,x1 = domain
        self._domain = (min(x0,x1),max(x0,x1))

        self._infos = {
            'slope' : self._slope,
            'intercept' : self._intercept,
            'resistance/support' : self._rs,
            'x-domain' : self._domain
        }
        
        
    def __init__(self,slope:float,intercept:float,rs:str='unknown',domain:tuple=(0,1)) :

        super().__init__(slope,intercept)
        self._set_initial_infos(rs,domain)
        
        
    def __repr__(self) :
        s = '{}(slope={},intercept={},rs=\'{}\',domain={})'.format(
            self.__class__.__name__,
            self.slope,self.intercept,self.rs,self.domain )
        
        return s
    
    @property
    def rs(self) :
        return self._rs
    
    @property
    def domain(self) :
        return self._domain
    
    @property
    def infos(self) :
        return self._infos
    
    @property
    def xs(self) :
        return np.array(self.domain)
    
    @property
    def ys(self) :
        return self.x2y(self.domain)
    
    @property
    def coords(self) :
        return np.concatenate((self.xs,self.ys)).reshape(-1,len(self.xs)).transpose()
    
    @property
    def length(self) :
        x1,x2 = self.domain
        return x2-x1
    
    def calc_dy_out_of_line(self,x,y) :
        if self.rs == 'R' :
            dy = self.calc_ydistance(x,y)
        elif self.rs == 'S' :
            dy = -self.calc_ydistance(x,y)
        
        if hasattr(dy,'__iter__') :
            dy[dy<0] = 0
        
        return dy
            
    def add_infos(self,**kwargs) :
        self._infos.update(kwargs)
    
    @classmethod
    def create_from_points(cls,p1,p2,rs:str='unknown',**kwargs) :
        """Creates 'TrendLine' object with two points.
        
        Args :
            p1 : a point.
            p2 : other point.
            rs : 'R' or 'S' for representing resistance or support. default = 'unknown'.
            **kwargs : if set, stored in '.infos' variable.
        """
            
        try :
            obj = super().create_from_points(p1,p2)
        except Exception as e :
            raise(e)
            
        obj._set_initial_infos(rs,(p1.x,p2.x))
        obj._infos.update(kwargs)
        
        return obj
    
    @classmethod
    def create_from_xsys(cls,xs,ys,rs:str='unknown',**kwargs) :
        """Creates 'TrendLine' object with x/y data.
        
        Args :
            xs : x-coordinates. len(xs) must be 2.
            ys : y-coordinates. len(ys) must be 2.
            rs : 'R' or 'S' for representing resistance or support. default = 'unknown'.
            **kwargs : if set, stored in '.infos' variable.
        """
        
        try :
            obj = super().create_from_xsys(xs,ys)
        except Exception as e :
            raise(e)
            
        obj._set_initial_infos(rs,tuple(xs))
        obj._infos.update(kwargs)
        
        return obj
