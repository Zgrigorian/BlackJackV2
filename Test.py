# -*- coding: utf-8 -*-
"""
Created on Tue Nov 26 21:54:51 2019

@author: GrigorianPC
"""
import PlayingCards as PC
import BlackJack as BJ
#==============================================================================
#Testing Functions associated with the Deck Class
def testGenerateCard():
    tester=PC.Card('Spade','Ace',1)
    boo=tester.suit=='Spade' and tester.name=='Ace' and tester.value==1
    print('Card Generation test result:', boo)
    
def testGenerateDeck():
    n=3
    tester=PC.Deck(n)
    boo=len(tester.order)==52*n
    print('Deck Generation test result:', boo)

def testTopCard():
    tester=PC.Deck(1)
    topCard=tester.Top_Card()
    boo=topCard.suit=='Spades' and topCard.name=='Ace' and topCard.value==1
    print('Deck.TopCard() test result:', boo)

def testDeal():
    tester=PC.Deck(1)
    topCard=tester.Deal()
    boo1=topCard.suit=='Spades' and topCard.name=='Ace' and topCard.value==1
    secCard=tester.Top_Card()
    boo2=secCard.suit=='Spades' and secCard.name=='Two' and secCard.value==2
    print('Deck.Deal() test result:', boo1 and boo2)

def testShuffle():
    PC.random.seed(a=4)
    tester=PC.Deck(1)
    tester.Shuffle()
    topCard=tester.Top_Card()
    boo= topCard.suit=='Diamonds' and topCard.name=='Nine' and topCard.value==9
    print('Deck.Shuffle() test result:', boo)
    
def testPrintOrder():
    tester=PC.Deck(1)
    tester.Print_Order()
    print('Deck.PrintOrder() test result:', True)
#==============================================================================
#Testing Functions associated with the hand class
def testGenerateHand():
    tester=PC.Hand()
    boo=len(tester.order)==0 and tester.n==0 and tester.value==0
    print('Hand Generation test result:', boo)

def testHasAce():
    tester=PC.Hand()
    card1=PC.Card('Spade','King',10)
    card2=PC.Card('Spade','Ace',1)
    tester.order.append(card1)
    tester.n=1
    hasNoAce=not tester.Has_Ace()
    tester.order.append(card2)
    tester.n=2
    hasAce=tester.Has_Ace()
    print('Hand.Has_Ace() test result', hasNoAce and hasAce)

def testCountAces():
    tester=PC.Hand()
    card1=PC.Card('Spade','King',10)
    card2=PC.Card('Spade','Ace',1)
    card3=PC.Card('Diamond','Ace',1)
    tester.order.append(card1)
    tester.n=1
    boo1=tester.Count_Aces()==0
    tester.order.append(card2)
    tester.n=2
    boo2=tester.Count_Aces()==1
    tester.order.append(card3)
    tester.n=3
    boo3=tester.Count_Aces()==2
    print('Hand.Count_Aces() test result:', boo1 and boo2 and boo3)

def testGenericEvaluate():
    tester=PC.Hand()
    card1=PC.Card('Spade','Nine',9)
    card2=PC.Card('Spade','King',10)
    tester.order.append(card1)
    tester.order.append(card2)
    tester.n=2
    boo=tester.Evaluate()==19
    print('Hand.Evaluate() generic low test result:',boo)
    
def testAcesEvaluate():
    tester=PC.Hand()
    card1=PC.Card('Spade','King',10)
    card2=PC.Card('Spade','Ace',11)
    card3=PC.Card('Diamond','Three',3)
    tester.order.append(card1)
    tester.order.append(card2)
    tester.n=2
    boo=tester.Evaluate()==21
    print('Hand.Evaluate() hard ace result:', boo)
    tester.order.append(card3)
    tester.n=3
    boo=tester.Evaluate()==14
    print('Hand.Evaluate() single soft ace result:', boo)
    tester.order.append(card2)
    tester.n=4
    boo=tester.Evaluate()==15
    print('Hand.Evaluate() double soft ace result:',boo)
    tester2=PC.Hand()
    tester2.order.append(card3)
    tester2.order.append(card3)
    tester2.order.append(card2)
    tester2.order.append(card2)
    tester2.n=4
    boo=tester2.Evaluate()==18
    print('Hand.Evaluate() mixed ace result:', boo)    

def testHit():
    PC.random.seed(a=4)
    newDeck=PC.Deck()
    newDeck.Shuffle()
    tester=PC.Hand()
    tester.Hit(newDeck.Deal())
    boo=len(tester.order)==1 and tester.n==1 and tester.value==9
    print('Hand.Hit() test result:', boo)

def testHandTopCard():
    tester=PC.Hand()
    newDeck=PC.Deck()
    tester.Hit(newDeck.Deal())
    tester.Hit(newDeck.Deal())
    tester.Hit(newDeck.Deal())
    topCard=tester.Top_Card()
    boo=topCard.value==3 and topCard.name=='Three' and topCard.suit=='Spades'
    print('Hand.Top_Card() test result:', boo)
    
def testCheckHasFaceCard():
    tester=PC.Hand()
    card1=PC.Card('Diamond','Nine',9)
    card2=PC.Card('Diamond','Jack',10)
    tester.Hit(card1)
    print('Hand.Check_Has_Face_Card() no face card result:', not tester.Check_Has_Face_Card())
    tester.Hit(card2)
    print('Hand.Check_Has_Face_Card() yes face card result:', tester.Check_Has_Face_Card())
    
def testCheckBlackJack():
    tester=PC.Hand()
    tester.n=2
    tester.value=21
    print('Hand.Check_BlackJack() pass result:', tester.Check_BlackJack())
    tester.n=3
    print('Hand.Check_BlackJack() n>2 result:', not tester.Check_BlackJack())
    tester.n=2
    tester.value=22
    print('Hand.Check_BlackJack() val!=21 result:', not tester.Check_BlackJack())
    tester.n=3
    print('Hand.Check_BlackJack() val!=21 and n!=2 result:', not tester.Check_BlackJack())

def testCheckCanSplit():
    tester=PC.Hand()
    card1=PC.Card('Clubs','Six',6)
    card2=PC.Card('Hearts','Seven',7)
    tester.Hit(card1)
    print('Hand.Check_Can_Split() n=1 result:', not tester.Check_Can_Split())
    tester.Hit(card1)
    print('Hand.Check_Can_Split() n=2, same result:', tester.Check_Can_Split())
    tester.Hit(card1)
    print('Hand.Check_Can_Split() n=3 same result:', not tester.Check_Can_Split())
    tester2=PC.Hand()
    tester2.Hit(card1)
    tester2.Hit(card2)
    print('Hand.Check_Can_Split() n=2, diff result:', not tester2.Check_Can_Split())
    tester2.Hit(card1)
    print('Hand.Check_Can_Split() n=3, 1 pair result:',not tester2.Check_Can_Split())
#==============================================================================
#Testing handStack Functions
def testGenerateHandStack():
    tester=PC.Hand_Stack()
    boo=tester.size==1 and tester.fresh== True and tester.hasSplit==False
    print('Generate Hand Stack result:', boo)
    
def testHandStackHit():
    tester=PC.Hand_Stack()
    card=PC.Card('Spade','Eight',8)
    tester.Hit(card,0)
    hand1=tester.stack[0]
    boo=hand1.n==1 and tester.fresh==False
    print('Hand_Stack.Hit() result:',boo)

def testHandStackSplit():
    tester=PC.Hand_Stack()
    card1=PC.Card('Spade','Eight',8)
    card2=PC.Card('Diamond','Eight',8)
    tester.Hit(card1,0)
    tester.Hit(card2,0)
    tester.Split(0)
    hand1=tester.stack[0]
    hand2=tester.stack[1]
    boo1=hand1.n==1 and hand1.order[0].suit=='Spade'
    boo2=hand2.n==1 and hand2.order[0].suit=='Diamond'
    boo3=tester.fresh==False and tester.hasSplit==True
    print('Hand_Stack.Split() result:',boo1 and boo2 and boo3)
    
    
#==============================================================================
#Testing Blackjack Functions
def testNewHand():
    deck=PC.Deck();
    player,dealer=BJ.Deal_Hand(deck)
    boo1=player.n==2 and player.value==14
    boo2=dealer.n==2 and dealer.value==6
    print('New_Hand(deck) result:', boo1 and boo2)
#==============================================================================
testGenerateCard()
testGenerateDeck()
testTopCard()
testDeal()
testShuffle()
#testPrintOrder()
testHasAce()
testCountAces()
testGenericEvaluate()
testAcesEvaluate()
testHit()
testHandTopCard()
testCheckHasFaceCard()
testCheckBlackJack()
testCheckCanSplit()
testNewHand()
testGenerateHandStack()
testHandStackHit()
testHandStackSplit()