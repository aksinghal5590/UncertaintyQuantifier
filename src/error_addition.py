import pandas as pd
import csv
import statistics

def error_addition(inputDir):
    # predict_errorValue.predict_error_value(inputDir)
    print("I am in")
    df1 = pd.read_csv("../bin/testing_data_" + inputDir + ".csv", sep="\t")
    df2 = pd.read_csv("../bin/pred_errorValue_" + inputDir + ".csv", sep="\t")
    # print(df1["StandardDeviation"],df2["Predicted_ErrorValue"])
    # df2["Diff1"] = abs(df2["Predicted_ErrorValue"]) - (1*df1["StandardDeviation"])
    # print(x)
    i = 0
    for err in df2["Predicted_ErrorValue"]:
        if err < 0:
            df2.ix[i,"Diff"] = df2.ix[i,"Mean"] - (df2.ix[i,"Predicted_ErrorValue"])*(0.45)
        if err > 0:
            df2.ix[i,"Diff"] = df2.ix[i,"Mean"] + (df2.ix[i,"Predicted_ErrorValue"])*(0.45)
        i+=1
    print(df2, df1["Variance"])
    names = df2["Name"].tolist()
    # print(df2["Diff"])

    trCIMap = dict()
    with open('../input/' + inputDir + '/quant_bootstraps.tsv') as tsv:
        for column in zip(*[line for line in csv.reader(tsv, dialect="excel-tab")]):
            bootstrapData = list(column)
            trID = bootstrapData.pop(0)
            bootstrapData = [float(x) for x in bootstrapData]
            mean = statistics.mean(bootstrapData)
            mean1 = mean
            sd = statistics.stdev(bootstrapData, xbar=mean)
            if trID in names:
                loc = names.index(trID)
                # print(loc)
                mean = df2.ix[loc,'Diff']
                # if mean1 != mean:
                    # print(mean)
            trCIMap[trID] = (mean - 2*sd), (mean + 2*sd)
    ciMap = trCIMap
    lineCount = 0
    faultyTr = list()
    for line in open('../input/' + inputDir + '/poly_truth.tsv'):
        lineCount += 1
        if lineCount == 1:
            continue
        data = line.split('\t')
        if data[0] in ciMap:
            ciTuple = ciMap[data[0]]
            if (float(data[1]) < ciTuple[0]) or (float(data[1]) > ciTuple[1]):
                tuple = data[0]
                faultyTr.append(tuple)

    print(len(faultyTr))

    data_frame = pd.read_csv('../input/' + inputDir + '/quant_bootstraps.tsv', sep='\t')
    new_names = list(data_frame.columns.values)
    for name in new_names:
        if name in names:
            loc = names.index(name)
            data_frame[name] += df2.ix[loc,"Diff1"]
    data_frame.to_csv('../input/' + inputDir + '/quant_bootstraps_new.tsv', sep='\t',index=False)
    print("Done")


print("Hello")
error_addition("poly_mo")
