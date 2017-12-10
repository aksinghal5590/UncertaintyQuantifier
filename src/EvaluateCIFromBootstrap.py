import csv
import statistics

def evaluateCI(inputDir):
    trCIMap = dict()
    with open('../input/' + inputDir + '/quant_bootstraps.tsv') as tsv:
        for column in zip(*[line for line in csv.reader(tsv, dialect="excel-tab")]):
            bootstrapData = list(column)
            trID = bootstrapData.pop(0)
            bootstrapData = [float(x) for x in bootstrapData]
            mean = statistics.mean(bootstrapData)
            sd = statistics.stdev(bootstrapData, xbar=mean)
            trCIMap[trID] = (mean - 2*sd), (mean + 2*sd)
    return trCIMap


def get_mean_sd(inputDir):
    txp_mean_sd_map = dict()
    with open('../input/' + inputDir + '/quant_bootstraps.tsv') as tsv:
        for column in zip(*[line for line in csv.reader(tsv, dialect="excel-tab")]):
            bootstrapData = list(column)
            trID = bootstrapData.pop(0)
            bootstrapData = [float(x) for x in bootstrapData]
            mean = statistics.mean(bootstrapData)
            sd = statistics.stdev(bootstrapData, xbar=mean)
            txp_mean_sd_map[trID] = mean, sd
    return txp_mean_sd_map
