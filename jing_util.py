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
def transition_score(df, slide1, slide2):
    s1 = set.union(*[set(df.loc[x, 'tags']) for x in slide1])
    s2 = set.union(*[set(df.loc[x, 'tags']) for x in slide2])
    return min(len(s1 & s2), len(s1 - s2), len(s2 - s1))

'''
create a dict
keys: number of tags a photo has
values: photos that has that number of tags
'''
def num_tag_dict(df, t_list=None):
    if not t_list:
        t_list = {}

    taglist = list(df['tags'].values)
    orientation = df['orientation'].values[0]

    if orientation == 'H':
        for i in range(0, len(taglist), 1):
            tag_len = len(taglist[i])
            photoID = [df.iloc[[i]].index[0]]

            # append photo into empty slide
            # assign slide to appropriate key value
            if tag_len not in t_list.keys():
                t_list[tag_len] = [photoID]
            else:
                t_list[tag_len].append(photoID)

    elif orientation == 'V':
        for i in range(0, len(taglist), 2):
            if i == len(df)-1: break

            tag_len = len(taglist[i] | taglist[i+1])
            photoID = [df.iloc[[i]].index[0], df.iloc[[i+1]].index[0]]

            # append adjacent photos into empty slide
            # (todo: pair V photos in a way to maximise score)
            # assign slide to appropriate key value
            if tag_len not in t_list.keys():
                t_list[tag_len] = [photoID]
            else:
                t_list[tag_len].append(photoID)

    return t_list