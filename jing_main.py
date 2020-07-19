from jing_util import *

# 60,000 rows of verticals
# 30,000 rows of horizontals
# df, N_pics = extract_data("d_pet_pictures.txt")

# choose the first 500 pictures for experimentation
# disregard orientation for now
df, N_pics = extract_data("test_file.txt")

df["max"] = 0
MAX_LEN = 15
INTERVAL = 500

f_list = cal_flow(df)

# # calculates the top 15 pictures that will give the highest scores for each picture
# # store it in dataframe under the column "max" as a list of tuples
# # tuple = (<index of related picture>, <score with the picture>)
# df = cal_max(df, max_len=MAX_LEN, interval=INTERVAL)

# # choose a starting picture X
# # choose the next picture, Y, that has the highest score with picture X
# # append to slideshow and choose the next picture that has the highest score with picture Y
# # if the next picture is already in the slideshow that is being formed, choose the next highest
# # if all the 15 pictures are used up, choose a random picture that is not in the slideshow
# # repeat process until a slideshow with all the pictures is formed
# print("")
# seq, score = optimise(start=0, slides=list(df["max"]), interval=INTERVAL)
# print("")
# print("=============")
# print(seq)
# print("score:", score)