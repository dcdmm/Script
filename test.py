import numpy as np

arr = np.array([1, 2, 3])
print(arr)


import pandas as pd

df = pd.DataFrame(arr)
print(df)

df.columns = ["a", "b", "c"]

arr1 = np.array([1, 2, 3, 4])
print(arr1)

arr2 = np.array([1, 2, 3, 4, 5])
print(arr2)