
# This class holds all the games rules.
# This handles token creation, message generation,
# 

from Token import Token
import random

class RuleTables(object):

    
    def __init__(self,dice,mainScreen,currentTable = 1):
        self.table0 = {
            1:[(lambda :self.message(self.skipString)),  (lambda:self.advanceTable())],
            2:[(lambda :self.message(self.skipString)),  (lambda:self.advanceTable())],
            3:[(lambda :self.message(self.skipString)),  (lambda:self.advanceTable())],
            4:[(lambda :self.message(self.skipString)),  (lambda:self.advanceTable())],
            5:[(lambda :self.message(self.skipString)),  (lambda:self.advanceTable())],
            6:[(lambda :self.message(self.skipString)),  (lambda:self.advanceTable())],
            7:[(lambda :self.message(self.skipString)),  (lambda:self.advanceTable())],
            8:[(lambda x="DEEP IQ sends your best creature to your graveyard.":self.message(x)),  (lambda:self.advanceTable())],
            9:[(lambda x=-4:self.setModifier(x)), (lambda :self.createToken(1,1)), (lambda:self.advanceTable())],
            10:[(lambda x=-4:self.setModifier(x)), (lambda :self.createToken(1,1))]
        }
            
            
        self.table1 = {
        
        }       
        
        
        self.table2 = {
        
        }
        
        
        self.table3 = {
        
        }
        
        
        self.table4 = {
        
        }
    
        
        self.table5 = {
        
        }    
        
    
    
        
        self.tables = [self.table0,self.table1,self.table2,self.table3,self.table4,self.table5]
        
        
        self.tokenChart = {
        1:" ",
        2:"+2/+0 and first strike.",
        3:"Regeneration. -1/-1",
        4:"+0/+3 and defender.",
        5:"First strike.",
        6:"Protection from your best creature color",
        7:"Deathtouch.",
        8:"+2/+2, flying, lifelink.",
        9:"Haste and trample.",
        10:"+2/+2 trample, lifelink.",
        11:"Flying and trample.",
        12:"Protection from your best creature and vigilance.",
        13:"When this creature enters the battlefield, sacrifice one of your creatures at random.",
        14:"First strike and shroud.",
        15:"Protection from your best creature color, deathtouch, and your weakest creature becomes unblockable.",
        16:"When this creature enters the battlefield, exile target permanent you control."
        }
        
        
        self.spookyChart = {
        
        }     
        
        self.dice = dice
        self.chartModifier = 0
        self.currentTableNumber = 0
        self.mainScreen = mainScreen
        self.currentTable = self.tables[self.currentTableNumber]
        self.skipString = "DEEP IQ does nothing this turn."
        
           
        
    def rollTable(self):
        roll = random.randint(1,10)
        for action in self.currentTable[roll]:
            action()
        
    
    def advanceTable(self):
        pass
        #self.currentTableNumber += 1
        #self.currentTable = self.tables[self.currentTableNumber]
        
    def goToTable(self,number):
        self.currentTableNumber = number
        self.currentTable = self.tables[self.currentTableNumber]
        
    def setModifier(self,modifier):
        self.chartModifier = modifier
    
    def message(self,message):
        self.dice.newMessage(message)
        
    def createToken(self,power,toughness):
        roll = random.randint(1,10) + self.chartModifier
        # clip the modified roll to fit in the chart 
        if roll < 1 : roll = 1
        if roll > 16 : roll = 16
        text = self.tokenChart[roll]
        token = Token(0,power,toughness,extraText=text,x=25,y=650)
        self.mainScreen.tokens.append(token)
        
        

    
    
