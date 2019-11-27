# -*- coding: utf-8 -*-
"""
Created on Tue Nov 26 21:53:25 2019

@author: GrigorianPC
"""

import random
import numpy as np
class Card(object):
    def __init__(self,suit='Spade',name='Ace',value=1):
        self.suit = suit
        self.name = name
        self.value= value

class Deck:
    def __init__(self,n=1):
        
        def New_Deck(self):
            Output=[]
            for k in range(0,self.n):
                for i in range(1,5):
                    for j in range(1,14):
                        val=j
                        if j == 1:
                            val = 11
                        elif j == 11 or j==12 or j==13:
                            val = 10
                            
                        New_Card=Card(self.suit_dic[i],self.name_dic[j],val)
                        Output.append(New_Card)
            return Output
        
        self.n = n
        self.name_dic = {1:'Ace',
                2:'Two',
                3:'Three',
                4:'Four',
                5:'Five',
                6:'Six',
                7:'Seven',
                8:'Eight',
                9:'Nine',
                10:'Ten',
                11:'Jack',
                12:'Queen',
                13:'King'}
        self.suit_dic = {1:'Spades',
                2:'Clubs',
                3:'Hearts',
                4:'Diamonds'}
        self.order = New_Deck(self)
    def Top_Card(self):
        return self.order[0]
    
    def Deal(self):
        Output=self.Top_Card()
        self.order.pop(0)
        return Output
    
    def Shuffle(self):
        list=[]
        while len(list)<len(self.order):
            r=random.random()
            if r not in list: list.append(r)
        dictionary=dict(zip(list,self.order))
        list.sort()
        new_list=[]
        for i in range(0,len(self.order)):
            new_list.append(dictionary[list[i]])
        self.order=new_list
        
    def Print_Order(self):
        for i in range(len(self.order)):
            print("Card number ", i+1, " is the ", self.order[i].name, " of ", self.order[i].suit)
            
class Hand:
    def __init__(self):
        self.order=[]
        self.value=0
        self.n=0
    
    def Hit(self,card):
        self.order.append(card)
        self.n=self.n+1
        self.value=self.Evaluate()
    
    def Evaluate(self):
        output=0
        numAces=self.Count_Aces()
        for i in range(0,self.n):
            card=self.order[i]
            output=card.value+output
        while numAces > 0 and output > 21:
            numAces=numAces-1
            output=output-10
        return output
    
    def Has_Ace(self):
        output=False
        for i in range(0,self.n):
            if self.order[i].name=='Ace':
                output=True
                break
        return output
    
    def Count_Aces(self):
        output=0
        for i in range(0,self.n):
            if self.order[i].name=='Ace':
                output=output+1
        return output
    
    def Top_Card(self):
        return self.order[-1]
    
    def Check_BlackJack(self):
        return self.n==2 and self.value==21
    
    def Check_Has_Face_Card(self):
        output=False
        for i in range(0,self.n):
            if self.order[i].value==10:
                output=True
        return output
    
    def Check_Can_Split(self):
        return self.n==2 and self.order[0].value==self.order[1].value

class Hand_Stack:
    def __init__(self):
        self.stack = [Hand()]
        self.size=1
        self.fresh=True
        self.hasSplit=False
    
    def Split(self,i):
        oldHand=self.stack[i]
        newHand1=Hand()
        newHand2=Hand()
        newHand1.Hit(oldHand.order[0])
        newHand2.Hit(oldHand.order[1])
        self.stack[i]=newHand1
        self.stack.append(newHand2)
        self.hasSplit=True
        self.fresh=False
        self.size=self.size+1
    
    def Hit(self,card,i):
        self.stack[i].Hit(card)
        self.fresh=False