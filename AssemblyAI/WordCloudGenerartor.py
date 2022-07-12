from wordcloud import WordCloud
import os
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

#change the value in return to set the single color need, in hsl format.
def grey_color_func(word, font_size, position,orientation,random_state=None, **kwargs):
    return "black" 

# read text from file and store in a variable
with open("/home/pi/content.txt") as file:
    data = file.read()

# create wordcloud using data
wordcloud = WordCloud(
    background_color="white", height=300, width=400,
    include_numbers = True, min_word_length=6, # minimum length of word
    max_words = 15, margin = 4 # margin between words
).generate(data)

default_colors = wordcloud.to_array()

plt.imshow(wordcloud.recolor(color_func=grey_color_func),
interpolation="bilinear")

plt.axis("off")
plt.savefig('latestWordCloud.png')
plt.savefig('/home/pi/latestWordCloud.png')
#plt.show()

#
os.system("python3 /home/pi/Pimoroni/inky/examples/what/dither-image-what.py --colour 'red' --image '/home/pi/latestWordCloud.png'")

