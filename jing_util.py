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

'''
create a dict that stores the scores between any picture
keys: possible scores
values: list of tuples indicating the picture index pairs
'''
def cal_flow(df):
    f_list = {}

    tags = list(df['tags'].values)

    for i in range(len(tags)-1):
        for j in range(i+1, len(tags)):
            score = transition_score(tags[i], tags[j])
            if score > 0:
                if score not in f_list.keys():
                    f_list[score] = [(i,j)]
                else:
                    f_list[score].append((i,j))

    return f_list

'''
calculate maximum score pairings
'''
def cal_max(df, max_len=10, interval=500):
    tags = list(df['tags'].values)

    for i in range(len(tags)):
        max_score = deque(maxlen=max_len)
        for j in range(len(tags)):
            if i == j: continue
            
            score = transition_score(tags[i], tags[j])
            if len(max_score) == 0:
                max_score.append((j, score))
            else:
                old_len = len(max_score)
                for k in range(len(max_score),0,-1):
                    if score >= max_score[k-1][-1]:
                        if len(max_score) == max_len:
                            max_score.popleft()
                            k -= 1
                        max_score.insert(k, (j, score))
                        break
                if (len(max_score) < max_len) and (old_len == len(max_score)):
                    max_score.insert(0, (j, score))

        df.loc[i,"max"] = ",".join([str(x) for x in list(max_score)])

        if i+1 % interval == 0:
            print(i, ":", max_score)

    return df

'''
arrange slides according to maximum score pairings
'''
def optimise(start, slides, interval):
    new_slides = [(start,0)]
    for i in range(len(slides)-1):
        j = -1
        next_slide = eval(slides[start])
        while next_slide[j][0] in [x[0] for x in new_slides]:
            j -= 1
            if -j > len(next_slide): break
        
        if -j <= len(next_slide):
            new_slides.append(next_slide[j])
            start = next_slide[j][0]
        else:
            remaining = set(range(len(slides))) - set([x[0] for x in new_slides])
            next_pic = random.choice(list(remaining))
            score = transition_score(set(eval(slides[start])), set(eval(slides[next_pic])))
            new_slides.append((next_pic, score))
            start = next_pic

        if i+1 % interval == 0:
            print("score:", sum([x[1] for x in new_slides]))

    return [x[0] for x in new_slides], sum([x[1] for x in new_slides])


