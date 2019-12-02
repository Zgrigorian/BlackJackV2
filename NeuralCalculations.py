# -*- coding: utf-8 -*-
"""
Created on Thu Nov 28 23:23:12 2019

@author: Zach
"""
import numpy as np
import random as rand

def Sigma(x):
    return np.exp(x)/(np.exp(x)+1)

def Seed_Matrix(rows,cols):
    mat=np.zeros((rows,cols),dtype=float)
    for i in range(0,rows):
        for j in range(0,cols):
            mat[i,j]=2*(rand.random()-.5)
    return mat

def Generate_Matrix_List(hiddenLayers,hiddenNodes,inputs,outputs):
    matrixList=[]
    if hiddenLayers > 0:
        matrixList.append(Seed_Matrix(hiddenNodes,inputs))
        for i in range(0,hiddenLayers):
            matrixList.append(Seed_Matrix(hiddenNodes,hiddenNodes))
        matrixList.append(Seed_Matrix(outputs,hiddenNodes))
    else:
        matrixList.append(Seed_Matrix(outputs,inputs))
    return matrixList
    
def Evaluate_Neural_Net(input_vec,matrixList):
    output=input_vec
    for i in range(0,len(matrixList)):
        mat=matrixList[i]
        output=mat.dot(output)
        output=Sigma(output)
        if i < len(matrixList)-1:
            output=np.around(output)
    output=Transform_Output(output)
    return output

def Permute_Matrix(mu,matrix):
    rows=len(matrix)
    cols=len(matrix.T)
    output=np.zeros((rows,cols),dtype=float)
    for i in range(0,rows):
        for j in range(0,cols):
            output[i,j]=matrix[i,j]+np.random.normal(0,mu,1)
    return output

def Permute_Matrix_List(mu,matrixList):
    n=len(matrixList)
    output=[]
    for i in range(0,n):
        mat=matrixList[i]
        output.append(Permute_Matrix(mu,mat))
    return output

def Generate_Seed(seeds,hiddenLayers,hiddenNodes,inputs,outputs):
    masterList=[]
    for i in range(0,seeds):
        masterList.append(Generate_Matrix_List(hiddenLayers,hiddenNodes,inputs,outputs))
    return masterList

def Seed_From_Best(seeds,mu,bestList):
    masterList=[]
    for i in range(0,seeds):
        masterList.append(Permute_Matrix_List(mu,bestList))
    return masterList

def Transform_Output(output):
    if output[1] > .75:
        output[1]=1
    else:
        output[1]=0
    output=np.around(output)
    return output

#inlet=np.ones((4,1),dtype=float)
#hiddenLayers=4
#hiddenNodes=10
#inputs=len(inlet)
#outputs=3
#matList=Generate_Matrix_List(hiddenLayers,hiddenNodes,inputs,outputs)
#outlet=Evaluate_Neural_Net(inlet,matList)
#Test=Generate_Seed(10,4,10,4,3)