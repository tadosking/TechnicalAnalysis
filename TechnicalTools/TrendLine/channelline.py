class ChannelLine() :
    """Represents a channel line.
    A channel line has upper(resistance) & lower(support) lines, optionally mid line.
    """
    
    
    def __init__(self,resistance_line,support_line) :

        self._resistance_line = resistance_line
        self._support_line = support_line
        
        self._domain = ( min(resistance_line.domain[0], support_line.domain[0])
                        , max(resistance_line.domain[1], support_line.domain[1]) )
        
        self._infos = {
            'x-domain' : self._domain,
            'resistance_line' : self._resistance_line,
            'support_line' :self._support_line,
        }
        
        
    def __repr__(self) :
        s = '{}(resistance_line={},support_line={})'.format(
            self.__class__.__name__,
            self._resistance_line, self._support_line )
        
        return s
    
    @property
    def resistance_line(self) :
        return self._resistance_line
    
    @property
    def support_line(self) :
        return self._support_line
    
    @property
    def infos(self) :
        return self._infos
    
    @property
    def domain(self) :
        return self._domain
    
    @property
    def length(self) :
        return self.x_end - self.x_start
        
    @classmethod
    def create_from_RSlines(cls,resistance_line,support_line,**kwargs) :
        """Creates 'ChannelLine' object binding resistance & support lines.
        
        Args :
            resistance_line : 'TrendLine' object representing resistance line.
            support_line : 'TrendLine' object representing support line.
            **kwargs : pass any key=value type arguments, it will be included in .infos property. 
            
        Returns : 'ChannelLine' object.
        """
        obj = cls(resistance_line,support_line)
        obj._infos.update(kwargs)
        
        return obj
        
