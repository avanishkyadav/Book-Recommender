import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os

def load_dataset(split=0.9):
    #rating contains books which are not rated by any user so we are going to
    #eliminate them and create new data files which contains only books rated by
    #atleast one user. We give  a tempId to rated book in list books
    df=pd.read_csv("data/ratings.csv")
    Y=[]
    for index,row in df.iterrows():
        Y.append((row['user_id']-1,row['book_id']-1,row['rating']))
        print(index)
    m=len(Y)
    train=Y[:int(split*m)]
    test=Y[int(split*m):]
    Y=np.array(df.pivot(index='user_id',columns='book_id',values='rating').fillna(0))
    numU,numB=Y.shape
    print("ended")
    return train,test,numU,numB




def train_model(numUser,numBook,Y,test_Y,latent_factors=20,numIterarions=100,learning_rate=0.001,Lambda=0.01):
    #initialize the parameters
    userMatrix,bookMatrix,userBias,bookBias=initialize_parameters(numUser,numBook,latent_factors)
    m=len(Y)
    epochLoss=[]
    for k in range(numIterarions):
        cost=0
        np.random.shuffle(Y)
        for i,j,r in Y:
            prediction=predict(userMatrix[i,:],bookMatrix[j,:],userBias[i],bookBias[j])
            error=pow(prediction-r,2)
            cost+=((error+ Lambda*(np.dot(userMatrix[i,:],userMatrix[i,:].T)+np.dot(bookMatrix[j,:],bookMatrix[j,:].T)))/m)

            #update the parameters
            userBias[i]-=learning_rate*(error)
            bookBias[j]-=learning_rate*(error)
            userMatrix[i,:]-=learning_rate*( error*bookMatrix[j,:]  +  Lambda*userMatrix[i,:])
            bookMatrix[j,:]-=learning_rate*( error*userMatrix[i,:]  +  Lambda*bookMatrix[j,:])
        if (m+1)%10==0:
            print("Cost after "+str(m+1)+" Iteration is: "+str(totalError))
        epochLoss.append(cost)

    print("Loss on train data is: "+str(calculate_loss(userMatrix,bookMatrix,userBias,bookBias,Y)))
    print("Loss on test data is: "+str(calculate_loss(userMatrix,bookMatrix,userBias,bookBias,test_Y)))
    return userMatrix,bookMatrix,userBias,bookBias,epochLoss

def calculate_loss(userMat,bookMat,userBias,bookBias,y):
    loss=0
    m=len(y)
    for i,j,r in y:
        prediction=predict(userMat[i,:],bookMat[j,:],userBias[i],bookBias[j])
        loss+=pow(prediction-r,2)/m
    return loss

def predict(user,book,uBias,bBias):
    prediction=np.dot(user,book.T)+uBias+bBias
    return prediction


def initialize_parameters(numUser,numBook,latent_factors):
    userMat=np.random.rand(numUser,latent_factors)
    bookMat=np.random.rand(numBook,latent_factors)
    userBias=np.zeros((numUser))
    bookBias=np.zeros((numBook))
    return userMat,bookMat,userBias,bookBias
