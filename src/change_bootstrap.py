

from src import predict
import pandas as pd
import statistics
import csv
import sys
from pathlib import Path

def get_mean_sd(inputDir):
    txp_mean_sd_map = dict()
    with open('../input/' + inputDir + '/quant_bootstraps.tsv') as tsv:
        for column in zip(*[line for line in csv.reader(tsv, dialect="excel-tab")]):
            bootstrapData = list(column)
            trID = bootstrapData.pop(0)
            bootstrapData = [float(x) for x in bootstrapData]
            mean = statistics.mean(bootstrapData)
            sd = statistics.stdev(bootstrapData, xbar=mean)
            list1 = []
            list1.append(mean)
            list1.append(sd)
            list1.append(0)
            txp_mean_sd_map[trID]=list1
    return txp_mean_sd_map

def filterFaultyTranscripts(inputDir,ciMap):
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
    return faultyTr

def change_mean_check(inputDir):
    if Path("../bin/change_bootstrap_" + inputDir + ".csv").is_file() == False:
        predictions = predict.runPredictionModel(inputDir)
        test_dataframe = pd.read_csv("../bin/quant_new_" + inputDir + ".csv", sep="\t")
        print(predictions)
        se = pd.Series(predictions)
        test_dataframe['FaultyPredicted'] = se.values
        df2 = test_dataframe[['Name','FaultyPredicted']]
        df2.to_csv("../bin/change_bootstrap_" + inputDir + ".csv", sep="\t", index=False)
    df2 = pd.read_csv("../bin/change_bootstrap_" + inputDir + ".csv", sep="\t")
    df3 = df2.loc[df2.FaultyPredicted == 1]
    initial_count = df3.count
    print(initial_count)
    mean_sd_map =get_mean_sd(inputDir)
    new_mean_map = {}
    trCIMap = dict()
    for index, row in df2.iterrows():
        trID = row["Name"]
        if(trID) in mean_sd_map.keys():
            old_mean = mean_sd_map[trID][0]
            sd = mean_sd_map[trID][1]
            if row["FaultyPredicted"] is True :
                new_mean = old_mean+0.5*old_mean
                count = mean_sd_map[trID][2]
                count2 = count+0.5*old_mean
                list2 = []
                list2.append(new_mean)
                list2.append(mean_sd_map[trID][1])
                list2.append(count2)
                new_mean_map[trID]= list2
                trCIMap[trID] = (new_mean - 2 * sd), (new_mean + 2 * sd)
            else:
                trCIMap[trID] = (old_mean - 2 * sd), (old_mean + 2 * sd)
    faultyTrList = filterFaultyTranscripts(inputDir,trCIMap)
    new_count = len(faultyTrList)
    print(new_count)

change_mean_check("poly_ro")
# def create_new_bootstrap(inputDir,faultyListPredicted,mean_sd_map):
#     with open('../input/' + inputDir + '/quant_bootstraps.tsv') as tsv:
#         for column in zip(*[line for line in csv.reader(tsv, dialect="excel-tab")]):
#             bootstrapData = list(column)
#             trID = bootstrapData.pop(0)
#             if trID in faultyListPredicted:
#                 error = mean_sd_map[trID][2]
#                 bootstrapData = [float(x+error) for x in bootstrapData]
#                 mean = statistics.mean(bootstrapData)
#                 sd = statistics.stdev(bootstrapData, xbar=mean)
#                 list1 = []
#                 list1.append(mean)
#                 list1.append(sd)
#                 list1.append(0)
#             txp_mean_sd_map[trID]=list1
#     return txp_mean_sd_map
#
#
# if __name__== "__main__":
#     if(len(sys.argv)>1):
#        change_mean_check(sys.argv[1])
#     else:
#        change_mean_check("poly_mo")
#
#
#
#
#
