from sklearn.cross_validation import train_test_split
from sklearn.metrics import confusion_matrix, classification_report
from sklearn.preprocessing import StandardScaler
import pandas as pd
from sklearn import svm
from pathlib import Path
from src import ParseEQ_Class
import pickle
import matplotlib.pyplot as plt
import numpy as np
import itertools


# def plot_confusion_matrix(cm, classes,
#                           normalize=False,
#                           title='Confusion matrix',
#                           cmap=plt.cm.Blues):
#     """
#     This function prints and plots the confusion matrix.
#     Normalization can be applied by setting `normalize=True`.
#     """
#     if normalize:
#         cm = cm.astype('float') / cm.sum(axis=1)[:, np.newaxis]
#         print("Normalized confusion matrix")
#     else:
#         print('Confusion matrix, without normalization')
#
#     print(cm)
#
#     plt.imshow(cm, interpolation='nearest', cmap=cmap)
#     plt.title(title)
#     plt.colorbar()
#     tick_marks = np.arange(len(classes))
#     plt.xticks(tick_marks, classes, rotation=45)
#     plt.yticks(tick_marks, classes)
#
#     fmt = '.2f' if normalize else 'd'
#     thresh = cm.max() / 2.
#     for i, j in itertools.product(range(cm.shape[0]), range(cm.shape[1])):
#         plt.text(j, i, format(cm[i, j], fmt),
#                  horizontalalignment="center",
#                  color="white" if cm[i, j] > thresh else "black")
#
#     plt.tight_layout()
#     plt.ylabel('True label')
#     plt.xlabel('Predicted label')

def runPredictionModel(inputDir):
    if Path("../bin/data_" + inputDir + ".csv").is_file() == False:
        ParseEQ_Class.getUniqueAndAmbiguousMaps(inputDir)
    test_dataframe = pd.read_csv("../bin/data_" + inputDir + ".csv", sep="\t")
    test_dataframe["Length"] = test_dataframe["Length"].astype(int)
    test_dataframe["EffectiveLength"] = test_dataframe["EffectiveLength"].astype(int)
    test_dataframe["TPM"] = test_dataframe["TPM"].astype(int)
    test_dataframe["NumReads"] = test_dataframe["NumReads"].astype(int)
    test_dataframe["ErrorFraction"] = test_dataframe["ErrorFraction"].astype(int)
    #test_dataframe = test_dataframe[test_dataframe.TPM != 0]

    print("Classification started")
    test_dataframe = test_dataframe.drop('Name', axis=1)
    test_dataframe = test_dataframe.drop('Length', axis=1)
    test_dataframe = test_dataframe.drop('EffectiveLength', axis=1)
    # test_dataframe = test_dataframe.drop('TPM', axis=1)
    test_dataframe = test_dataframe.drop('NumReads', axis=1)
    test_dataframe = test_dataframe.drop('Weight', axis=1)
    # test_dataframe = test_dataframe.drop('UniqueMap', axis=1)
    test_dataframe = test_dataframe.drop('ErrorFraction', axis=1)

    X = test_dataframe.drop('Faulty', axis=1)
    y = test_dataframe['Faulty']

    # X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.1)

    X_test = X
    y_test = y
    scaler = StandardScaler()
    scaler.fit(X_test)
    X_test = scaler.transform(X_test)
    filename = 'training_model.sav'
    clf = pickle.load(open(filename, 'rb'))
    predictions = clf.predict(X_test)


    print(confusion_matrix(y_test, predictions))

    # Compute confusion matrix
    # cnf_matrix = confusion_matrix(y_test, predictions)
    # np.set_printoptions(precision=2)
    #
    # # Plot non-normalized confusion matrix
    # plt.figure()
    # plot_confusion_matrix(cnf_matrix, classes=class_names, title='Confusion matrix, without normalization')
    #
    # # Plot normalized confusion matrix
    # plt.figure()
    # plot_confusion_matrix(cnf_matrix, classes=class_names, normalize=True, title='Normalized confusion matrix')
    #
    # plt.show()
    print(classification_report(y_test, predictions))
    print("Classification done")




runPredictionModel("poly_mo")
#drunPredictionModel("poly_mo")

