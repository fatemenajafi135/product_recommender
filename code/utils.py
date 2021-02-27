'''

author: Fateme Najafi

Some useful functions

'''

import pickle

def write_to_pickle(obj, file_name):
    '''
    Writes given object (obj) as a pickle file in the given path(file_name)
    '''
    open_file = open(file_name, "wb")
    pickle.dump(obj, open_file)
    open_file.close()

def read_pickle(file_name):
    '''
    Reads given pickle file by its path(file_name) and returns the object
    '''
    open_file = open(file_name, "rb")
    data = pickle.load(open_file)
    open_file.close()
    return data
