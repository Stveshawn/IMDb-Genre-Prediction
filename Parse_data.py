import numpy as np
import h5py
import pandas as pd
import matplotlib.image as img
from sklearn.preprocessing import LabelEncoder

df = pd.read_csv('url_poster.csv')

LE = LabelEncoder()
df['target'] = LE.fit_transform(df['main_genre'])
label_dict = LE.classes_

nn = len(df)
# convert picture to data
print("1. Converting posters png's to data ...", end='\r')
X = np.zeros((nn, *img.imread('posters/0.png', 0).shape))
y = np.zeros(nn, dtype=np.int8)
for i in range(nn):
    try:
        X[i] = img.imread('posters/{}.png'.format(i), 0)/255
        y[i] = int(df2.target[i])
    except:
        pass
    print("1. Converting posters png's to data {:.2f}% ...".format(i/nn*100), end='\r')
print("1. Done converting posters png's to data.               ".format(i/nn*100))


# hf = h5py.File('data.h5', 'w')

# hf.create_dataset('X', data=X)
# hf.create_dataset('y', data=y)
# hf.create_dataset('label_dict', data=np.array(label_dict, dtype='S'))
# hf.close()
# print("2. Data saved to data.h5")