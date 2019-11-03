#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Mar  3 11:17:45 2019

@author: kaleem
"""

'''
SIH 2019
Team Recursion:
    Kaleem Ahmad
    Himanshu Singh
    Abhinav Bajpai
    Debrup Datta
    Dakshita Chaturvedi
    Muskan Agrawal
'''

import pandas as pd
import csv
from collections import defaultdict

#nt_data.to_csv("nodetable.csv",index=False)
data = pd.read_csv("new.csv", encoding ="ISO-8859-1")
#data.head()
len(data['Source'].unique())
len(data['Target'].unique())
df = pd.DataFrame(data)
df_1 = pd.get_dummies(df.Target)
df_s = df['Source']
df_pivoted = pd.concat([df_s,df_1], axis=1)
df_pivoted.drop_duplicates(keep='first',inplace=True)
#df_pivoted[:5]

cols = df_pivoted.columns
df_pivoted = df_pivoted.groupby('Source').sum()
df_pivoted = df_pivoted.reset_index()
#df_pivoted[:5]
flag =0
li = ['failure heart','lung cancer','HIV', 'chicken pox','lung cancer','hepatitis B','HIV','dengu','malaria','pneumonia']
#df_pivoted.to_csv("df_pivoted_again.csv")
x = df_pivoted[cols]
y = df_pivoted['Source']

import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split

index_to_symptom = {}
for index, row in x.iterrows():
    #print(row)
    index_to_symptom [index] = row[0]
    
symptom_to_index ={}
for index, row in x.iterrows():
    #print(row)
    symptom_to_index [row[0]] =index 

def ToList(y):
    ytmp = []
    for src in y.tolist():
        ytmp.append(symptom_to_index[src])
    return ytmp

x = x.drop('Source', 1)
y=ToList(y)

from sklearn.tree import DecisionTreeClassifier

from sklearn import tree 
from sklearn.tree import export_graphviz
cols = cols[1:]

X_train, X_test, Y_train, Y_test = train_test_split(x, y, test_size=0.3, random_state=42)
'''
test_data = pd.read_csv("/home/kaleem/Desktop/login/Manual-Data/Testing.csv")
'''


#print("============================APPLYING RANDOM FOREST CLASSIFIER==================================")
from sklearn.ensemble import RandomForestClassifier
classifier = RandomForestClassifier(n_estimators = 10, criterion = 'entropy', random_state = 0)
classifier.fit(X_train,Y_train)
random_pred= classifier.predict(X_test)
'''
from sklearn.svm import SVC
classifier = SVC(kernel = 'linear', random_state = 0)
classifier.fit(X_train, Y_train)
ho=classifier.predict(X_test)
'''
def PredictDisease(XX):
    random_pred = classifier.predict(XX)
    return random_pred


'''
==============================DialogFlow Part===================================
'''
SYMPTOMS = list(X_test.columns.values)
import os
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'sih-app-739b1db0be0c.json'

import dialogflow
from google.api_core.exceptions import InvalidArgument
DIALOGFLOW_PROJECT_ID = 'sih-app-2237'
DIALOGFLOW_LANGUAGE_CODE = 'en'
GOOGLE_APPLICATION_CREDENTIALS = 'sih-app-739b1db0be0c.json'
SESSION_ID = 0
MLPart = 'please provide me symptoms of your disease so that I can help you.'

def DiseasePrediction(text_to_be_analyzed):
    
    ParseToFile = MLPart
    '''
    Convert ParseToFile into Audio
    '''
    
    #text_to_be_analyzed = input()

    session_client = dialogflow.SessionsClient()
    session = session_client.session_path(DIALOGFLOW_PROJECT_ID, SESSION_ID)

    text_input = dialogflow.types.TextInput(text=text_to_be_analyzed, language_code=DIALOGFLOW_LANGUAGE_CODE)
    query_input = dialogflow.types.QueryInput(text=text_input)
    try:
        response = session_client.detect_intent(session=session, query_input=query_input)
    except InvalidArgument:
            raise

    QueryText = response.query_result.query_text
    
    X = []
    for i in range(len(SYMPTOMS)):
        X.append(0)

    symptoms = list(QueryText.split(" "))
    for i, symptom in enumerate(SYMPTOMS):
        if symptom in symptoms:
            X[i] = 1
            
    XY = pd.DataFrame(np.array(X).reshape(1, 154), columns = SYMPTOMS)
    #print(XY)
    Disease = PredictDisease(XY)        
    '''
    Predict Diseases

    Query Food from Table
    '''
    return Disease


def ApplyDialogFlow(text_to_be_analyzed):
    global flag

    session_client = dialogflow.SessionsClient()
    session = session_client.session_path(DIALOGFLOW_PROJECT_ID, SESSION_ID)

    text_input = dialogflow.types.TextInput(text=text_to_be_analyzed, language_code=DIALOGFLOW_LANGUAGE_CODE)
    query_input = dialogflow.types.QueryInput(text=text_input)
    try:
        response = session_client.detect_intent(session=session, query_input=query_input)
    except InvalidArgument:
            raise

    QueryText = response.query_result.query_text
    FulfillmentText = response.query_result.fulfillment_text
    
    if FulfillmentText == MLPart:
          flag = 1 
          return(MLPart)

          #FulfillmentText = DiseasePrediction(text_to_be_analyzed)
          #FulfillmentText = index_to_symptom[FulfillmentText[0]]
    
    print(FulfillmentText)
    return FulfillmentText
    

def analyze(text_to_be_analyzed):
    global flag
    global li
    '''
    Text input from Audio File should be Parsed here
    '''
    #text_to_be_analyzed = input()
    if flag == 0 :
        ParseToFile = ApplyDialogFlow(text_to_be_analyzed)
        print(ParseToFile)
        return(ParseToFile)
    elif flag == 1:
        FulfillmentText = DiseasePrediction(text_to_be_analyzed)
        FulfillmentText = index_to_symptom[FulfillmentText[0]]
        if FulfillmentText in li:
            FulfillmentText = "Please consult your nearest doctor, your disease might be"+str(FulfillmentText)
        else:
            pass
        print(FulfillmentText)
        flag = 0 
        return FulfillmentText


    '''
    Convert ParseToFile into Audio
    '''