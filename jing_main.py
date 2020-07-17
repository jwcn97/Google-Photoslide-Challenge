from jing_util import *

# 60,000 rows of verticals
# 30,000 rows of horizontals
df = extract_data("d_pet_pictures.txt")

verts = df[df['orientation'] == 'V']
horis = df[df['orientation'] == 'H']

v_tags = [0,1,2,3,4,5,6,7,8]

# v_tags = verts['tags'].values

res = [(i,j) for i in range(len(v_tags)) 
          for j in range(i + 1, len(v_tags) + 1)]

print(res)