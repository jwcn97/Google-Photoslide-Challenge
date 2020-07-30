import pandas as pd
import numpy as np
from collections import deque
import random

'''
input: name of textfile
output: dataframe
'''
def extract_data(filename):
    # open file
    f = open(filename, "r")
    N_pics = int(f.readline())

    rows = []
    for line in f:
        arr = line.split(" ", 2)
        arr[-1] = arr[-1].replace('\n', '')
        arr[-1] = set(arr[-1].split(" "))
        rows.append(arr)

    # close file
    f.close()
    # append into dataframe
    return pd.DataFrame(rows, columns=['orientation', 'number of tags', 'tags'])

'''
input: two sets of string elements
output: score between two slides
'''
def transition_score(s1, s2):
    return min(len(s1 & s2), len(s1 - s2), len(s2 - s1))

'''
create a dict
keys: number of tags a photo has
values: photos that has that number of tags
'''
def num_tag_dict(df):
    t_list = {}
    taglist = list(df['tags'].values)

    for i in range(len(taglist)):
        tag_len = len(taglist[i])
        if tag_len not in t_list.keys():
            t_list[tag_len] = [df.iloc[[i]].index[0]]
        else:
            t_list[tag_len].append(df.iloc[[i]].index[0])

    return t_list