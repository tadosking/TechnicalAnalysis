from math import ceil, floor, sqrt
import numpy as np
import numpy.polynomial.polynomial as npp
from itertools      import chain
from more_itertools import windowed

from . utils.utils    import TrendLineDetectorChunks
from .. DataOrganizer import DataPoints
from . trendline  import TrendLine
from . channlline import ChannelLine


class ChannelLineDetector() :

    
    MIN_WINDOW_SIZE = 4

    
    def __init__(self,max_window_size=5,upper_symbol='H',lower_symbol='L') :
        self.MAX_WINDOW_SIZE = max_window_size
        self.UPPER_SYMBOL = upper_symbol
        self.LOWER_SYMBOL = lower_symbol


    @staticmethod
    def __calc_min_required_size(s) :
        y = floor(s/2) - 2
        x = 2*ceil(sqrt(2*y+0.25)-0.5)
        return s-x
    
    
    @staticmethod
    def order_by_error(xs,cs,errs) :
        
        xs1  , xs2   = xs[cs== 1], xs[cs==-1]
        mu_x1, mu_x2 = xs1.mean(), xs2.mean()
        
        Sxx   = (xs**2).sum()
        v_err = errs.var(ddof=2)
        
        v_confidence1 = ( 1/len(xs1) + (xs1-mu_x1)**2 / Sxx ) * v_err
        v_confidence2 = ( 1/len(xs2) + (xs2-mu_x2)**2 / Sxx ) * v_err
        
        v_confidence = np.zeros(len(errs))
        v_confidence[np.where(cs== 1)] = v_confidence1
        v_confidence[np.where(cs==-1)] = v_confidence2
        
        return ( errs / v_confidence**0.5 ).argsort()
    

    def linear_fit(self, tlchunks) :
        
        std_err_old, std_err = None,None
        while True :
            datapoints = list(chain.from_iterable(tlchunks))
            xs,ys = DataPoints(datapoints).coords.transpose()
            cs = np.vectorize( \
                lambda s:1 if s==self.UPPER_SYMBOL else -1 )( DataPoints(datapoints).symbols )
            
            X = np.array([ (1,0,x) if c == 1 else (0,1,x) for x,c in zip(xs,cs) ])
            coefs = np.linalg.inv(X.transpose().dot(X)).dot(X.transpose()).dot(ys)
            
            ys_fit = X.dot(coefs)
            
            errs = (ys - ys_fit)*cs
                
            std_err_old, std_err = std_err, errs.std(ddof=2)
            if std_err_old and std_err_old < std_err :
                break
            
            iargs = self.order_by_error(xs,cs,errs)
            for i in iargs :
                
                dp = datapoints[i]
                
                if not dp.is_last_one and not dp.protected :
                    dp.remove()
                    break
                
                # if dp.is_last_one == True and ...
                if not dp.protected and not tlchunks.preprotected:
                        
                    datapoints[i-1].parent.marry(datapoints[i+1].parent)
                    dp.remove()

            else :
                break
                
        domain = (xs[0],xs[-1])
        resistance = TrendLine.create_from_xsys(domain, npp.polyval(domain,coefs[[0,2]]), 'R', 
                                                coefs=coefs[[0,2]], 
                                                datapoints=tlchunks.get_chunks_by_symbol(self.UPPER_SYMBOL) )
        support    = TrendLine.create_from_xsys(domain, npp.polyval(domain,coefs[[1,2]]), 'S', 
                                                coefs=coefs[[1,2]],
                                                datapoints=tlchunks.get_chunks_by_symbol(self.LOWER_SYMBOL) )
        
        infos = {
            'domain' : (xs[0],xs[-1]),
            'fitting_method' : 'linear_fit',
            'coefs' : coefs,
            'resid' : (errs**2).sum(),
            'datapoints' : tlchunks.to_datapoints(),
        }

        channelline = ChannelLine.create_from_RSlines(resistance,support,**infos)
        return channelline


    def detect_from_chunks(self,chunks) :
        
        # check
        symbols = chunks.to_datapoints().symbols 
        if np.any( (symbols != self.UPPER_SYMBOL) & (symbols != self.LOWER_SYMBOL) ) :
            raise Exception("chunks includes datapoint with symbol which is not '{}' or '{}'".format(
                            self.UPPER_SYMBOL, self.LOWER_SYMBOL) )
        
        channellines = []
        for s in range(self.MIN_WINDOW_SIZE,min(len(chunks),self.MAX_WINDOW_SIZE)+1,1) :
            
            min_required_size = self.__calc_min_required_size(s)
            for w in windowed(chunks,s) :
                tlchunks = TrendLineDetectorChunks.create_from_chunks(w,min_size=min_required_size)
                channelline = self.linear_fit(tlchunks)
                channellines.append(channelline)
                
        return channellines
