'''

author: Fateme Najafi

Functions for cleaning data

'''



import re
import emoji
from utils import read_pickle

'''
Some dictionary and list we needed for cleaning data
'''
# stopwords = read_pickle('/content/drive/MyDrive/Project/Yektanet/stopwords.pkl')
# chars_dictionary = read_pickle('/content/drive/MyDrive/Project/Yektanet/chars_replacement.pkl')
# numbers_dictionary = read_pickle('/content/drive/MyDrive/Project/Yektanet/numbers_to_en.pkl')
stopwords_product = {'بسته', 'کد', 'عددی', 'مدل', 'طرح', 'مناسب', 'متر', 'سایز', 'سانتی', 'و'}
stopwords = read_pickle('data/stopwords.pkl')
chars_dictionary = read_pickle('data/chars_replacement.pkl')
numbers_dictionary = read_pickle('data/numbers_to_en.pkl')

def remove_emojis(s):
    '''
    returns given string without any emojis
    '''
    return ''.join(c for c in s if c not in emoji.UNICODE_EMOJI)

def character_refinement(text):
    '''
    for integration
    '''
    for ch in chars_dictionary.keys():
        text = text.replace(ch, chars_dictionary[ch])
    return text

def remove_stopwords(text_tokenized):
    '''
    returns given string without any stopwords
    '''
    return [word for word in text_tokenized if word not in stopwords_product]

def handle_numbers(text, task = 'remove'):
    '''
    task:
      * 'remove' replace with '' and remove it
      * 'replace' replace with N
      * 'refinement' replace each persian numbers with english
    '''
    replace_with = ""
    if (task == 'replace'):
            replace_with = "N"
    if (task == 'refinement'):
            for ch in numbers_dictionary.keys():
                text = text.replace(ch, str(numbers_dictionary[ch]))
            return text
    else: 
            text = re.sub('((2[0-4]|[0-1]?[0-9]):([0-5][0-9]|[0-9]))', replace_with, text)
            text = re.sub('((۲[۰-۴]|[۰-۱]?[۰-۹]):([۰-۵][۰-۹]|[۰-۹]))', replace_with, text)
            text = re.sub(r'\d+', replace_with, text) 
    return text

def clean_string(text, return_string = True):
    '''
    It cleans given text in these steps:
      * removing emojis
      * removing english alphabets
      * removing punctation
      * refining numbers
      * refining charecter
      * removing typical and product stopwords
      * lemmetization
    '''
    # text = re.sub(r'\\','',text)
    # text = re.sub(r'\xa0','',text)
            
    # emojis
    text = remove_emojis(text)
            
    # remove english alphabet
    text = re.sub(r'[a-zA-Z]+','',text)
            
    # punctation
    text = text.replace('_','')
    text = text.replace('ـ','')
    text = re.sub(r'[^\w\d\s]+','',text)
            
    # remove number 
    text = handle_numbers(text, task = 'refinement')
            
    # Char refinement
    text = character_refinement(text)

    text = " ".join(text.split())
    text = text.split(' ')

    # stop words
    text = remove_stopwords(text)

    # lemmetization       = > doesn't need now
            
    if (return_string):
              return (" ".join(text))
    return text

def clean_data(data, return_string = True):
    return [clean_string(text, return_string) for text in data]
