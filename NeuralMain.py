# -*- coding: utf-8 -*-
"""
Created on Fri Nov 29 09:44:37 2019

@author: Zach
"""

# -*- coding: utf-8 -*-
"""
Created on Tue Nov 26 21:53:00 2019

@author: GrigorianPC
"""
from NeuralBlackJack import Play_BlackJack
from Test_Harness import Form_Decision_Matrix
import NeuralCalculations as NC
import matplotlib.pyplot as plt
import random as rand

def Train_Network(n,mu,hiddenLayers,hiddenNodes,inputs,outputs,seeds,
                  gameNum,iterations,reseed,show,masterList,randomlySurvive):
    if reseed:
        
        masterList=NC.Generate_Seed(seeds,hiddenLayers,hiddenNodes,inputs,outputs)
    maxList=[]
    minList=[]
    avgList=[]
    iterList=[]
    for i in range(0,iterations):
        iterList.append(i)
        print('-----------Beginning Iteration',i,'-----------')
        #==============================================================================
        Winnings=[]
        for j in range(0,seeds):
            matrixList=masterList[j]
            Winnings.append(Play_BlackJack(n,matrixList,gameNum,show))
        #==============================================================================
        maxProfit=max(Winnings)
        minProfit=min(Winnings)
        avgProfit=sum(Winnings)/len(Winnings)
        maxList.append(maxProfit)
        minList.append(minProfit)
        avgList.append(avgProfit)
        print('Max Iteration Winnings:',maxProfit)
        print('Min Iteration Winnings:',minProfit)
        print('Avg Iteration Winnings:',avgProfit)
        print(len(masterList))
        topIndex=sorted(range(len(Winnings)), key=lambda i: Winnings[i])[-round(survivalRate):]
        for m in range(0,randomlySurvive):
            topIndex.append(rand.randint(0,seeds-1))
        masterListNew=[]
        for k in range(0,len(topIndex)):
            masterListNew.extend(NC.Seed_From_Best(2,mu,masterList[topIndex[k]]))
        masterList=masterListNew
    return masterList,maxList,minList,avgList,iterList,topIndex

n=2
mu=0.01
hiddenLayers=1
hiddenNodes=8
inputs = 4
outputs = 4
seeds=100
gameNum=100
iterations=1000
reseed=False
show=False
survivalRate=10
randomlySurvive=40
if reseed:
    masterList=[]
masterList,maxList,minList,avgList,iterList,topIndex=Train_Network(
                                                          n,mu,hiddenLayers,
                                                          hiddenNodes,inputs,
                                                          outputs,seeds,
                                                          gameNum,iterations,
                                                          reseed,
                                                          show,masterList,
                                                          randomlySurvive)
actionFrameList=[]
insuranceFrameList=[]
for i in range(0,len(masterList)):
    actionFrame,insuranceFrame=Form_Decision_Matrix(masterList,i)
    actionFrameList.append(actionFrame)
    insuranceFrameList.append(insuranceFrame)
actionFrame.to_excel("decisionMatrix.xlsx")
insuranceFrame.to_excel("insuranceMatrix.xlsx")