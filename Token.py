import sfml as sf
import os
import urllib
from Card import Card

class Token(Card):
    maxY = 150
    velocity = 2
    
    def update(self,surface,allTokens):
        if self.canMove(allTokens):
            self.y -= self.velocity
        super(Token,self).update(surface)
    
    def canMove(self,allTokens):
        if self.y <= self.maxY:
            return False
        for token in  allTokens:
            if (token.y < self.y) and (self.y - self.velocity) < (token.y  + token.outlineHeight + 5 ):
                if token is not self:
                    return False
        return True
    
    def getHoverImage(self):
        pass 
            
            
class Equipment(Token):
    minY = 825
    velocity = -2
    def __init__(self,multiverseID,power,toughness,x,y):
        super(Equipment,self).__init__(multiverseID,power,toughness,x,y)
        self.defaultColor = sf.Color.BLUE
        self.altColor = sf.Color.GREEN
        self.currentColor = self.defaultColor
        self.outline.size = (self.outlineWidth,self.outlineHeight)
        self.getHoverImage()
        
    def canMove(self,allTokens):
        if self.y >= self.minY:
            return False
        for token in  allTokens:
            if (token.y > self.y) and (self.y + self.outlineHeight + 5 + self.velocity) < (token.y):
                if token is not self:
                    return False
        return True
        
    def getHoverImage(self):
        super(Token,self).getHoverImage()
        