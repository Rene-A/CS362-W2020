# -*- coding: utf-8 -*-
"""
Created on 1/18/20

@author: Rene Arana
"""

import testUtility
import Dominion

#Get player names
player_names = testUtility.getPlayerNames()

#number of curses and victory cards
nV = testUtility.getNumberOfVictoryCards(player_names)
nC = testUtility.getNumberOfCurseCards(player_names)

# Introduce a bug that allows more curse cards than should be allowed
nC = 100

#Define box
box = testUtility.getBoxes(nV)

supply_order = testUtility.getSupplyOrder()

#Pick 10 random cards from box to be in the supply, then add the cards that are included in every game.
supply = testUtility.getSupplyCards(box, player_names, nV, nC)

#initialize the trash
trash = testUtility.initializeTrash()

#Costruct the Player objects
players = testUtility.getPlayerObjects(player_names)

#Play the game
turn  = 0
while not Dominion.gameover(supply):
    turn += 1    
    print("\r")    
    for value in supply_order:
        print (value)
        for stack in supply_order[value]:
            if stack in supply:
                print (stack, len(supply[stack]))
    print("\r")
    for player in players:
        print (player.name,player.calcpoints())
    print ("\rStart of turn " + str(turn))    
    for player in players:
        if not Dominion.gameover(supply):
            print("\r")
            player.turn(players,supply,trash)
            

#Final score
dcs=Dominion.cardsummaries(players)
vp=dcs.loc['VICTORY POINTS']
vpmax=vp.max()
winners=[]
for i in vp.index:
    if vp.loc[i]==vpmax:
        winners.append(i)
if len(winners)>1:
    winstring= ' and '.join(winners) + ' win!'
else:
    winstring = ' '.join([winners[0],'wins!'])

print("\nGAME OVER!!!\n"+winstring+"\n")
print(dcs)