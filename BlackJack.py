# -*- coding: utf-8 -*-
"""
Created on Tue Nov 26 23:34:12 2019

@author: GrigorianPC
"""

from PlayingCards import Card
from PlayingCards import Deck 
from PlayingCards import Hand 

def Deal_Hand(deck):
    player=Hand()
    dealer=Hand()
    player.Hit(deck.Deal())
    dealer.Hit(deck.Deal())
    player.Hit(deck.Deal())
    dealer.Hit(deck.Deal())
    return player,dealer

