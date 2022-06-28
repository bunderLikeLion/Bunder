import pandas as pd
import numpy as np
import random

categories = ['문학', '예술', '자기계발', '정치/사회', '과학', '기술/IT', '인문']

df = pd.read_excel('./utilities/bestseller.xlsx', usecols="D,K")
df = df.set_index('상품명').T.to_dict('list')
keys = list(df.keys())  # keys
values = np.array(list(df.values())).flatten()  # values
zip_dict = zip(keys, values)

book_category_dict = dict(zip_dict)


def get_random_book_list(category):
    array = list(book_category_dict)
    if category == "기타":
        random_list = random.choices(array, k=3)
    else:
        for key in book_category_dict.keys():
            if book_category_dict.get(key) == category:
                array.append(key)
        random_list = random.choices(array, k=3)

    return random_list