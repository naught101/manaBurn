#!/usr/bin/python
# -*- coding: utf-8 -*-
####################
## Mana Burn      ##
## Mardigon Toler ##
####################

# Mana Burn is a single player format
# for Magic the Gathering based on
# the Deep IQ MTG format.
#
# for card images, I use the api located at (http://api.mtgdb.info/)
#
# Each round has a boss which acts as the enemy planeswalker. It attacks when a perfect 10 (without modifiers) is rolled.
# The boss drops loot if the game is won, the mana cost of which is equal to the boss's mana cost.
# Loot is a spell that can be cast at any time in a future game without paying its cost. Only 3 canbe in the inventory.
# If the inventory is full at the end of a match, no loot is picked up.
#
# Do I need to balance the gameplay at all to account for loot advantage?
# Also, keep track of winning streaks so that difficulty(enemy roll modifiers) increases.
# Losses reset the win streak and empty the inventory.
#
##############

import os
import json
import random
import sfml as sf
from MainScreen import MainScreen
from MenuScreen import MenuScreen
from SavedGame import SavedGame
from Card import Card


class ManaBurn(object):

    def __init__(self):
        self.cardPool = None
        self.windowWidth = 1100
        self.windowHeight = 850
        self.main()

    def main(self):

        # load big resources first
        cardPath = os.path.join(os.getcwd() ,"res","cardData.json")
        allCardData = None
        with open(cardPath, 'r',encoding="utf-8") as f:
            allCardData = json.load(f)

        # SET UP THE GRAPHICS WINDOW
        window = sf.RenderWindow(sf.VideoMode(1100, 800), 'Mana Burn')
        window.framerate_limit = 60
        window.clear()
        view = sf.View()
        view.reset(sf.Rectangle((0,0),(1100,850)))
        window.view = view
        window.display()

        # figure out the save game situation
        currentSavedGame = SavedGame()
        currentScreen = MainScreen(window, view, currentSavedGame,allCardData)

        # A clock runs and cleans up dead objects periodically
        cleanupClock = sf.Clock()
        
        # THE UPDATE AND GAME LOOP
        while window.is_open:
            for event in window.events:
                if type(event) is sf.CloseEvent:
                    window.close()
                if type(event) is sf.KeyEvent and event.code is sf.Keyboard.ESCAPE:
                    window.close()
                if type(currentScreen) is MainScreen:
                    if type(event) is sf.MouseButtonEvent:
                        currentScreen.checkClicks(window,event)
                    if type(event) is sf.MouseWheelEvent:
                        currentScreen.checkScroll(window,event)
                    
            window.clear()
            currentScreen.update()
            window.display()
            
            if cleanupClock.elapsed_time.seconds >= .5:
                currentScreen.cleanUp()
                cleanupClock.restart()


if __name__ == '__main__':
    manaburn = ManaBurn()
