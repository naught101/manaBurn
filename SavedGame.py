import json
import os

class SavedGame(object):
    def __init__(self):
        self.inventory = []
        self.winStreak = 0
        self.saveFileName = "save.json"
        
    def save(self,inventory,winStreak):
        saveInfo = {'inventoryIDs':inventory, 'winStreak':winStreak}
        try:
            with open(self.saveFileName,'w') as f:
                f.write(json.dumps(saveInfo))
        except IOError as e:
            print(e)
            print('\n\n Sorry, the game cannot be saved.')
        
    def load(self):
        # the load method returns a tuple contain [0] the list of the ID numbers of cards in the
        # inventory and [1] an integer containg how many games have been won. 
        # first, read the file and store its contents
        loadInfo = None
        try:
            with open(self.saveFileName,'r') as f:
                loadInfo = json.load(f)
        except IOException as e:
            print(e)
            print('\n\n Sorry, the game cannot be loaded.')
        self.inventory = loadInfo['inventoryIDs']
        self.winStreak = loadInfo['winStreak']
        return (self.inventory, self.winStreak)
#################
