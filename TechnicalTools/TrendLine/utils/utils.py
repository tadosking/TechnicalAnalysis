from ... DataOrganizer import DataPoint, Chunk, Chunks

class TrendLineDetectorDataPoint(DataPoint) :
    
    def __init__(self, x,y,index=None,symbol=None) :
        super().__init__(x,y,index=index,symbol=symbol)
        
    def set_parent(self,parent) :
        self._parent = parent
        return self
        
    def remove(self) :
        parent = self.parent
        parent._data.remove(self)
        if parent._data == [] :
            parent.remove()
        
    @property
    def parent(self) :
        return self._parent
    
    @property
    def protected(self) :
        if self.parent.protected and len(self.parent) == 1 :
            return True
        else :
            return False
        
    @property
    def is_last_one(self) :
        if len(self.parent) == 1 :
            return True
        return False
        
    @classmethod
    def create_from_datapoint(cls,dp) :
        obj = cls(dp.x,dp.y,dp.index,dp.symbol)
        obj._create_from = dp
        return obj
        
    
class TrendLineDetectorChunk(Chunk) :
    
    def __init__(self,list_of_data_point,symbol=None) :
        super().__init__(list_of_data_point,symbol)
    
    def set_parent(self,parent) :
        self._parent = parent
        return self
    
    def remove(self) :
        parent = self.parent
        parent._data.remove(self)
    
    def marry(me,good_looking_guy) :
        if me is good_looking_guy :
            raise Exception("hey miss chunk ! you can't marry with yourself !!")
        me._data.extend(good_looking_guy._data)

        # new parent is ME. fixed @ Nov 30th, 2022.
        for child in good_looking_guy._data :
            child.set_parent(me)

        good_looking_guy.remove()
    
    @property
    def parent(self) :
        return self._parent
    
    @property
    def protected(self) :
        if self is self.parent._data[0] or self is self.parent._data[-1] :
            return True
        elif self.parent.protected :
            return True
        else :
            return False
        
    @classmethod
    def create_from_chunk(cls,chunk) :
        obj = cls([ TrendLineDetectorDataPoint.create_from_datapoint(dp) for dp in chunk])
        obj._create_from = chunk
        for o in obj :
            o.set_parent(obj)
        return obj
        
class TrendLineDetectorChunks(Chunks) :
    
    def __init__(self,list_of_chunks,min_size=3) :
        super().__init__(list_of_chunks)
        self.MIN_SIZE = min_size
        
    @property
    def protected(self) :
        if len(self) <= self.MIN_SIZE :
            return True
        return False
    
    @property
    def preprotected(self) :
        if len(self) <= self.MIN_SIZE + 1 :
            return True
        return False
       
    @classmethod
    def create_from_chunks(cls,chunks,min_size=3) :
        obj = cls([ TrendLineDetectorChunk.create_from_chunk(c) for c in chunks], min_size=min_size)
        obj._create_from = chunks
        for o in obj :
            o.set_parent(obj)
        return obj
