from ... DataOrganizer import DataPoint

class SamplerDataPoint(DataPoint) :
    
    def __init__(self,x,y,index,symbol) :
        super().__init__(x,y,index=index,symbol=symbol)
        
        self._deleted = False
        self._left  = None
        self._right = None
    
    @property
    def deleted(self) :
        return self._deleted
    
    @property
    def left(self) :
        return self._left
    
    @property
    def right(self) :
        return self._right
    
    def delete(self) :
        self._deleted = True
        
    def update(self) :
        self.update_left() 
        self.update_right()
        
    def update_left(self) :
        v = self
        while True :
            v = v.left
            if v is None or v.deleted == False :
                self._left = v
                break
            
    def update_right(self) :
        v = self
        while True :
            v = v.right
            if v is None or v.deleted == False :
                self._right = v
                break


