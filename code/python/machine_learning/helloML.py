#!/usr/local/bin/python3
import numpy as np

from sklearn import preprocessing

#We imported a couple of packages. Let's create some sample data and add the line to this file:

print("Preprocessing techniques")
input_data = np.array([[3, -1.5, 3, -6.4], [0, 3, -1.3, 4.1], [1, 2.3, -2.9, -4.3]])
print("input data \n",input_data)

#remove mean (each value is substracted by mean). Then print mean and std dev
data_standardized = preprocessing.scale(input_data)
print("\nMean = ", data_standardized.mean(axis = 0))
print("Std deviation = ", data_standardized.std(axis = 0))

#scale values to fit between 0-1
data_scaler = preprocessing.MinMaxScaler(feature_range = (0, 1))
data_scaled = data_scaler.fit_transform(input_data)
print ("\nMin max scaled data = ", data_scaled)

#normalize, scale values so that sum to 1 
data_normalized = preprocessing.normalize(input_data, norm  = 'l1')
print ("\nL1 normalized data = ", data_normalized)

#convert value to binary. here use threshold of 1.4
data_binarized = preprocessing.Binarizer(threshold=1.4).transform(input_data)
print ("\nBinarized data =", data_binarized)

#one-hot encode. instead of label encoding (assign number) assign a binary of K (# of categories) bits. all 0 but nth bit (n is category number)
encoder = preprocessing.OneHotEncoder(categories='auto')
encoder.fit([  [0, 2, 1, 12], 
               [1, 3, 5, 3], 
               [2, 3, 2, 12], 
               [1, 2, 4, 3]
])
encoded_vector = encoder.transform([[2, 3, 5, 3]]).toarray()
print ("\nEncoded vector =", encoded_vector)

#label encode. assign each category a number
label_encoder = preprocessing.LabelEncoder()
input_classes = ['suzuki', 'ford', 'suzuki', 'toyota', 'ford', 'bmw']
#create label encoding
label_encoder.fit(input_classes)
print ("\nClass mapping:")
for i, item in enumerate(label_encoder.classes_):
    print (item, '-->', i)

#apply label encoding
labels = ['toyota', 'ford', 'suzuki']
encoded_labels = label_encoder.transform(labels)
print("\nLabels =", labels)
print("Encoded labels =", list(encoded_labels))

#inverse label encoding
encoded_labels = [3, 2, 0, 2, 1]
decoded_labels = label_encoder.inverse_transform(encoded_labels)
print ("\nEncoded labels =", encoded_labels)
print ("Decoded labels =", list(decoded_labels))


print("Analysis techniques")
import pandas
data = 'pima-indians-diabetes.csv'
names = ['Pregnancies', 'Glucose', 'BloodPressure', 'SkinThickness', 'Insulin', 'Outcome']
dataset = pandas.read_csv(data, names = names)
print(dataset.shape)
print(dataset.head(20))
print(dataset.describe())
print(dataset.groupby('Outcome').size())

import pandas
import matplotlib.pyplot as plt
data = 'iris_df.csv'
names = ['sepal-length', 'sepal-width', 'petal-length', 'petal-width', 'class']
dataset = pandas.read_csv(data, names=names)
dataset.plot(kind='box', subplots=True, layout=(2,2), sharex=False, sharey=False)
plt.show()

dataset.hist()
plt.show()

from pandas.plotting import scatter_matrix
scatter_matrix(dataset)
plt.show()

