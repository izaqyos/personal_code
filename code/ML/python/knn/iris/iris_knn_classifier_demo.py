import numpy as np 
import matplotlib.pyplot as plt 
import pandas as pd 

url = "https://archive.ics.uci.edu/ml/machine-learning-databases/iris/iris.data"
# Assign colum names to the dataset
names = ['sepal-length', 'sepal-width', 'petal-length', 'petal-width', 'Class']

# Read dataset to pandas dataframe
print('reading dataset from', url)
dataset = pd.read_csv(url, names=names)

import seaborn as sns
from pylab import rcParams

def plot_confusion_matrix(cm,
                          target_names,
                          title='Confusion matrix',
                          cmap=None,
                          normalize=True):
    """
    given a sklearn confusion matrix (cm), make a nice plot

    Arguments
    ---------
    cm:           confusion matrix from sklearn.metrics.confusion_matrix

    target_names: given classification classes such as [0, 1, 2]
                  the class names, for example: ['high', 'medium', 'low']

    title:        the text to display at the top of the matrix

    cmap:         the gradient of the values displayed from matplotlib.pyplot.cm
                  see http://matplotlib.org/examples/color/colormaps_reference.html
                  plt.get_cmap('jet') or plt.cm.Blues

    normalize:    If False, plot the raw numbers
                  If True, plot the proportions

    Usage
    -----
    plot_confusion_matrix(cm           = cm,                  # confusion matrix created by
                                                              # sklearn.metrics.confusion_matrix
                          normalize    = True,                # show proportions
                          target_names = y_labels_vals,       # list of names of the classes
                          title        = best_estimator_name) # title of graph

    Citiation
    ---------
    http://scikit-learn.org/stable/auto_examples/model_selection/plot_confusion_matrix.html

    """
    import matplotlib.pyplot as plt
    import numpy as np
    import itertools

    accuracy = np.trace(cm) / float(np.sum(cm))
    misclass = 1 - accuracy

    if cmap is None:
        cmap = plt.get_cmap('Blues')

    plt.figure(figsize=(8, 6))
    plt.imshow(cm, interpolation='nearest', cmap=cmap)
    plt.title(title)
    plt.colorbar()

    if target_names is not None:
        tick_marks = np.arange(len(target_names))
        plt.xticks(tick_marks, target_names, rotation=45)
        plt.yticks(tick_marks, target_names)

    if normalize:
        cm = cm.astype('float') / cm.sum(axis=1)[:, np.newaxis]


    thresh = cm.max() / 1.5 if normalize else cm.max() / 2
    for i, j in itertools.product(range(cm.shape[0]), range(cm.shape[1])):
        if normalize:
            plt.text(j, i, "{:0.4f}".format(cm[i, j]),
                     horizontalalignment="center",
                     color="white" if cm[i, j] > thresh else "black")
        else:
            plt.text(j, i, "{:,}".format(cm[i, j]),
                     horizontalalignment="center",
                     color="white" if cm[i, j] > thresh else "black")


    plt.tight_layout()
    plt.ylabel('True label')
    plt.xlabel('Predicted label\naccuracy={:0.4f}; misclass={:0.4f}'.format(accuracy, misclass))
    plt.show()

def plot_correlation(data):
    '''
    plot correlation's matrix to explore dependency between features
    '''
    # init figure size
    rcParams['figure.figsize'] = 15, 20
    fig = plt.figure()
    sns.heatmap(data.corr(), annot=True, fmt=".2f")
    plt.show()
    fig.savefig('corr.png')

# plot correlation & densities
print('plotting features correlation. high correlation between features (-->1) means one can be dropped. high correlation to labels increase importance')
plot_correlation(dataset)

print('dataset loaded, head:\n',dataset.head())

features = dataset.iloc[:, :-1].values
labels = dataset.iloc[:, 4].values

print("split data to training and test 80/20")
from sklearn.model_selection import train_test_split
features_train, features_test,labels_train, labels_test = train_test_split(features, labels, test_size=0.20)

print("standardize features. since KNN relies on distance (euclidean, manhattan, hamming etc) so normalization of the features is required")

from sklearn.preprocessing import StandardScaler
scaler = StandardScaler() # scale as z = (x-u)/s , where x is the random var, u - mean, s - std deviation
scaler.fit(features_train) #calc mean, std
features_train = scaler.transform(features_train) # normalize train and test data. 
features_test = scaler.transform(features_test)

from sklearn.neighbors import KNeighborsClassifier
classifier = KNeighborsClassifier(n_neighbors=5) #there's no magic number for K. we start w/ 5 but we try out different values...
classifier.fit(features_train, labels_train) # train the model

#predict
labels_predict = classifier.predict(features_test)
# print('prediction of following features', features_test)
# print(labels_predict)

from sklearn.metrics import classification_report, confusion_matrix 
#confusion_matrix is such that Cij = # of i labels predicted as j, so i==j (diagonal) is a hit
#non diagonal are misses. like for binary classification C10 is false negative, C01 is false positive
# classification_report 
#  The recall means "how many of this class you find over the whole number of element of this class"
# The precision will be "how many are correctly classified among that class"
# The f1-score is the harmonic mean between precision & recall
# The support is the number of occurence of the given class in your dataset (so you have 37.5K of class 0 and 37.5K of class 1, which is a really well balanced dataset.

confusion  = confusion_matrix(labels_test, labels_predict)
print(confusion)
plot_confusion_matrix(confusion, target_names=['Iris-versicolor' 'Iris-virginica' 'Iris-setosa'])
# from sklearn.metrics import plot_confusion_matrix as pcm
# pcm(labels_test, labels_predict)
# plt.show()
print(classification_report(labels_test, labels_predict))


single1 = np.array([[ 5.1,          3.5,           1.4,          0.2 ]])
predict1 = classifier.predict(scaler.transform(single1))
print('prediction for {} is {}. expected Iris-setosa'.format(single1, predict1))
