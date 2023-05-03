import re
from langchain import PromptTemplate
from langchain.text_splitter import RecursiveCharacterTextSplitter
import os.path
import time
import json
import matplotlib as plt
import pandas as pd
import spacy
import seaborn as sns
import pandas as pd
import numpy as np

 


nlp = spacy.load("en_core_web_lg")



def read_text(textfile):
    
    with open(textfile, 'r') as file:
        data = file.read().rstrip()
    
    text_splitter = RecursiveCharacterTextSplitter(chunk_size = 12000, chunk_overlap = 0)
    texts= text_splitter.split_text(data)

    number_splits = len(texts)
    total_tokens = round(len(data)/4000)
    
    
    return(data,texts)


def prepare_json_topics(repsonse_input):
    
    list_topics=[]
    list_probas =[]

    y=json.loads(repsonse_input[0]['content'])


    for topic in y['topics']:
        
        list_topics.append(topic['topic'])
        list_probas.append(topic['rating'])

    
    return list_topics, list_probas



def prepare_json_scale(repsonse_input):
    
    list_scale=[]
    list_rating =[]


    y=json.loads(repsonse_input[0]['content'])


    for scales in y['scales']:
        list_scale.append(scales['scale'])
        list_rating.append(scales['rating'])

    
    return list_scale, list_rating    


def prepare_dataframe(textfile):

    df = pd.read_table(textfile ,header = None, encoding= 'unicode_escape',names=['text'])
    return df


def df_nouns_verbs(df,column_name):


    nouns_text = []
    verbs_text=[]
    nouns_list=[]
    verbs_list=[]

    for irow, row in df.iterrows():
        doc = nlp(df[column_name][irow])
        #print(doc)
        #print(irow)
        
        for token in doc:
            if token.pos_ == "NOUN" and not token.is_stop:
                nouns_text.append(token)
                nouns_list.append(str(token))
            if token.pos_ == "VERB" and not token.is_stop:
                verbs_text.append(token)
                verbs_list.append(str(token))
                #print(token.text, token.pos_, token.dep_)
        #print(norm_text)
        #break
        
        df.loc[irow,'nouns']=str(nouns_text)
        df.loc[irow,'verbs']=str(verbs_text)
        nouns_text=[]
        verbs_text =[]


    return df,nouns_list, verbs_list

def prep_df_for_wordlcoud(df,nouns_list,verbs_list):
    from collections import Counter
    my_series_nouns = pd.Series(Counter(nouns_list)).sort_values(ascending =False)
    my_series_verbs= pd.Series(Counter(verbs_list)).sort_values(ascending=False)
    
    my_df_nouns = pd.DataFrame(my_series_nouns)
    my_df_verbs=pd.DataFrame(my_series_verbs)
    
    arr_nouns =np.array(my_df_nouns[0])
    noun_quantile = np.quantile(arr_nouns,0.8)
    arr_verbs=np.array(my_df_verbs[0])
    verb_quantile = np.quantile(arr_verbs,0.8)

    nouns_cut_off=list(my_df_nouns[my_df_nouns[0]>noun_quantile].index)
    verbs_cut_off=list(my_df_verbs[my_df_verbs[0]>verb_quantile].index)

    return nouns_cut_off,verbs_cut_off