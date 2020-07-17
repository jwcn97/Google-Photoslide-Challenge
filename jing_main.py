from jing_util import *

# 60,000 rows of verticals
# 30,000 rows of horizontals
df = extract_data("d_pet_pictures.txt")

verts = df[df['orientation'] == 'V']
horis = df[df['orientation'] == 'H']

print(verts)