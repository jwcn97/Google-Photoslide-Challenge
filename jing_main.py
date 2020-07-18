from jing_util import *

# 60,000 rows of verticals
# 30,000 rows of horizontals
# df = extract_data("test_file.txt")
df = extract_data("d_pet_pictures.txt")

# verts = df[df['orientation'] == 'V']
# horis = df[df['orientation'] == 'H']

df["max"] = 0
MAX_LEN = 15

df = cal_max(df, max_len=MAX_LEN)
print(df)

optimise(0, list(df["max"]))