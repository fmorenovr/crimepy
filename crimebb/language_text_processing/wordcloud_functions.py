import matplotlib.pyplot as plt
import numpy as np

from wordcloud import WordCloud

def to_grey_color_func(word, font_size, position, orientation, random_state=None,
                    **kwargs):
    return "hsl(0, 0%%, %d%%)" % random.randint(60, 100)

def showWordCloud(text_dict, title, 
									max_words=10000, 
									mask=None, 
									widht=1000, 
									height=1000, 
									figsize=(20,10), 
									stopwords_avoid=None, 
									to_gray_scale=False):

    x, y = np.ogrid[:widht, :height]

    if mask is None:
        mask = (x - widht/2) ** 2 + (y - widht/2) ** 2 > (widht/2) ** 2
        mask = 255 * mask.astype(int)

    wc = WordCloud(min_font_size=10,  
                   max_font_size=300, 
                   background_color="white", 
                   stopwords=stopwords_avoid, 
                   max_words=max_words, 
                   mask=mask, 
                   contour_color='steelblue', 
                   random_state=42)
    
    wc.generate_from_frequencies(text_dict)

    fig = plt.subplots(figsize=figsize)
    plt.axis("off")
    plt.title(title)
    if to_gray_scale:
    		plt.imshow(wc.recolor(color_func=to_grey_color_func, random_state=3), interpolation="bilinear")
    else:
		    plt.imshow(wc, interpolation="bilinear")
    plt.show()
