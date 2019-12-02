# -*- coding: utf-8 -*-
"""
Created on Thu Nov 28 22:56:53 2019

@author: Zach
"""

# -*- coding: utf-8 -*-
"""
Created on Tue Nov 26 23:34:12 2019

@author: GrigorianPC
"""

from PlayingCards import Card
from PlayingCards import Deck 
from PlayingCards import Hand 
from PlayingCards import Hand_Stack
import numpy as np
import NeuralCalculations as NC

def Deal_Hand(deck):
    player=Hand_Stack()
    dealer=Hand()
    player.Hit(deck.Deal(),0)
    dealer.Hit(deck.Deal())
    player.Hit(deck.Deal(),0)
    dealer.Hit(deck.Deal())
    return player,dealer

def New_Deck(n):
    newDeck=Deck(n)
    newDeck.Shuffle()
    return newDeck

def Initialize_Game(n):
    deck=New_Deck(n)
    player,dealer=Deal_Hand(deck)
    #player.Print_Player(0)
    #dealer.Print_Dealer_Top()
    return deck,player,dealer

def Ask_Insurance(dealer,player,Bet,matrixList,show):
    dealerTop=dealer.Top_Card()
    output=0
    neuron=Form_Neuron(dealer,player,0,matrixList)
    if dealerTop.value == 11:
        output=neuron[0]
        if show:
            print('Neural Net takes insurance',neuron[0])
        player.insurance=output
        output=-Bet/2
    else:
        if neuron[0]:
            output=-30
    return output
    
def Check_Dealer_BlackJack(dealer,player,show):
    dealerBlack = dealer.Check_BlackJack()
    playerBlack = player.Check_BlackJack()
    if dealerBlack and playerBlack:
        player.Update_Status('Push')
        if show:
            dealer.Print_Dealer()
    elif dealerBlack:
        player.Update_Status('Lost')
        if show:
            dealer.Print_Dealer()
    elif playerBlack:
        player.Update_Status('Blackjack')
    else:
        player.Update_Status('Live')

def Resolve_Prehit(dealer,player,Bet):
    profit=0
    if player.insurance == True and dealer.Check_BlackJack()==True:
        profit=Bet
    return profit   
        
def Ask_To_Hit(player,i,deck):
    if player.status[i]=='Live':
        card=deck.Deal()
        player.Hit(card,i)
        #print('You hit the', card.name,'of',card.suit)
        #player.Print_Player(i)

def Update_Hand_Condition(player,i):
    hand=player.stack[i]
    if hand.Check_BlackJack():
        player.status[i]='Blackjack'
    elif hand.value>21:
        player.status[i]='Lost'
    else:
        player.status[i]='Live'

def Ask_To_Stay(player,i,neuron,show):
    if player.status[i]=='Live':
        stayTrue=neuron[1]
        if show:
            print('Neural Net Stay',neuron[1])
        if stayTrue:
            player.Update_Status('Stay',i)

def Ask_To_Split(player,i,Bet,neuron):
    canSplit=player.Check_Can_Split(i)
    output=0
    if canSplit and player.status[i]=='Live':
        doesSplit=neuron[3]
        #print('Neural Net Split',neuron[3])
        if doesSplit:
            player.Split(i)
            #player.Print_Player(i)
            player.Update_Status('Split',i)
            output=-Bet
    return output
    

def Ask_To_Double(player,i,deck,Bet,neuron,show):
    output=0
    if player.first[i] and player.status[i]=='Live':
        doesDouble=neuron[2]
        if show:
            print('Neural Net Double', neuron[2])
        if doesDouble:
            output=-Bet
            player.Hit(deck.Deal(),i)
            if player.stack[i].value < 22:
                player.Update_Status('Stay',i)
            else:
                player.Update_Status('Lost',i)
            if show:
                player.Print_Player(i)
            player.doubled[i]=True
    return output

def Ask_To_Surrender(player,i,Bet):
    doesSurrender=input('Would you like to surrender? (y/n)')
    output=0
    if doesSurrender=='y':
        output=Bet/2
        player.Update_Status('Surrender')
    return output

def Resolve_Dealer(dealer,player,deck,show):
    if show:
        dealer.Print_Dealer()
    allBlack=All_BlackJack(player)
    allLost=All_Lost(player)
    while dealer.value<17 and not allBlack and not allLost:
        card=deck.Deal()
        dealer.Hit(card)
        if show:
            print('The Dealer hits the',card.name,'of',card.suit)
            dealer.Print_Dealer()
    if dealer.value>21:
        dealer.value=-1

def All_BlackJack(player):
    output=True
    for i in range(0,player.size):
        output=output and player.status[i]=='Blackjack'
    return output

def All_Lost(player):
    output=True
    for i in range(0,player.size):
        output=output and player.status[i]=='Lost'
    return output

def Evaluate_Stay(player,dealer):
    for i in range(0,player.size):
        if player.status[i]=='Stay':
            if player.stack[i].value > dealer.value:
                player.status[i]='Win'
            elif player.stack[i].value == dealer.value:
                player.status[i]='Push'
            else:
                player.status[i]='Lost'

def Pay_Out(player,dealer,Bet,show):
    output=0
    for i in range(0,player.size):
        if player.status[i]=='Push':
            if player.doubled[i]:
                output=2*Bet+output
            else:
                output=Bet+output
            if show:
                print('Hand',i,'is a push, no net winnings')
        elif player.status[i]=='Blackjack':
            output=Bet*2.5+output
            if show:
                print('You have Blackjack on hand',i,'win 1.5 payout')
        elif player.status[i]=='Lost':
            output=0+output
            if show:
                print('You lost hand',i)
        elif player.status[i]=='Win':
            if player.doubled[i]:
                output=Bet*4+output
                if show:
                    print('Hand',i,'won its double down')
            else:
                output=Bet*2+output
                if show:
                    print('Hand',i,'won, even payout')
        else:
            print(player.status[i])
    return output

def Resolve_Player_Hand(dealer,player,deck,Winnings,Bet,matrixList,show):
    i=0
    while i < player.size:
        while player.status[i]=='Live':
            neuron=Form_Neuron(dealer,player,i,matrixList)
            if show:
                player.Print_Player(i)
            Ask_To_Stay(player,i,neuron,show)
            Winnings=Winnings+Ask_To_Double(player,i,deck,Bet,neuron,show)
            Winnings=Winnings+Ask_To_Split(player,i,Bet,neuron)
            Ask_To_Hit(player,i,deck)
            if player.status[i]=='Live' or player.status[i]=='Split':
                Update_Hand_Condition(player,i)
        i=i+1
    return Winnings

def Form_Neuron(dealer,player,i,matrixList):
    inputVec=np.zeros((4,1),dtype=float)
    inputVec[0]=player.Has_Ace(i)
    inputVec[1]=player.Check_Can_Split(i)
    inputVec[2]=player.stack[i].value
    inputVec[3]=dealer.order[1].value
    neuron=NC.Evaluate_Neural_Net(inputVec,matrixList)
    return neuron

def Play_BlackJack(n,matrixList,gameNum,show):
    Winnings=0
    Bet=10
    deck=New_Deck(n)
    for i in range(0,gameNum):
        Winnings=Winnings-Bet
        if len(deck.order)<26*n:
            deck=New_Deck(n)
        player,dealer=Deal_Hand(deck)
        if show: print(player.doubled)
        if show:
            print(player.status)
            player.Print_Player()
            dealer.Print_Dealer_Top()
        player.first[0]=True
        Ask_Insurance(dealer,player,Bet,matrixList,show)
        Check_Dealer_BlackJack(dealer,player,show)
        Winnings=Winnings+Resolve_Prehit(dealer,player,Bet)
        if show:
            print('---------Beginning Phase Complete-------')
        Winnings=Resolve_Player_Hand(dealer,player,deck,Winnings,Bet,matrixList,show) #Edited this
        if show:
            print('Winnings after Player Hand',Winnings)
        if show:
            print('-------Resolving Dealer Hand------------')
            print(Winnings)
        Resolve_Dealer(dealer,player,deck,show)
        if show:
            print('-------Evaluating Results---------------')
        Evaluate_Stay(player,dealer)
        if show:
            print(player.doubled)
            print(player.status)
        Winnings=Pay_Out(player,dealer,Bet,show)+Winnings
        if show:
            print('Current Winnings:', Winnings)
    return Winnings

