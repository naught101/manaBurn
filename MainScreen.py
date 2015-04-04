# the main screen excpects to passed a SavedGame object contain save information.
import SavedGame
import MenuScreen
import sfml as sf
import random
import os
import json
from Card import Card
from Token import Token
from Token import Equipment
from RuleTables import RuleTables


class MainScreen(object):
    def __init__(self,window,view,savedGame,allCardData):
        self.window = window
        self.view = view
        self.playField = []
        self.tokens = []
        self.equipment = []
        self.bossCard = self.getRandomCard(allCardData,"Creature")
        self.bossCard.x = 25
        self.bossCard.y = 110
        self.bossCard.getHoverImage()
        self.playerHP = 20
        self.enemyHP = 20
        
        #### CREATE GUI ELEMENTS HERE
        self.enemyHPBox = HPBox(900,200,100,100,20)
        self.playerHPBox = HPBox(900,725,100,100,20)
        self.divider = sf.RectangleShape()
        self.divider.size = (1500,4)
        self.divider.outline_color = sf.Color.CYAN
        self.divider.position = (0,700)
        self.divider.fill_color = sf.Color(0,100,255,255)
        self.maxNumberOfTokens = 15
        self.HPBoxes = [self.enemyHPBox, self.playerHPBox]
        self.dice = Dice(self,self.tokens)
        self.dice.x,self.dice.y = (850,25)
        self.dice.tables.createToken(4,2)
        
        #self.equipment.append(Equipment(247337,0,0,x=55,y=685))
        self.equipment.append(Equipment(247337,0,0,x=55,y=715))
        
        #############################
        
        
    ##### DRAW ALL MAIN SCREEN GRAPHICS    
    def update(self):
        self.window.draw(self.divider)
        self.enemyHPBox.update(self.window)
        self.playerHPBox.update(self.window)
        self.playerHP = self.playerHPBox.hp
        self.enemyHP = self.enemyHPBox.hp
        for token in self.tokens:
            token.update(self.window,self.tokens)
        for equipment in self.equipment:
            equipment.update(self.window,self.equipment)
        self.bossCard.update(self.window)
        self.dice.update(self.window)
            
            
    def getRandomCard(self, allCardData,typeSearch):
        #NOTE THAT THIS METHOD IS SPECIFIC TO THE FORMAT OF MTG CARDS FROM THE mtg JSON project    
        #print json.dumps(allCardData, sort_keys=True,indent=4, separators=(',', ': '))
        select = None
        allCards = []
        for cardSet in allCardData.values():
            for card in cardSet["cards"]:
                allCards.append(card)
        #for card in allCards:print card["name"]
        select = random.choice(allCards)
        while typeSearch not in select["types"] or "multiverseid" not in select:
            select = random.choice(allCards)
        
        power = 0
        toughness = 0
        
        if "power" in select:
            power = select["power"]
        else:
            power = 0
            
        if "toughness" in select:
            toughness = select["toughness"]
        else:
            toughness = 0

        multiverseid = (select['multiverseid'])
        cardObject = Card(multiverseid,power,toughness)
        return cardObject
    
    def checkClicks(self,screen,event):
        mouseX,mouseY = screen.map_pixel_to_coords(sf.Mouse.get_position(screen))
        for token in self.tokens + self.equipment:
            if token.check_hover(mouseX,mouseY):
                if sf.Mouse.is_button_pressed(sf.Mouse.LEFT):
                    token.toggle()
                if sf.Mouse.is_button_pressed(sf.Mouse.RIGHT):
                    token.kill()
        if self.dice.check_hover(mouseX,mouseY):
            if sf.Mouse.is_button_pressed(sf.Mouse.LEFT):
                self.dice.clicked()
            
                    
    def checkScroll(self,screen,event):
        mouseX,mouseY = screen.map_pixel_to_coords(sf.Mouse.get_position(screen))
        for box in self.HPBoxes:
            if box.check_hover(mouseX,mouseY):
                box.hp += event.delta
                    
                    
                    
    def cleanUp(self):
        # Reassign the list of tokens to a list of only the ones that
        # are still alive
        tempTokens = [token for token in self.tokens if token.alive]
        self.tokens = tempTokens

        
        
        
    
# # #        
#################################################
class HPBox(sf.Drawable):
    font = sf.Font.from_file(os.getcwd()+"\\res\\arial.ttf")
    def __init__(self,x,y,width,height,hp):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.hp = hp
        self.hovered = False
        self.characterDead = False
        
        box = sf.RectangleShape()
        box.size = (self.width,self.height)
        box.outline_color = sf.Color.WHITE
        box.outline_thickness = 3
        box.fill_color = sf.Color.TRANSPARENT
        box.position = (self.x,self.y)
        self.box = box
        
    def draw(self,window):
        text = sf.Text(str(self.hp))
        text.font = self.font
        text.position = (self.x+20,self.y+20)
        text.character_size = 50
        text.color = sf.Color.RED
        window.draw(text)
        window.draw(self.box)
    
    def update(self,window):
        #CLIP THE HP BOX TEXT TO 2 DIGITS
        if self.hp < -99: self.hp = -99
        if self.hp > 99: self.hp = 99
        if self.hp <= 0:
            self.characterDead = True
        self.draw(window)
        
    def check_hover(self,mouseX,mouseY):
        if(mouseX > self.x and mouseX < self.x + self.width):
            if (mouseY > self.y and mouseY < self.y + self.height):
                return True
            else:return False
        else:
            return False
            
# This class creates     
class Dice(sf.Drawable):
    font = sf.Font.from_file(os.getcwd()+"\\res\\arial.ttf")
    def __init__(self,mainScreen,ruleTables,x=0,y=200,width=200,height=75,text="DEEP IQ's Turn"):
        self.tables = RuleTables(self,mainScreen)
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.text = text
        self.message = "DEEP IQ waits idly. "
        self.coolDown = sf.Clock()
        self.canBeClicked = True
        self.mainScreen = mainScreen
        box = sf.RectangleShape()
        box.size = (self.width,self.height)
        box.outline_color = sf.Color.WHITE
        box.outline_thickness = 3
        box.fill_color = sf.Color.TRANSPARENT
        box.position = (self.x,self.y)
        self.box = box
        
        buffers = [sf.SoundBuffer.from_file(os.path.join(os.getcwd(),"res" ,"dice0.ogg")),
        sf.SoundBuffer.from_file(os.path.join(os.getcwd(),"res" ,"dice0.ogg")),
        sf.SoundBuffer.from_file(os.path.join(os.getcwd(),"res" ,"dice1.ogg")),
        sf.SoundBuffer.from_file(os.path.join(os.getcwd(),"res" ,"dice2.ogg")),
        sf.SoundBuffer.from_file(os.path.join(os.getcwd(),"res" ,"dice3.ogg")),
        sf.SoundBuffer.from_file(os.path.join(os.getcwd(),"res" ,"dice4.ogg"))]
        
        self.sounds = []
        for buffer in buffers:
            sound = sf.Sound()
            sound.buffer = buffer
            self.sounds.append(sound)
        
        
    def draw(self,window):
        self.box.position = (self.x,self.y)
        text = sf.Text(self.text)
        text.font = self.font
        text.position = (self.x+20,self.y+20)
        text.character_size = 12
        text.color = sf.Color.RED
        
        messageText = sf.Text(self.message)
        messageText.font = self.font
        messageText.position = (15,15)
        messageText.character_size = 20
        messageText.color = sf.Color.RED
        window.draw(text)
        window.draw(messageText)
        window.draw(self.box)
        
    def update(self,window):
        if self.coolDown.elapsed_time.seconds > 1.5:
            self.canBeClicked = True
            self.box.outline_color = sf.Color.WHITE
        else:
            self.canBeClicked = False
            self.box.outline_color = sf.Color.RED
        self.draw(window)
        
    def check_hover(self,mouseX,mouseY):
        if(mouseX > self.x and mouseX < self.x + self.width):
            if (mouseY > self.y and mouseY < self.y + self.height):
                return True
            else:return False
        else:
            return False

            
    def clicked(self):
        if self.canBeClicked:
            self.coolDown.restart()
            self.canBeClicked = False
            random.choice(self.sounds).play()
            self.tables.rollTable()
            
    def newMessage(self,message):
        self.message = message