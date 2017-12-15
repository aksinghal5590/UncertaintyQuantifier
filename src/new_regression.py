import FaultyTranscriptFilter
import pandas as pd
from pathlib import Path
import ParseEQ_Class
import EvaluateCIFromBootstrap
import csv
import pickle
from sklearn.preprocessing import StandardScaler
from sklearn import linear_model

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
    for line in open('input/'+inputDir+'/poly_truth.tsv'):
        lineCount2 += 1
        if lineCount2 == 1:
            continue
        data = line.split('\t')
        truthMap[data[0]] = int(data[1])
    return truthMap

def train_model(inputDir):
    faultyList = FaultyTranscriptFilter.filterFaultyTranscripts(inputDir)
    if Path("bin/quant_new_" + inputDir + ".csv").is_file() == False:
        ParseEQ_Class.getUniqueAndAmbiguousMaps(inputDir)
    train_dataframe = pd.read_csv("bin/quant_new_" + inputDir + ".csv",sep="\t")
    print(train_dataframe.shape)
    train_dataframe=train_dataframe.loc[train_dataframe['Name'].isin(faultyList)]
    # print(train_dataframe)
    print(train_dataframe.shape)
    train_dataframe["Length"] = train_dataframe["Length"].astype(int)
    train_dataframe["EffectiveLength"] = train_dataframe["EffectiveLength"].astype(int)
    train_dataframe["TPM"] = train_dataframe["TPM"].astype(int)
    train_dataframe["NumReads"] = train_dataframe["NumReads"].astype(int)
    # train_dataframe["ErrorFraction"] = train_dataframe["ErrorFraction"].astype(int)
    train_dataframe = train_dataframe[train_dataframe.TPM != 0]

    train_dataframe.to_csv("bin/quant_new_regr_" + inputDir + ".csv",sep="\t",index=False)
    truth_value = error(inputDir)
    unique, weight = unique_map(inputDir)
    mean_sd_map = EvaluateCIFromBootstrap.get_mean_sd(inputDir)
    v = open("bin/quant_new_regr_" + inputDir + ".csv", "r")
    r = csv.reader(v, delimiter="\t")
    write = open("bin/quant_rtraining_" + inputDir + ".csv", "w")
    writer = csv.writer(write, dialect='excel', delimiter='\t', quoting=csv.QUOTE_ALL)
    for row in r:
        tr = row[0].split('\t')[0]
        if tr != "Name":
            # if tr in mean_sd_map.keys():
            #     row.append(mean_sd_map[tr][0])
            #     row.append((mean_sd_map[tr][1])**2)
            if tr in truth_value.keys():
                row.append(truth_value[tr])
            else:
                row.append(0)
            # if tr in unique:
            #     row.append(1)
            # else:
            #     row.append(0)
        else:
            # row.append("Mean")
            # row.append("Variance")
            row.append("Truth_val")
            # row.append("Unique_maps")
        writer.writerow(row)
    v.close()
    write.close()

    print("Done making file")
    df = pd.read_csv("bin/quant_rtraining_" + inputDir + ".csv", sep="\t")

    df['error'] = df["Truth_val"] - df["Mean"]
    print(df)
    df = df.drop('Truth_val', axis=1)
    df = df.drop('Name', axis=1)
    df = df.drop('Faulty', axis=1)
    # df = df.drop('UniqueMap', axis=1)
    # df = df.drop('ErrorFraction', axis=1)
    # df = df.drop('Length',axis=1)
    # df = df.drop('EffectiveLength',axis=1)
    # df = df.drop('Unique_maps',axis=1)
    #df = df.drop('Mean', axis=1)
    X = df.drop('error', axis=1)
    df.to_csv("bin/training_data_" + inputDir + ".csv", sep="\t", index=False)
    y = df['error']

    X_train = X
    y_train = y
    scaler = StandardScaler()
    scaler.fit(X_train)
    print("Training data fitted")
    X_train = scaler.transform(X_train)
    # X_test = scaler.transform(X_test)

    regr = linear_model.LinearRegression()
    regr.fit(X_train, y_train)
    filename = 'src/Regression_model.sav'
    pickle.dump(regr, open(filename, 'wb'))
    print("Training done")

train_model("poly_mo")
