import os.path
import time
import matplotlib.pyplot as plt
from wordcloud import WordCloud
import spacy



nlp = spacy.load("en_core_web_lg")



#change the value in return to set the single color need, in hsl format.
def grey_color_func(word, font_size, position,orientation,random_state=None, **kwargs):
    return "black"




# define drawing of the words and links separately.
def plot_main_topics(topics,values):

    

    px = 1/plt.rcParams['figure.dpi']
    
    fig = plt.figure(figsize=(640*px, 480*px))
    plt.clf()
    
    for i, word in enumerate(topics):
        plt.text(0.5,0.9-i*0.2, word, ha="center", va="center",size=values[i]*30)
        
    plt.axis('off')
    plt.savefig('main_topics.png')



def plot_categories(str_scale, str_rating):
    i=0
    px = 1/plt.rcParams['figure.dpi']
    
    fig = plt.figure(figsize=(640*px, 480*px))
 
    # creating the bar plot
    bar = plt.barh(str_scale,str_rating, color ='blacK')
    

     # Add counts above the two bar graphs
    for rect in bar:
        width = rect.get_width()
     
        
        
        
        plt.text(width+0.5,rect.get_y()+rect.get_height()/2, f'{str_rating[i]}', ha='center', va='bottom',color = 'black', size=20)
        #plt.text(rect.get_x() + rect.get_width() /2, 0.08, f'{str_topic[i]}', ha='center', va='bottom',rotation = 90,color = 'white', size=15)
        i=i+1
    plt.xlim(0,10) 
    plt.axvline(x = 10, color = 'black', label = 'axvline - full height',lw=10)
    plt.xticks([])
    plt.tight_layout()
    plt.savefig('categories.png')
  


def plot_summary(text):
    
    px = 1/plt.rcParams['figure.dpi']

    fig = plt.figure(figsize=(640*px, 480*px))

    plt.text(0,0,text, family='serif',size=18, va='top', wrap=True)

    plt.xticks([])
    plt.tight_layout()
    plt.axis('off')
    plt.savefig('summary.png')


def plot_wordcloud(df,stopwordslist,savefigas):
    
    stop_words = nlp.Defaults.stop_words.union(stopwordslist)
    # Start with one review:
    text = " ".join(nouns for nouns in df.nouns)

    wordcloud = WordCloud(max_font_size=50, max_words=15,height=300, width=400,background_color="white",stopwords  = stop_words).generate(text)
    #plt.imshow(wordcloud, interpolation='bilinear')
    default_colors = wordcloud.to_array()

    plt.imshow(wordcloud.recolor(color_func=grey_color_func), interpolation="bilinear")


    plt.axis("off")
    plt.savefig(f'{savefigas}.png')

