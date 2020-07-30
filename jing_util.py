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
    return pd.DataFrame(rows, columns=['orientation', 'number of tags', 'tags']), N_pics

'''
input: two sets of string elements
output: score between two slides
'''
def transition_score(s1, s2):
    return min(len(s1 & s2), len(s1 - s2), len(s2 - s1))

def deviation_score(s1, s2):
    return (0.5 * min(len(s1), len(s2))) - transition_score(s1, s2)

'''
create a dict that stores the scores between any picture
keys: possible scores
values: list of tuples indicating the picture index pairs
'''
def cal_flow(df, min_score=1):
    f_list = {}

    tags = list(df['tags'].values)

    for i in range(len(tags)-1):
        for j in range(i+1, len(tags)):
            score = transition_score(tags[i], tags[j])
            if score >= min_score:
                if score not in f_list.keys():
                    f_list[score] = [(i,j)]
                else:
                    f_list[score].append((i,j))

    return f_list

'''
print out number of transitions that are grouped in terms of score
input:
    flist, a dictionary of transitions grouped by score
    index, all transitions that contain this particular index
'''
def print_transitions_by_score(dic, index=None, max=None):
    new_dict = {}
    if index is not None:
        count = 0
        for score in sorted(dic, reverse=True):
            if len([x for x in dic[score] if x[0] == index or x[1] == index]) > 0:
                new_dict[score] = [x for x in dic[score] if x[0] == index or x[1] == index]
                print(score, ":", len([x for x in dic[score] if x[0] == index or x[1] == index]))
                # print(score, ":", [x for x in dic[score] if x[0] == index or x[1] == index])
                count += 1
                if count == max: break

    else:
        new_dict = dic
        for score in sorted(dic, reverse=True):
            print(score, ":", len([x for x in dic[score]]))
            # print(score, ":", [x for x in dic[score]])

    return new_dict