## Card class

import sfml as sf
import os
import urllib
import urllib.request


    
class Card(sf.Drawable):

    font = sf.Font.from_file(os.getcwd()+"\\res\\arial.ttf")

    def __init__(self,multiverseID,power,toughness,x=0,y=0,extraText=""):
        self.multiverseID = multiverseID
        self.x = x
        self.y = y
        self.alive = True
        self.outlineWidth = 700
        self.outlineHeight = 16
        self.power = str(power)
        self.toughness = str(toughness)
        self.hoverTexture = None
        self.hoverSprite = None
        self.canDisplayImage = False
        self.defaultColor = sf.Color.WHITE
        self.altColor = sf.Color.RED    
        self.currentColor = self.defaultColor
        self.outline = sf.RectangleShape()
        self.outline.size = (self.outlineWidth,self.outlineHeight)
        self.outline.outline_color = self.currentColor
        self.outline.outline_thickness = 2
        self.outline.fill_color = sf.Color.TRANSPARENT
        self.outline.position = (self.x,self.y)
        self.extraText = extraText
        self.textContent = (self.power + " / " + self.toughness + "  " + extraText)
        
    def draw(self,surface):
        text = sf.Text(self.textContent)
        text.font = self.font
        text.character_size = 10
        text.color = sf.Color.WHITE
        text.position = (self.x + 2, self.y + 2)
        self.outline.outline_color = self.currentColor
        self.outline.position = (self.x,self.y)
        surface.draw(text)
        surface.draw(self.outline)
        mouseX,mouseY = surface.map_pixel_to_coords(sf.Mouse.get_position(surface))
        if self.canDisplayImage:
            self.hoverSprite.position = sf.Vector2(mouseX, self.y + 3)        
            if type(self) is not Card:
                self.hoverSprite.position = sf.Vector2(mouseX,self.y - self.hoverSprite.texture.height)
        if self.check_hover(mouseX,mouseY) and self.canDisplayImage:
            aspectX = surface.width
            aspectY = surface.height
            self.hoverSprite.ratio = (1100/aspectX,850/aspectY)
            surface.draw(self.hoverSprite)
        
    
    def update(self,surface):
        if self.alive:
            self.draw(surface)
        
            
    def check_hover(self,mouseX,mouseY):
        if(mouseX > self.x and mouseX < self.x + self.outlineWidth):
            if (mouseY > self.y and mouseY < self.y + self.outlineHeight):
                return True
            else:return False
        else:
            return False
            
        
    def move(self,x,y):
        self.x = x
        self.y = y
        
    def toggle(self):
        if self.currentColor == self.defaultColor:
            self.currentColor = self.altColor
        else:
            self.currentColor = self.defaultColor
        
    def kill(self):
        self.alive = False
        
        
    def getHoverImage(self):
        succeeded = False
        try:
            imageRequest = urllib.request.urlopen("http://gatherer.wizards.com/Handlers/Image.ashx?multiverseid=" + str(self.multiverseID) + "&type=card")
            imageData = imageRequest.read()
            self.hoverTexture = sf.Texture.from_memory(imageData)
            self.hoverSprite = sf.Sprite(self.hoverTexture)
            self.hoverSprite.color = sf.Color(255,255,255,225)
            succeeded = True
        except Exception as e:
            print(e)
        self.canDisplayImage = succeeded
        

