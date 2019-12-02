# -*- coding: utf-8 -*-
"""
Created on Tue Nov 26 23:34:12 2019

@author: GrigorianPC
"""

from PlayingCards import Card
from PlayingCards import Deck 
from PlayingCards import Hand 
from PlayingCards import Hand_Stack

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
#    deck.order[0]=Card('Spades','Ace',11)
#    deck.order[1]=Card('Spades','Diamond',10)
#    deck.order[2]=Card('Spades','Queen',10)
#    deck.order[3]=Card('Spades','King',10)
#    deck.order[4]=Card('Spades','King',10)
#    deck.order[5]=Card('Spades','Seven',7)
    player,dealer=Deal_Hand(deck)
    player.Print_Player(0)
    dealer.Print_Dealer_Top()
    return deck,player,dealer

def Ask_Insurance(dealer,player,Bet):
    dealerTop=dealer.Top_Card()
    output=0
    if dealerTop.value == 11:
        output=input('Would you like insurance (y/n)? ')
        player.insurance=output=='y'
        output=-Bet/2
    return output
    
def Check_Dealer_BlackJack(dealer,player):
    dealerBlack = dealer.Check_BlackJack()
    playerBlack = player.Check_BlackJack()
    if dealerBlack and playerBlack:
        player.Update_Status('Push')
        dealer.Print_Dealer()
    elif dealerBlack:
        player.Update_Status('Lost')
        dealer.Print_Dealer()
    elif playerBlack:
        player.Update_Status('Blackjack')
    else:
        player.Update_Status('Live')

def Resolve_Prehit(dealer,player,Bet):
    profit=0
    if player.insurance == True and dealer.Check_BlackJack()==True:
        profit=Bet
#    if player.status[0]=='Blackjack':
#        profit=Bet*1.5+profit
    return profit   
        
def Ask_To_Hit(player,i,deck):
    if player.status[i]=='Live':
#        hitTrue=input('Would you like to hit? (y/n) ')
#        if hitTrue=='y':
        card=deck.Deal()
        player.Hit(card,i)
        print('You hit the', card.name,'of',card.suit)
        player.Print_Player(i)

def Update_Hand_Condition(player,i):
    hand=player.stack[i]
    if hand.Check_BlackJack():
        player.status[i]='Blackjack'
    elif hand.value>21:
        player.status[i]='Lost'
    else:
        player.status[i]='Live'

def Ask_To_Stay(player,i):
    if player.status[i]=='Live':
        stayTrue=input('Would you like to stay? (y/n)')
        if stayTrue=='y':
            player.Update_Status('Stay',i)

def Ask_To_Split(player,i,Bet):
    canSplit=player.Check_Can_Split(i)
    output=0
    if canSplit and player.status[i]=='Live':
        doesSplit=input('Would you like to split? (y/n)')
        if doesSplit=='y':
            player.Split(i)
            player.Print_Player(i)
            player.Update_Status('Split',i)
            output=-Bet
    return output
    

def Ask_To_Double(player,i,deck,Bet):
    output=0
    if player.first[i] and player.status[i]=='Live':
        doesDouble=input('Would you like to double down? (y/n)')
        if doesDouble=='y':
            output=-Bet
            player.Hit(deck.Deal(),i)
            player.Update_Status('Stay',i)
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

def Resolve_Dealer(dealer,player,deck):
    dealer.Print_Dealer()
    allBlack=All_BlackJack(player)
    allLost=All_Lost(player)
    while dealer.value<17 and not allBlack and not allLost:
        card=deck.Deal()
        print('The Dealer hits the',card.name,'of',card.suit)
        dealer.Hit(deck.Deal())
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
        print('made it here')
        if player.status[i]=='Stay':
            if player.stack[i].value > dealer.value:
                player.status[i]='Win'
            elif player.stack[i].value == dealer.value:
                player.status[i]='Push'
            else:
                player.status[i]='Lost'

def Pay_Out(player,dealer,Bet):
    output=0
    for i in range(0,player.size):
        if player.status[i]=='Push':
            if player.doubled[i]:
                output=2*Bet+output
            else:
                output=Bet+output
            print('Hand',i,'is a push, no net winnings')
        elif player.status[i]=='Blackjack':
            output=Bet*2.5+output
            print('You have Blackjack on hand',i,'win 1.5 payout')
        elif player.status[i]=='Lost':
            output=0+output
            print('You lost hand',i)
        elif player.status[i]=='Win':
            if player.doubled[i]:
                output=Bet*4+output
                print('Hand',i,'won its double down')
            else:
                output=Bet*2+output
                print('Hand',i,'won, even payout')
        else:
            print(player.status[i])
    return output
        
def Resolve_Player_Hand(player,deck,Winnings,Bet):
    i=0
    while i < player.size:
        while player.status[i]=='Live':
            player.Print_Player(i)
            Ask_To_Stay(player,i)
            Winnings=Winnings+Ask_To_Double(player,i,deck,Bet)
            Winnings=Winnings+Ask_To_Split(player,i,Bet)
            Ask_To_Hit(player,i,deck)
            if player.status[i]=='Live' or player.status[i]=='Split':
                Update_Hand_Condition(player,i)
        i=i+1
    