import openai
import re
from langchain import PromptTemplate
from langchain.text_splitter import RecursiveCharacterTextSplitter
import configparser
import os.path
import time
import argparse

from provotype.prep import read_text,prepare_dataframe,df_nouns_verbs,prep_df_for_wordlcoud
from provotype.promts_gpt import generate_summarizer,do_summarization,create_five_topics,create_summary,scale_conversation
from provotype.generate_output import plot_main_topics,plot_categories,plot_summary,plot_wordcloud

def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--configfile', default='config.ini',metavar='N', type=str, nargs='+',
                        help='an integer for the accumulator')
    parser.add_argument('--textfile', default = 'textfile.txt', metavar='N', type=str, nargs='+',
                        help='an integer for the accumulator')
    args = parser.parse_args()
    print(args.configfile)
    return args


def parse_config(configfile):
    config = configparser.ConfigParser()   
    config.read(configfile)
    api_key = config['API']['my_api']
    return api_key
   
 


def do_job(text_file):
    
    from time import sleep

    whole_text, splitted_text = read_text(text_file)
    df_text = prepare_dataframe(text_file)

    df_text,nouns_list,verbs_list = df_nouns_verbs(df_text,'text')

    nouns_cut_off, verbs_cut_off = prep_df_for_wordlcoud(df_text,nouns_list,verbs_list)

    plot_wordcloud(df_text,nouns_cut_off,'wordcloud_nouns')
    plot_wordcloud(df_text,verbs_cut_off,'wordcloud_verbs')

    text_summarization = do_summarization(splitted_text)
    #response_summary = create_summary(text_summarization)

    plot_summary(response_summary[0]['content'])
    
    print("summary done!\n")

    topics,rating  = create_five_topics(text_summarization)
    
    plot_main_topics(topics,rating)
    print("topics done!\n")
    

    list_scale, list_rating_scale = scale_conversation(text_summarization)
    print("scale conversation done!\n")
    plot_categories(list_scale, list_rating_scale)



def main(args):
    config = args.configfile
    textfile = args.textfile
    
    if config is not None:
        api_key = parse_config(config)

        openai.api_key = api_key

        print(api_key)
        
        if textfile is not None:
            do_job(textfile)
         
        else:
            print("no textfile available")
        
    



if __name__=='__main__':  
   
    args = get_args()
    main(args)