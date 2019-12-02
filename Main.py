# -*- coding: utf-8 -*-
"""
Created on Tue Nov 26 21:53:00 2019

@author: GrigorianPC
"""
import BlackJack as BJ
n=1
Winnings=0
Bet=10
gameNum=2
#==============================================================================
#First Game
#Winnings=Winnings-Bet
#deck,player,dealer=BJ.Initialize_Game(n)
#player.first[0]=True
#BJ.Ask_Insurance(dealer,player,Bet)
#BJ.Check_Dealer_BlackJack(dealer,player)
#Winnings=Winnings+BJ.Resolve_Prehit(dealer,player,Bet)
#i=0
#print('---------Beginning Phase Complete-------')
#BJ.Resolve_Player_Hand(player,deck,Winnings,Bet)
#print('-------Resolving Dealer Hand------------')
#BJ.Resolve_Dealer(dealer,player,deck)
#print('-------Evaluating Results---------------')
#BJ.Evaluate_Stay(player,dealer)
#Winnings=BJ.Pay_Out(player,dealer,Bet)+Winnings
#print('Current Winnings:',Winnings)
#==============================================================================
#Subsequent Games
deck=BJ.New_Deck(n)
for i in range(0,gameNum):
    Winnings=Winnings-Bet
    if deck.n<26*n:
        deck=BJ.New_Deck(n)
    player,dealer=BJ.Deal_Hand(deck)
    player.Print_Player()
    dealer.Print_Dealer_Top()
    player.first[0]=True
    BJ.Ask_Insurance(dealer,player,Bet)
    BJ.Check_Dealer_BlackJack(dealer,player)
    Winnings=Winnings+BJ.Resolve_Prehit(dealer,player,Bet)
    i=0
    print('---------Beginning Phase Complete-------')
    BJ.Resolve_Player_Hand(player,deck,Winnings,Bet)
    print('-------Resolving Dealer Hand------------')
    BJ.Resolve_Dealer(dealer,player,deck)
    print('-------Evaluating Results---------------')
    BJ.Evaluate_Stay(player,dealer)
    Winnings=BJ.Pay_Out(player,dealer,Bet)+Winnings
    print('Current Winnings:', Winnings)