# -*- coding: utf-8 -*-
"""
Created on Sat Nov 30 16:22:10 2019

@author: Zach
"""

import PlayingCards as PC
import NeuralBlackJack as BJ
import pandas as pd
import random as rand
def Generate_Player_Combinations():
    suit='Spades'
    nameDic = { 2:'Two',
                3:'Three',
                4:'Four',
                5:'Five',
                6:'Six',
                7:'Seven',
                8:'Eight',
                9:'Nine',
                10:'Ten',
                11:'Ace'}
    output=[]
    for i in range(2,12):
        card1=PC.Card(suit,nameDic[i],i)
        for j in range(i,12):
            card2=PC.Card(suit,nameDic[j],j)
            tup=card1,card2
            output.append(tup)
    return output

def Generate_Dealer_Combinations():
    suit='Spades'
    nameDic = { 2:'Two',
                3:'Three',
                4:'Four',
                5:'Five',
                6:'Six',
                7:'Seven',
                8:'Eight',
                9:'Nine',
                10:'Ten',
                11:'Ace'}
    output=[]
    for i in range(2,12):
        card=PC.Card(suit,nameDic[i],i)
        output.append(card)
    return output

def Form_Player_Hand(tup):
    player=PC.Hand_Stack()
    card1,card2=tup
    player.Hit(card1)
    player.Hit(card2)
    return player

def Form_Dealer_Hand(card):
    dealer=PC.Hand()
    dummy=PC.Card('Spade','Two',2)
    dealer.Hit(dummy)
    dealer.Hit(card)
    return dealer

def Test_Response(player,dealer,matrixList):
    neuron=BJ.Form_Neuron(dealer,player,0,matrixList)
    if neuron[0]:
        Insur='Take insurance'
    else:
        Insur='Do not take insurance'
    if neuron[1]:
        action='Stay'
    elif neuron[2] and player.fresh:
        action='Double'
    elif neuron[3] and player.Check_Can_Split():
        action='Split'
    else:
        action='Hit'
    return Insur,action

def Form_Combination_Lists(playerComb):
    output=[]
    for i in range(0,55):
        player=Form_Player_Hand(playerComb[i])
        playerHand=player.stack[0]
        card1=str(playerHand.order[0].value)
        card2=str(playerHand.order[1].value)
        if card1 == '11':
            card1='A'
        if card2 =='11':
            card2='A'
        output.append(card1+','+card2)
    return output

def Form_Dealer_Combination_List(dealerComb):
    dealerList=[]
    for i in range(0,10):
        dealerList.append(dealerComb[i].name)
    return dealerList

def Has_Behavior(sample,masterAction):
    boo=False
    for i in range(len(masterAction)):
        for j in range(len(masterAction[i])):
            if masterAction[i][j] != 'Stay':
                boo=True
                break
    if boo:
        print(sample, 'has interesting behavior')
    else:
        print(sample, 'has no interesting behavior')
        
def Form_Decision_Matrix(masterList,index):
    bestList=masterList[index]
    masterInsurance=[]
    masterAction=[]
    playerComb=Generate_Player_Combinations()
    playerList=Form_Combination_Lists(playerComb)
    dealerComb=Generate_Dealer_Combinations()
    dealerList=Form_Dealer_Combination_List(dealerComb)
    for j in range(0,10):
        insuranceList=[]
        actionList=[]
        for i in range(0,55):
            player=Form_Player_Hand(playerComb[i])
            dealer=Form_Dealer_Hand(dealerComb[9])
            matrixList=bestList
            insur,action=Test_Response(player,dealer,matrixList)
            insuranceList.append(insur)
            actionList.append(action)
        masterInsurance.append(insuranceList)
        masterAction.append(actionList)
    Has_Behavior(index,masterAction)
    actionFrame=pd.DataFrame(data=masterAction,index=dealerList,columns=playerList)
    insuranceFrame=pd.DataFrame(data=masterInsurance,index=dealerList,columns=playerList)
    return actionFrame.T,insuranceFrame.T