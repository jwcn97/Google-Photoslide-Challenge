from jing_util import *
import time
start_time = time.time()

# 60,000 rows of verticals
# 30,000 rows of horizontals
# df, N_pics = extract_data("d_pet_pictures.txt")

# choose the first 500 pictures for experimentation
# disregard orientation for now
df, N_pics = extract_data("test_test.txt")
# df, N_pics = extract_data("test_file.txt")
# df, N_pics = extract_data("d_pet_pictures.txt")
print("--- finish extracting data %s minutes ---" % ((time.time() - start_time)/60))
print("")

dic = cal_flow(df)
print("--- finish creating score list %s minutes ---" % ((time.time() - start_time)/60))
print("")

scr_list = sorted(dic, reverse=True)
# find nodes with the highest score in the whole matrix
(i,j) = dic[scr_list[0]][0]
# i,j = head & tail of slideshow pointer
new_list = [i,j]
new_list_scr = scr_list[0]
current_len = 0

i_search = True
j_search = True

# continue operation if length of slideshow is still changing
while current_len < len(new_list):
    # update current length of new list
    current_len = len(new_list)

    if i_search or j_search:
        i_search = False
        j_search = False

        for score in scr_list:
            if not i_search:
                # list of possible transitions at the head of the slideshow
                lst = [x for x in dic[score] if i in x]
                # list of possible slides appended to the head of slideshow
                other_lst = [x[0] if i == x[1] else x[1] for x in lst]
                remaining = [x for x in other_lst if x not in new_list]

                
                for k in remaining:
                    for scr in range(score,0,-1):
                        dic[scr] = list(set(dic[scr]) - set([x for x in dic[scr] if i in x]))
                    
                    # append to start of new list and update score
                    new_list.insert(0,k)
                    new_list_scr += score
                    # a slide has been found, break from the loop
                    i_search = True
                    # update head pointer of slideshow
                    i = k
                    # # remove connections that are already in the slideshow to speed up search the next round
                    # dic[score] = list(set(dic[score]) - set(lst))
                    break

            if not j_search:
                # list of possible transitions at the tail of the slideshow
                lst = [x for x in dic[score] if j in x]
                # list of possible slides appended to the tail of slideshow
                other_lst = [x[0] if j == x[1] else x[1] for x in lst]
                remaining = [x for x in other_lst if x not in new_list]

                
                for k in remaining:
                    for scr in range(score,0,-1):
                        dic[scr] = list(set(dic[scr]) - set([x for x in dic[scr] if j in x]))
                    
                    # append to end of new list and update score
                    new_list.append(k)
                    new_list_scr += score
                    # a slide has been found, break from the loop
                    j_search = True
                    # update tail pointer of slideshow
                    j = k
                    # # remove connections that are already in the slideshow to speed up search the next round
                    # dic[score] = list(set(dic[score]) - set(lst))
                    break
                
            if i_search and j_search: break

    print("score:", new_list_scr, "; list_len:", len(new_list))

print("--- finish creating slideshow %s minutes ---" % ((time.time() - start_time)/60))
print("")