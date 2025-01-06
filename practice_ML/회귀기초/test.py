import pandas as pd
import numpy as np
print(1)

pd.DataFrame([1,2,3])
np.array([1,2,3])



books = ['a', 'b', 'c', 'b', 'b', 'c', 'z', 'x', 'a', 'a']

book_dict = {}
for book in books:
    book_dict[book] = book_dict.get(book, 0) + 1
    
book_list = list(book_dict.items())
print(book_list)
book_list.sort(key=lambda x: (-x[1], x[0]))

print(book_list)

