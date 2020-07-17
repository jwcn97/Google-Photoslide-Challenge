import pandas as pd

df = pd.read_fwf('d_pet_pictures.txt')
# df = df[1:]
print(df.iloc[0:2,:])

# # open file
# f = open("d_pet_pictures.txt", "r")
# # skips the first line (which just tells us how many pictures there are)
# next(f)

# for line in f:
#     arr = line.split(" ", 2)
#     arr[-1] = arr[-1][:-1]
#     print(arr)
#     break

# f.close()