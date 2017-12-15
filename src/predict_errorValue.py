
from sklearn.preprocessing import StandardScaler
import pandas as pd
import ParseEQ_Class
import pickle
import predict
import EvaluateCIFromBootstrap
import csv

import warnings
warnings.filterwarnings("ignore")

def unique_map(inputDir):
    uniquely_mapped_tr_list = []
    weight_map = dict()
    trEQMap = ParseEQ_Class.parseEQClass(inputDir)
    for tr in trEQMap.keys():
        eq_tuple = trEQMap[tr]
        if eq_tuple[1] == 1:
            if eq_tuple[2] == 1:
                uniquely_mapped_tr_list.append(tr)
    for tr in trEQMap.keys():
        weight_map[tr] = trEQMap[tr][3]
    return uniquely_mapped_tr_list,weight_map


def predict_error_value(inputDir):   
    predictions = predict.runPredictionModel(inputDir)
    print("Predicting Error values for faulty transcripts..................................................................................................")
    test_dataframe = pd.read_csv("bin/quant_new_" + inputDir + ".csv", sep="\t")
    se = pd.Series(predictions)
    test_dataframe['FaultyPredicted'] = se.values
    test_dataframe = test_dataframe.loc[test_dataframe.FaultyPredicted == 1]
    test_dataframe = test_dataframe.drop('FaultyPredicted', axis=1)
    test_dataframe["Length"] = test_dataframe["Length"].astype(int)
    test_dataframe["EffectiveLength"] = test_dataframe["EffectiveLength"].astype(int)
    test_dataframe["TPM"] = test_dataframe["TPM"].astype(int)
    test_dataframe["NumReads"] = test_dataframe["NumReads"].astype(int)
    test_dataframe.to_csv("bin/quant_new_regr_testing" + inputDir + ".csv", sep="\t", index=False)
    unique, weight = unique_map(inputDir)
    mean_sd_map = EvaluateCIFromBootstrap.get_mean_sd(inputDir)
    v = open("bin/quant_new_regr_testing" + inputDir + ".csv", "r")
    r = csv.reader(v, delimiter="\t")
    write = open("bin/quant_rtesting_" + inputDir + ".csv", "w")
    writer = csv.writer(write, dialect='excel', delimiter='\t', quoting=csv.QUOTE_ALL)
    for row in r:
        tr = row[0].split('\t')[0]
        # if tr != "Name":
            # if tr in mean_sd_map.keys():
            #     row.append(mean_sd_map[tr][0])
            #     row.append((mean_sd_map[tr][1])**2)
            # if tr in unique:
            #     row.append(1)
            # else:
            #     row.append(0)
        # else:
        #     row.append("Mean")
        #     row.append("Variance")
            # row.append("Truth_val")
            # row.append("Unique_maps")
        writer.writerow(row)
    v.close()
    write.close()

    df_test = pd.read_csv("bin/quant_rtesting_" + inputDir + ".csv", sep="\t")
    df2 = df_test
    df_test = df_test.drop('Name', axis=1)
    df_test.to_csv("bin/testing_data_" + inputDir + ".csv", sep="\t", index=False)
    X_test = df_test
    scaler = StandardScaler()
    scaler.fit(X_test)
    X_test = scaler.transform(X_test)
    filename = 'src/'+'Regression_model.sav'
    regr = pickle.load(open(filename, 'rb'))
    predictions = regr.predict(X_test)
    df2 = df2[['Name','NumReads','Mean']]
    se2 = pd.Series(predictions)
    df2['Predicted_ErrorValue'] = se2.values
    df2.to_csv("bin/pred_errorValue_" + inputDir + ".csv", sep="\t", index=False)
    print("Error values predicted.")

# predict_error_value("poly_mo")

