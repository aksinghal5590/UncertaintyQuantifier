
from sklearn.preprocessing import StandardScaler
import pandas as pd
import ParseEQ_Class
import pickle
import predict
import EvaluateCIFromBootstrap
from sklearn.metrics import r2_score
import csv

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

def error(inputDir):
    lineCount2 = 0
    truthMap = dict()
    for line in open(inputDir+'/poly_truth.tsv'):
        lineCount2 += 1
        if lineCount2 == 1:
            continue
        data = line.split('\t')
        truthMap[data[0]] = int(data[1])
    return truthMap

def predict_error_value(inputDir):
    predictions = predict.runPredictionModel(inputDir)
    test_dataframe = pd.read_csv("bin/quant_new_" + inputDir + ".csv", sep="\t")
    se = pd.Series(predictions)
    test_dataframe['FaultyPredicted'] = se.values
    test_dataframe = test_dataframe.loc[test_dataframe.FaultyPredicted == 1]
    test_dataframe = test_dataframe.drop('FaultyPredicted', axis=1)
    test_dataframe["Length"] = test_dataframe["Length"].astype(int)
    test_dataframe["EffectiveLength"] = test_dataframe["EffectiveLength"].astype(int)
    test_dataframe["TPM"] = test_dataframe["TPM"].astype(int)
    test_dataframe["NumReads"] = test_dataframe["NumReads"].astype(int)
    test_dataframe["ErrorFraction"] = test_dataframe["ErrorFraction"].astype(int)
    test_dataframe.to_csv("bin/quant_new_regr_testing" + inputDir + ".csv", sep="\t", index=False)

    truth_value = error(inputDir)
    unique, weight = unique_map(inputDir)
    mean_sd_map = EvaluateCIFromBootstrap.get_mean_sd(inputDir)
    v = open("bin/quant_new_regr_testing" + inputDir + ".csv", "r")
    r = csv.reader(v, delimiter="\t")
    write = open("bin/quant_rtesting_" + inputDir + ".csv", "w")
    writer = csv.writer(write, dialect='excel', delimiter='\t', quoting=csv.QUOTE_ALL)
    for row in r:
        tr = row[0].split('\t')[0]
        if tr != "Name":
            if tr in mean_sd_map.keys():
                row.append(mean_sd_map[tr][0])
                row.append((mean_sd_map[tr][1])**2)
            if tr in truth_value.keys():
                row.append(truth_value[tr])
            else:
                row.append(0)
            if tr in unique:
                row.append(1)
            else:
                row.append(0)
        else:
            row.append("Mean")
            row.append("Variance")
            row.append("Truth_val")
            row.append("Unique_maps")
        writer.writerow(row)
    v.close()
    write.close()

    df_test = pd.read_csv("bin/quant_rtesting_" + inputDir + ".csv", sep="\t")
    df_test['error'] = df_test["Truth_val"] - df_test["Mean"]
    df_test = df_test.drop('Truth_val', axis=1)
    df_test = df_test.drop('Length',axis=1)
    df_test = df_test.drop('EffectiveLength',axis=1)
    df_test = df_test.drop('ErrorFraction',axis=1)
    df_test = df_test.drop('Faulty',axis=1)
    df_test = df_test.drop('UniqueMap',axis=1)
    # df = df.drop('Unique_maps',axis=1)
    df2 = df_test
    df_test = df_test.drop('Name', axis=1)
    #df_test = df_test.drop('Mean', axis=1)
    df_test.to_csv("bin/testing_data_" + inputDir + ".csv", sep="\t", index=False)
    X_test = df_test.drop('error', axis=1)
    scaler = StandardScaler()
    scaler.fit(X_test)
    X_test = scaler.transform(X_test)
    y_test = df_test['error']

    filename = 'Regression_model.sav'
    regr = pickle.load(open(filename, 'rb'))
    predictions = regr.predict(X_test)
    #df2 = df2.drop('Mean',axis=1)
    #df2 = df2.drop('error',axis=1)
    df2 = df2[['Name','NumReads','Mean','error']]
    print(r2_score(y_test, predictions))
    se2 = pd.Series(predictions)
    df2['Predicted_ErrorValue'] = se2.values
    df2.to_csv("bin/pred_errorValue_" + inputDir + ".csv", sep="\t", index=False)
    print("Testing Done")

# predict_error_value("poly_mo")
