import pandas as pd
from collections import deque
import random

'''
input: name of textfile
output: dataframe
'''
def extract_data(filename):
    # open file and skips the first line (which just tells us how many pictures there are)
    f = open(filename, "r")
    next(f)

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
calculate maximum score pairings
'''
def cal_max(df, max_len=10):
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
                    if score > max_score[k-1][-1]:
                        if len(max_score) == max_len:
                            max_score.popleft()
                            k -= 1
                        max_score.insert(k, (j, score))
                        break
                if (len(max_score) < max_len) and (old_len == len(max_score)):
                    max_score.insert(0, (j, score))

        df.loc[i,"max"] = ",".join([str(x) for x in list(max_score)])

    return df

'''
arrange slides according to maximum score pairings
'''
def optimise(start, slides):
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

        print("list:", [x[0] for x in new_slides])
        print("score:", sum([x[1] for x in new_slides]))
        print("")


