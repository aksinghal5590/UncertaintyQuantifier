import csv
import statistics

#This function iterates over quant_bootstrap.tsv and creates a map for confidence interval for each transcript
def evaluateCI(inputDir):
    trCIMap = dict()
    with open('input/' + inputDir + '/quant_bootstraps.tsv') as tsv:
        for column in zip(*[line for line in csv.reader(tsv, dialect="excel-tab")]):
            bootstrapData = list(column)
            trID = bootstrapData.pop(0)
            bootstrapData = [float(x) for x in bootstrapData]
            mean = statistics.mean(bootstrapData)
            sd = statistics.stdev(bootstrapData, xbar=mean)
            trCIMap[trID] = (mean - 2*sd), (mean + 2*sd)
    return trCIMap

#This is a utilty function is calculate mean and standard deviation of each column.
def get_mean_sd(inputDir):
    txp_mean_sd_map = dict()
    with open('input/'+inputDir + '/quant_bootstraps.tsv') as tsv:
        for column in zip(*[line for line in csv.reader(tsv, dialect="excel-tab")]):
            bootstrapData = list(column)
            trID = bootstrapData.pop(0)
            bootstrapData = [float(x) for x in bootstrapData]
            mean = statistics.mean(bootstrapData)
            sd = statistics.stdev(bootstrapData, xbar=mean)
            txp_mean_sd_map[trID] = mean, sd
    return txp_mean_sd_map


#This function iterates over quant_bootstrap.tsv and creates a map for confidence interval for each transcript
def evaluateCI_new_quant(inputDir):
    trCIMap = dict()
    with open('output/quant_bootstraps_new.tsv') as tsv:
        for column in zip(*[line for line in csv.reader(tsv, dialect="excel-tab")]):
            bootstrapData = list(column)
            trID = bootstrapData.pop(0)
            bootstrapData = [float(x) for x in bootstrapData]
            mean = statistics.mean(bootstrapData)
            sd = statistics.stdev(bootstrapData, xbar=mean)
            trCIMap[trID] = (mean - 2*sd), (mean + 2*sd)
    return trCIMap