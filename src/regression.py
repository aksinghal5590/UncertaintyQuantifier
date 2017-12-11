from sklearn.metrics import r2_score
from sklearn.preprocessing import StandardScaler
from sklearn.cross_validation import train_test_split
from sklearn import linear_model
import pandas as pd
import csv
import statistics

def evaluateCI():
    trCIMap = dict()
    print("hello")
    with open('../input/poly_mo/quant_bootstraps.tsv') as tsv:
        for column in zip(*[line for line in csv.reader(tsv, dialect="excel-tab")]):
            bootstrapData = list(column)
            trID = bootstrapData.pop(0)
            bootstrapData = [float(x) for x in bootstrapData]
            mean = statistics.mean(bootstrapData)
            sd = statistics.stdev(bootstrapData, xbar=mean)
            #print(trID)
            #print(mean)
            trCIMap[trID] = [mean,sd]
    return trCIMap

def evaluateCI2():
    trCIMap = dict()
    print("hello")
    with open('../input/poly_ro/quant_bootstraps.tsv') as tsv:
        for column in zip(*[line for line in csv.reader(tsv, dialect="excel-tab")]):
            bootstrapData = list(column)
            trID = bootstrapData.pop(0)
            bootstrapData = [float(x) for x in bootstrapData]
            mean = statistics.mean(bootstrapData)
            sd = statistics.stdev(bootstrapData, xbar=mean)
            #print(trID)
            #print(mean)
            trCIMap[trID] = [mean,sd]
    return trCIMap

def error():
    lineCount2 = 0
    truthMap = dict()
    for line in open('../input/poly_mo/poly_truth.tsv'):
        lineCount2 += 1
        if lineCount2 == 1:
            continue
        data = line.split('\t')
        truthMap[data[0]] = int(data[1])
    return truthMap

def error2():
    lineCount2 = 0
    truthMap = dict()
    for line in open('../input/poly_ro/poly_truth.tsv'):
        lineCount2 += 1
        if lineCount2 == 1:
            continue
        data = line.split('\t')
        truthMap[data[0]] = int(data[1])
    return truthMap

def parseEQClass():
    trCount = 0
    lineCount = 0
    trMap = dict()
    trEqMap = dict()
    i = 0
    j = 0
    for line in open('../input/poly_mo/eq_classes.txt'):
        lineCount += 1
        if(lineCount == 1):
            trCount = int(line)
            continue
        if(lineCount == 2):
            continue
        if(i < trCount):
            trMap[i] = line[:-1]
            i += 1
            continue
        val = line.split("\t")
        for tr_id in val[1:-1]:
            eq_tuple = []
            if trMap[int(tr_id)] in trEqMap.keys():
                eq_tuple = trEqMap[trMap[int(tr_id)]]
                val1 = eq_tuple[0] + int(val[len(val) - 1][:-1])
                val2 = eq_tuple[1] + 1
                val3 = eq_tuple[2] + int(val[0])
                if int(val[0]) == 1:
                    eq_tuple[3] = 0
                eq_tuple[0] = val1
                eq_tuple[1] = val2
                eq_tuple[2] = val3
            else:
                eq_tuple.append(int(val[len(val) - 1][:-1]))
                eq_tuple.append(1)
                eq_tuple.append(int(val[0]))
                if int(val[0]) == 1:
                    eq_tuple.append(1)
                else:
                    eq_tuple.append(-1)
            trEqMap[trMap[int(tr_id)]] = eq_tuple
    return trEqMap

def parseEQClass2():
    trCount = 0
    lineCount = 0
    trMap = dict()
    trEqMap = dict()
    i = 0
    j = 0
    for line in open('../input/poly_ro/eq_classes.txt'):
        lineCount += 1
        if(lineCount == 1):
            trCount = int(line)
            continue
        if(lineCount == 2):
            continue
        if(i < trCount):
            trMap[i] = line[:-1]
            i += 1
            continue
        val = line.split("\t")
        for tr_id in val[1:-1]:
            eq_tuple = []
            if trMap[int(tr_id)] in trEqMap.keys():
                eq_tuple = trEqMap[trMap[int(tr_id)]]
                val1 = eq_tuple[0] + int(val[len(val) - 1][:-1])
                val2 = eq_tuple[1] + 1
                val3 = eq_tuple[2] + int(val[0])
                if int(val[0]) == 1:
                    eq_tuple[3] = 0
                eq_tuple[0] = val1
                eq_tuple[1] = val2
                eq_tuple[2] = val3
            else:
                eq_tuple.append(int(val[len(val) - 1][:-1]))
                eq_tuple.append(1)
                eq_tuple.append(int(val[0]))
                if int(val[0]) == 1:
                    eq_tuple.append(1)
                else:
                    eq_tuple.append(-1)
            trEqMap[trMap[int(tr_id)]] = eq_tuple
    return trEqMap

def unique_map():
    uniquely_mapped_tr_list = []
    weight_map = dict()
    trEQMap = parseEQClass()
    for tr in trEQMap.keys():
        eq_tuple = trEQMap[tr]
        if eq_tuple[1] == 1:
            if eq_tuple[2] == 1:
                uniquely_mapped_tr_list.append(tr)
    for tr in trEQMap.keys():
        weight_map[tr] = trEQMap[tr][3]
    return uniquely_mapped_tr_list,weight_map

def unique_map2():
    uniquely_mapped_tr_list = []
    weight_map = dict()
    trEQMap = parseEQClass2()
    for tr in trEQMap.keys():
        eq_tuple = trEQMap[tr]
        if eq_tuple[1] == 1:
            if eq_tuple[2] == 1:
                uniquely_mapped_tr_list.append(tr)
    for tr in trEQMap.keys():
        weight_map[tr] = trEQMap[tr][3]
    return uniquely_mapped_tr_list,weight_map

mean_sd = evaluateCI()
err = error()
unique, weight = unique_map()
v = open("../input/poly_mo/quant.tsv","r")
r = csv.reader(v,delimiter="\t")
write = open("../bin/quant_training.csv", "w")
writer = csv.writer(write,dialect='excel',delimiter='\t',quoting=csv.QUOTE_ALL)
for row in r:
    tr = row[0].split('\t')[0]
    if tr != "Name":
        if tr in mean_sd.keys():
            row.append(mean_sd[tr][0])
            row.append(mean_sd[tr][1])
        if tr in err.keys():
            row.append(err[tr])
        else:
            row.append(0)
        if tr in weight.keys():
            row.append(weight[tr])
        else:
            row.append(0)
        if tr in unique:
            row.append(1)
        else:
            row.append(0)
    else:
        row.append("Mean")
        row.append("Std_deviation")
        row.append("Truth_val")
        row.append("Weight")
        row.append("Unique_maps")
    writer.writerow(row)
v.close()
write.close()

mean_sd= evaluateCI2()
err = error2()
unique, weight = unique_map2()
v = open("../input/poly_ro/quant.tsv","r")
r = csv.reader(v,delimiter="\t")
write = open("../bin/quant_testing.csv", "w")
writer = csv.writer(write,dialect='excel',delimiter='\t',quoting=csv.QUOTE_ALL)
for row in r:
    tr = row[0].split('\t')[0]
    if tr != "Name":
        if tr in mean_sd.keys():
            row.append(mean_sd[tr][0])
            row.append(mean_sd[tr][1])
        if tr in err.keys():
            row.append(err[tr])
        else:
            row.append(0)
        if tr in weight.keys():
            row.append(weight[tr])
        else:
            row.append(0)
        if tr in unique:
            row.append(1)
        else:
            row.append(0)
    else:
        row.append("Mean")
        row.append("Std_deviation")
        row.append("Truth_val")
        row.append("Weight")
        row.append("Unique_maps")
    writer.writerow(row)
v.close()
write.close()

df = pd.read_csv("../bin/quant_training.csv",sep="\t")

df['error'] = df["Truth_val"] - df["Mean"]
df = df.drop('Truth_val',axis=1)
df = df.drop('Name',axis=1)
#df = df.drop('Unique_maps',axis=1)
df = df.drop('Mean',axis=1)
df = df.drop('Std_deviation',axis=1)
X = df.drop('error', axis=1)
y = df['error']

#X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.01)
X_train = X
y_train = y
scaler = StandardScaler()
scaler.fit(X_train)
print("Training data fitted")
X_train = scaler.transform(X_train)
#X_test = scaler.transform(X_test)

df_test = pd.read_csv("../bin/quant_testing.csv",sep="\t")
df_test['error'] = df_test["Truth_val"] - df_test["Mean"]
df_test = df_test.drop('Truth_val',axis=1)
df_test = df_test.drop('Name',axis=1)
#df = df.drop('Unique_maps',axis=1)
df_test = df_test.drop('Mean',axis=1)
df_test = df_test.drop('Std_deviation',axis=1)
X_test = df_test.drop('error', axis=1)
scaler = StandardScaler()
scaler.fit(X_test)
X_test = scaler.transform(X_test)
y_test = df_test['error']

regr = linear_model.LinearRegression()
regr.fit(X_train,y_train)
predict = regr.predict(X_test)
#print(predict,y_test)
print(r2_score(y_test,predict))