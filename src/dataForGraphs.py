import FaultyTranscriptFilter
import pandas as pd

def get_FaultyTranscriptError_CSV():
    faultyList = FaultyTranscriptFilter.filterFaultyTranscripts()
    lineCount = 0
    lineCount1 = 0
    truthMap = dict()
    quantMap = dict()
    for line in open('input/poly_truth.tsv'):
        lineCount += 1
        if lineCount == 1:
            continue
        data = line.split('\t')
        if data[0] in faultyList:
            truthMap[data[0]] = int(data[1])
    for line in open('input/quant.sf'):
        lineCount1 += 1
        if lineCount1 == 1:
            continue
        data1 = line.split('\t')
        if data1[0] in faultyList:
            value = data1[4]
            numReads = float(value[:-1])
            quantMap[data1[0]] = numReads

    resultMap = dict()
    for x in truthMap.keys():
        truthValue = truthMap.get(x)
        quantValue = quantMap.get(x)
        if(truthValue is None or quantValue is None):
            continue
        errorFraction = (truthValue - quantValue)/truthValue
        resultMap[x] = errorFraction
    df = pd.DataFrame(list(resultMap.items()), columns=['TranscriptID', 'ErrorFraction'])
    df.to_csv("bin/errorFraction_faulty.csv", encoding='utf-8')

def get_AllTrancriptsError_CSV(inputDir):
    lineCount2 = 0
    lineCount3 = 0
    truthMap = dict()
    quantMap = dict()
    for line in open('input/' + inputDir + '/poly_truth.tsv'):
        lineCount2 += 1
        if lineCount2 == 1:
            continue
        data = line.split('\t')
        truthMap[data[0]] = int(data[1])
    for line in open('input/' + inputDir + '/quant.sf'):
        lineCount3 += 1
        if lineCount3 == 1:
            continue
        data1 = line.split('\t')
        value = data1[4]
        numReads = float(value[:-1])
        quantMap[data1[0]] = numReads

    resultMap = dict()
    for x in truthMap.keys():
        truthValue = truthMap.get(x)
        quantValue = quantMap.get(x)
        if (truthValue is None or quantValue is None):
            continue
        errorFraction = (truthValue - quantValue) / truthValue
        resultMap[x] = errorFraction
    return resultMap


