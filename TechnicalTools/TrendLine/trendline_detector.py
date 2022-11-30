from math import ceil
import numpy.polynomial.polynomial as npp
from itertools import chain
from more_itertools import windowed

from . utils.utils import TrendLineDetectorChunks
from .. DataOrganizer import DataPoints
from . trendline import TrendLine


class TrendLineDetector() :    

    
    MIN_WINDOW_SIZE = 3

    
    def __init__(self,rs,max_window_size) :
        """
        Init.
        
        Args :
            rs : 'R'esistance or 'S'upport.
            max_window_size : detector use 'max_window_size' subchunks to fit trend line.
        """
        
        if rs not in ('S', 'R') :
            raise Exception("'rs' must be 'S' or 'R'.")
            
        self.RS = rs
        self.MAX_WINDOW_SIZE = max_window_size

    
    @staticmethod
    def order_by_error(xs,errs) :
        
        mu_x = xs.mean()
        Sxx  = (xs**2).sum()
        v_err = errs.var(ddof=2)
        v_confidence = ( 1/(len(xs)) + (xs-mu_x)**2 / Sxx ) * v_err
        
        return ( errs / v_confidence**0.5 ).argsort()
    

    def linear_fit(self, tlchunks) :
        
        std_err_old, std_err = None,None
        while True :
            datapoints = list(chain.from_iterable(tlchunks))
        
            xs,ys = DataPoints(datapoints).coords.transpose()
            coefs,(resid,*_) = npp.polyfit(xs,ys,deg=1,full=True)
            resid = resid[0]

            ys_fit = npp.polyval(xs,coefs)
            
            errs = ys - ys_fit
            if self.RS == 'S' :
                errs = -1 * errs
                
            std_err_old, std_err = std_err, errs.std(ddof=2)
            if std_err_old and std_err_old < std_err :
                break
            
            iargs = self.order_by_error(xs,errs)
            for i in iargs :
                dp = datapoints[i]
                if not dp.protected :
                    dp.remove()
                    break
            else :
                break
                
        
        infos = {
            'type' : self.RS,
            'domain' : (xs[0],xs[-1]),
            'fitting_method' : 'linear_fit',
            'coefs' : coefs,
            'resid' : resid,
            'R2' : 1 - resid/((ys-ys.mean())**2).sum(),
            'datapoints' : tlchunks.to_datapoints(),
        }

        trendline = TrendLine.create_from_xsys(xs[[0,-1]],ys_fit[[0,-1]],self.RS,**infos)
        return trendline
    
    
    def detect_from_chunks(self,chunks) :
        """
        detect trend lines from passed chunks.
        iterative linear fitting method is used.
        
        Args : 
            chunks : 'Chunks' object. 
                     call chunks.get_chunks_by_symbol('*') before passing to the method if required.
            
        Returns : list of 'TrendLine' objects.
        """
        
        trendlines = []
        for s in range(self.MIN_WINDOW_SIZE,min(len(chunks),self.MAX_WINDOW_SIZE)+1,1) :
            
            min_required_size = ceil(1+s/2)
            for w in windowed(chunks,s) :
                tlchunks = TrendLineDetectorChunks.create_from_chunks(w,min_size=min_required_size)
                trendline = self.linear_fit(tlchunks)
                trendlines.append(trendline)
                
        return trendlines
