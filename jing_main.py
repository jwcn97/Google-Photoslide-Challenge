from jing_util import *
import time
import sys
import pprint

start_time = time.time()
absolute_start = start_time
clear_interval = 1000

# 60,000 rows of verticals and 30,000 rows of horizontals
# only choose horizontal for now

df = extract_data("d_pet_pictures.txt")
N_pics = len(df)
hor = df[df['orientation'] == 'H']
ver = df[df['orientation'] == 'V']

# create dictionary
# key: number of tags in a picture
# value: picture ID
dic = num_tag_dict(hor)
dic = num_tag_dict(ver, dic)
scr_list = sorted(dic, reverse=True)
print("\nFinish extracting and storing data in %s seconds" % round(time.time() - start_time))
start_time = time.time()

# FIND FIRST PAIR
i = j = None
new_list_scr = 0
num_max = None
for slide in dic[scr_list[0]]:
    for num in scr_list:
        for other in dic[num]:
            score = transition_score(df, slide1, slide2)
            if score > new_list_scr:
                i, j, num_max, new_list_scr = slide, other, num, score

        if num < (new_list_scr * 2): break

dic[scr_list[0]].remove(i)
dic[num_max].remove(j)

new_list = [i,j]
current_len = 1

# continue operation if length of slideshow is still changing
while current_len < len(new_list):
    # update current length of new list
    current_len = len(new_list)

    if current_len % clear_interval == 0:
        print("length of slideshow: %s ; score: %s ; time: %s minutes" % (len(new_list), new_list_scr, round((time.time() - start_time)/60)))
        start_time = time.time()

    # CHOOSING PHOTO TO APPEND TO THE HEAD
    max_score = 0
    max_slide = None
    for num in scr_list:
        for other in dic[num]:
            # calculate maximum possible score between front photo and the rest of the unused photos
            score = transition_score(df, i, other)
            if score > max_score:
                max_score, max_slide = score, [num, other]

        # maximum score between slides = 0.5 * number of tags of pic with lesser tags
        # break from loop if number of tags is smaller than twice the maximum score
        if num < (max_score * 2): break

    if max_slide:
        i = max_slide[1]            # update head pointer
        new_list.insert(0, i)       # append to start of slideshow
        new_list_scr += max_score   # update score
        dic[max_slide[0]].remove(i) # remove photo from dictionary

    # CHOOSING PHOTO TO APPEND TO THE TAIL
    max_score = 0
    max_slide = None
    for num in scr_list:
        for other in dic[num]:
            score = transition_score(df, j, other)
            if score > max_score:
                max_score, max_slide = score, [num, other]
        
        if num < (max_score * 2): break

    if max_slide:
        j = max_slide[1]
        new_list.append(j)
        new_list_scr += max_score
        dic[max_slide[0]].remove(j)

print("length of slideshow: %s ; score: %s ; time: %s minutes" % (len(new_list), new_list_scr, round((time.time() - start_time)/60)))
start_time = time.time()

file1 = open("submission.txt","w")
for slide in new_list:
    file1.write(" ".join([str(x) for x in slide]) + "\n")
file1.close()
print("updated submission file: %s minutes" % round((time.time() - start_time)/60))

print("Total time: %s minutes" % round((time.time() - absolute_start)/60))