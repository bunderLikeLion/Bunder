import pandas as pd
import numpy as np
import random

categories = ['문학', '예술', '자기계발', '정치/사회', '과학', '기술/IT', '인문']

df = pd.read_excel('bestseller.xlsx', usecols="D,K")
df = df.set_index('상품명').T.to_dict('list')
keys = list(df.keys()) # keys
values = np.array(list(df.values())).flatten() # values
zip_dict = zip(keys, values)

book_category_dict = dict(zip_dict)

literature = []
for key in book_category_dict.keys():
    if book_category_dict.get(key) == '문학':
        literature.append(key)

random_literature = random.choices(literature, k=3)
print(random_literature)