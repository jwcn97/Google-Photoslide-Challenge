from jing_util import *
import time
import sys
start_time = time.time()
absolute_start = start_time

# 60,000 rows of verticals and 30,000 rows of horizontals
# disregard orientation for now

df, N_pics = extract_data("d_pet_test.txt")
# df, N_pics = extract_data("d_pet_pictures.txt")
clear_interval = min(1000, N_pics)

print("")
print("finish extracting data in %s ms" % ((time.time() - start_time)*1000))
start_time = time.time()

dic = cal_flow(df, min_score=2)
print("finish creating score dict in %s minutes" % ((time.time() - start_time)/60))
print("")
start_time = time.time()

scr_list = sorted(dic, reverse=True)
# find nodes with the highest score in the whole matrix
(i,j) = dic[scr_list[0]][0]
# i,j = head & tail of slideshow pointer
new_list = [i,j]
new_list_scr = scr_list[0]
current_len = 1

i_search = j_search = True

# continue operation if length of slideshow is still changing
while current_len < len(new_list):
    # update current length of new list
    current_len = len(new_list)

    # remove transition scores relating to slides that are already used up
    # computationally expensive and tedious, run only in pre-determined intervals
    if current_len % clear_interval == 0:
        print("score:", new_list_scr)
        print("--- finish creating slides %s to %s in %s minutes ---" % ((current_len-clear_interval+1), current_len, (time.time() - start_time)/60))
        start_time = time.time()

        occupied = new_list[1:-1]
        for scr in scr_list:
            dic[scr] = [x for x in dic[scr] if len(set(x) & set(occupied)) == 0]
            print("score %s: taken %s minutes" % (scr, (time.time() - start_time)/60))

        print("--- finish clearing part %s/%s of dict in %s minutes ---" % ((current_len//clear_interval), (N_pics//clear_interval), (time.time() - start_time)/60))
        print("")
        start_time = time.time()

    if i_search or j_search:
        i_search = j_search = False

        # loop through transitions from highest score to lowest score
        for score in scr_list:
            if not i_search:
                # list of possible transitions at the head of the slideshow
                lst = [x for x in dic[score] if i in x]
                # list of possible slides appended to the head of slideshow
                others = [x[0] if i == x[1] else x[1] for x in lst]
                others = [x for x in others if x not in new_list]
                
                if len(others) > 0:
                    new_list.insert(0,others[0]) # append to start of new list
                    new_list_scr += score        # update score
                    i_search = True              # a slide has been found, break from the loop
                    i = others[0]                # update head pointer of slideshow

            if not j_search:
                # list of possible transitions at the tail of the slideshow
                lst = [x for x in dic[score] if j in x]
                # list of possible slides appended to the tail of slideshow
                others = [x[0] if j == x[1] else x[1] for x in lst]
                others = [x for x in others if x not in new_list]

                if len(others) > 0:
                    new_list.append(others[0]) # append to end of new list
                    new_list_scr += score      # update score
                    j_search = True            # a slide has been found, break from the loop
                    j = others[0]              # update tail pointer of slideshow
                
            # both head and tails have been appended
            if i_search and j_search: break

    # print("score:", new_list_scr, "; list_len:", len(new_list))

print("--- finish creating slideshow in %s hours ---" % ((time.time() - absolute_start)/3600))