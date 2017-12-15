
from sklearn.metrics import confusion_matrix, classification_report
from sklearn.preprocessing import StandardScaler
import pandas as pd
from pathlib import Path
import ParseEQ_Class
import pickle

import warnings
warnings.filterwarnings("ignore")

#This function predicts the number of faulty transcripts in a dataset using the trained model.
def  runPredictionModel(inputDir):
    print("Predicting Faulty Transcripts...................................................................................................................")
    if Path("bin/quant_new_" + inputDir + ".csv").is_file() == False:
        ParseEQ_Class.getUniqueAndAmbiguousMaps_predicted(inputDir)
    test_dataframe = pd.read_csv("bin/quant_new_" + inputDir + ".csv", sep="\t")
    test_dataframe["Length"] = test_dataframe["Length"].astype(int)
    test_dataframe["EffectiveLength"] = test_dataframe["EffectiveLength"].astype(int)
    test_dataframe["TPM"] = test_dataframe["TPM"].astype(int)
    test_dataframe["NumReads"] = test_dataframe["NumReads"].astype(int)
    #test_dataframe = test_dataframe[test_dataframe.TPM != 0]

    print("Classification started")
    test_dataframe = test_dataframe.drop('Name', axis=1)
    test_dataframe = test_dataframe.drop('Weight', axis=1)

    X_test = test_dataframe
    scaler = StandardScaler()
    scaler.fit(X_test)
    X_test = scaler.transform(X_test)
    filename = 'src/' + 'training_model.sav'
    clf = pickle.load(open(filename, 'rb'))
    predictions = clf.predict(X_test)
    print("Classification done")
    # print(len(predictions))
    count = 0
    for pre in predictions:
        if pre:
            count += 1
    # print("Faulty Transcripts predicted:",count)
    print("Processing to reduce the faulty transcripts count...............................................................................................")
    #print(predictions[1])
    return predictions

# runPredictionModel("poly_mo")
