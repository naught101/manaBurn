# this class handles all the graphics for the main game screen and when a mode is selected,
# it creates a MenuScreen object and should fall out of reference

import sfml as sf
import MainScreen
import SavedGame

class MenuScreen(object):
    def __init__(self,window):
        self.window = window

    def startNewGame(self):
        newSavedGame = SavedGame()