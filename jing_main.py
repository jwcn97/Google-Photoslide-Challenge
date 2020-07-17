from jing_util import *

df = extract_data("d_pet_pictures.txt")

print(compute_score(df.iloc[0,2], df.iloc[1,2]))