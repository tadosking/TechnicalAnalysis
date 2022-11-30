from typing import Literal, Callable

from .. DataOrganizer import DataPoint, DataPoints
from . utils.sampler_datapoint import SamplerDataPoint
from . utils.sampler_datapoints import SamplerDataPoints



##################################
#### CONVEX SAMPLER DATAPOINT ####
##################################

class ConvexSamplerDataPoint(SamplerDataPoint) :
                
    def calc_convexity(self,w,xmin,xmax) :
        
        v  = self
        vl = self.left
        vr = self.right
        
        if vl :
            dyl = v.y - vl.y
            dxl = v.x - vl.x
        else :
            dyl = 0
            dxl = 2*( v.x - xmin ) + 1
            
        if vr :
            dyr = vr.y - v.y
            dxr = vr.x - v.x
        else :
            dyr = 0
            dxr = 2*( xmax - v.x ) + 1
        
        if dxl+dxr <= w :
            self._convexity = ( dyr/dxr - dyl/dxl ) / ( dxl + dxr )
        else :
            self._convexity = None
            
        return self._convexity
    
    @property
    def convexity(self) :
        return self._convexity


        
###################################
#### CONVEX SAMPLER DATAPOINTS ####
###################################

class ConvexSamplerDataPoints(SamplerDataPoints) :

    DATA_POINT_CLASS = ConvexSamplerDataPoint


        
########################
#### CONVEX SAMPLER ####
########################

class ConvexSampler() :
    """data sampler using 'convexity'.
    you can reduce data by deleting only dipped points (keeping bumped points) and vice versa.
    convexity is calculated to detect dip / bump.
    """    

    def __init__(self,
                 target=Literal['upward','downward','user_defined'],
                 w=10,
                 maxiter=None,
                 evaluator:Callable=None ) :
        """Init and set parameters.

        Args :
            target : 'upward' or 'downward', for deleting 'upward' or 'downward' convex points.
                     you can set 'user_defined' to use user defined function set as 'evaluator'.
            w : evaluate convexity with neighbor datapoints less than w-distance. 
                i.e. any single point in returned datapoints, as a result, don't have its 
                left and right neighbor points in distance greater than w.
                default = 10.
            maxiter : maximum number of trials of iteration.
                      if not set, maxiter will be set to max(1,int(w)).
            evaluator : evaluator function to select datapoints to delete by convexity value, etc.
                        set 'target' arg to 'user_defined' to enable it.
        """
        self._w = w

        self._maxiter = maxiter
        if maxiter is None :
            self._maxiter = max(1,int(w))

        self._target = target

        if target == 'upward' :
            self._evaluator = lambda dp:dp.convexity>0
        elif target == 'downward' :
            self._evaluator = lambda dp:dp.convexity<0
        elif target == 'user_defined':
            if evaluator is None :
                raise Exception("variable 'target' == \"user_defined\" but variable 'evaluator' is not set.")
            else :
                self._evaluator = evaluator
        else :
            raise Exception("invalid value for 'target' : {}.".format(target))


    @property
    def params(self) :

        params = {
            'w' : self._w,
            'maxiter' : self._maxiter,
            'target' : self._target,
        }

        if self._target == 'user_defined' :
            params.update({ 'evaluator_function' : self._evaluator })

        return params


    def _delete_convexes(self,sdps) :
        
        xmin,xmax = sdps.xs[[0,-1]]
        
        def enclosure() :
            
            to_delete = []
            for dp in sdps :
                dp.calc_convexity(self._w,xmin,xmax) 
                if dp.convexity and self._evaluator(dp) :
                    to_delete.append(dp)

            to_delete.sort(key=lambda dp:abs(dp.convexity),reverse=True)

            cnt = 0
            for dp in to_delete :
                if ( dp.left and dp.left.deleted ) or (dp.right and dp.right.deleted ) :
                    continue
                dp.delete()
                cnt += 1

            sdps.update()

            return cnt
       
 
        return enclosure

    
    def sample(self, data:DataPoints ) :
        """Returns sampled datapoints using convex sampling method ( iteratively deletes convexed points )
        
        Args :
            data : 'DataPoints' objects.

        Returns : 'DataPoints' objects.
        """

        sdps = ConvexSamplerDataPoints.create_from_data_points(data)
        delete_convexes = self._delete_convexes(sdps)

        for i in range(self._maxiter) :
            cnt = delete_convexes()
            if cnt == 0 :
                break
            
        return DataPoints([ DataPoint(dp.x,dp.y,index=dp.index,symbol=dp.symbol) for dp in sdps ])
