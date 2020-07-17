import pandas as pd

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
def transition_score(slide1, slide2):
    intersect = slide1 & slide2
    s1 = slide1 - slide2
    s2 = slide2 - slide1
    return min(len(intersect), len(s1), len(s2))
