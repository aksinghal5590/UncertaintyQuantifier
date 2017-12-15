from sklearn.preprocessing import StandardScaler
import pandas as pd
from sklearn import svm
from pathlib import Path
import ParseEQ_Class
import pickle
import EvaluateCIFromBootstrap

# This function is used to create classification model which will be used to predict faulty transcripts.
def train_model(inputDir):
    if Path("bin/quant_new_poly_mo.csv").is_file() == False:
        ParseEQ_Class.getUniqueAndAmbiguousMaps("poly_mo")
    train_dataframe1 = pd.read_csv("bin/quant_new_poly_mo.csv", sep="\t")
    if Path("bin/quant_new_poly_ro.csv").is_file() == False:
        ParseEQ_Class.getUniqueAndAmbiguousMaps("poly_ro")
    train_dataframe2 = pd.read_csv("bin/quant_new_poly_ro.csv",sep="\t")
    train_dataframe = pd.concat([train_dataframe1,train_dataframe2], axis=0)
    train_dataframe["Length"] = train_dataframe["Length"].astype(int)
    train_dataframe["EffectiveLength"] = train_dataframe["EffectiveLength"].astype(int)
    train_dataframe["TPM"] = train_dataframe["TPM"].astype(int)
    train_dataframe["NumReads"] = train_dataframe["NumReads"].astype(int)
    # train_dataframe["ErrorFraction"] = train_dataframe["ErrorFraction"].astype(int)
    train_dataframe["Mean"] = train_dataframe["Mean"].astype(int)
    train_dataframe["Variance"] = train_dataframe["Variance"].astype(int)
    print(train_dataframe.shape)
    print("Classification started")
    train_dataframe = train_dataframe.drop('Name', axis=1)
    train_dataframe = train_dataframe.drop('Weight', axis=1)
    # train_dataframe = train_dataframe.drop('ErrorFraction', axis=1)


    X = train_dataframe.drop('Faulty', axis=1)
    y = train_dataframe['Faulty']

    X_train = X
    y_train = y
    scaler = StandardScaler()
    scaler.fit(X_train)
    print("Training data fitted")
    X_train = scaler.transform(X_train)

    clf = svm.SVC(gamma=0.001, C=500)
    clf.fit(X_train, y_train)
    filename = 'src/training_model.sav'
    pickle.dump(clf, open(filename, 'wb'))
    print("Training done")


train_model("poly_mo")
