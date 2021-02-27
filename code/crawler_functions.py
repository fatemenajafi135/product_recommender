'''

author: Fateme Najafi

Functions for crawling digikala's products
Using BeautifulSoup

'''

# import pandas as pd
import numpy as np
import time
import pickle
import requests
from bs4 import BeautifulSoup as bs
from utils import read_pickle, write_to_pickle

def product_digi(dkp):
    '''
    By giving the product's number, it returns some information about product in as a list.
    input:
        * dkp: integer, product name and number
    information about the product (output):
        * string: product number
        * string: product name
        * string: a description about the product
        * list: classes of the product
        * boolean: Is product in stock
    '''
    url = 'https://www.digikala.com/product/dkp-'+str(dkp)+'/'
    res = requests.get(url)
    soup = bs(res.content)
    # classes and name of product
    spans = soup.find_all('span',{"property":"name"})
    classes = [str(each_span).replace('<span property="name">', '').replace('</span>','') for each_span in spans]
    # description
    text = soup.find('div',{'class':"c-mask js-mask"})
    text = (str(text).split('\n'))[1:-3]
    # Is it in the stock?
    stock = [str(i) for i in soup.find_all('span',{'class':'btn-add-to-cart__txt'})    ]
    is_stocked = 'افزودن به سبد خرید' in (' '.join(stock))
    return [dkp, classes[-1], ' '.join(text), classes[1:-1], is_stocked]


def crawling_digikala(start, size, file_path, file_number):
    '''
    After loaing the product's page, It stores existing items in a file and the name of unavailables in another one.
    input:    
        * start: integer, number (and name) of the first product to be crawl
        * size: integer, number of digikala product in each round
        * file_path: string, the path for writing pickle files
        * file_number: string, file's path and name
    example of existing items file names: digikala_p_stocked0.pkl
    example of unavailable items file names: digikala_p_doesnt_exist0.pkl
    '''
    columns = []
    doesnt_exist = []
    for product in range(start, start+size):
        # s1  = time.time()
        try:
            columns.append(product_digi(product))
        except:
            doesnt_exist.append(product)
        # s2  = time.time()
        # print((str(product)+" "+str(s2-s1)))
    write_to_pickle(columns, file_path+str(file_number)+".pkl")
    write_to_pickle(columns, file_path+'doesnt_exist_'+str(file_number)+".pkl")


def run_crawler(first_product, scale, size, file_name):
    '''
    It runs "crawling_digikala" function by creating an iterator list.
    input:    
        * first_product: integer, number (and name) of the first product to be crawl
        * scale: integer, number of digikala product at all
        * size: integer, number of digikala product in each round
        * file_name: string, file's path and name
    (Because of some limits, I needed to crawl on small scales.)
    '''
    iterate = (np.arange(first_product, first_product+scale, size).tolist())
    for index, iter in enumerate(iterate):
        s1  = time.time()
        
        # crawling_digikala(iter, size, '/content/drive/MyDrive/Project/Yektanet/digikala/digikala_p_', str(index+file_name))
        crawling_digikala(iter, size, 'data/pickle_files/digikala_p_', str(index+file_name))
        s2  = time.time()
        print((index), 'in', str(s2-s1), 'seconds done!')

