from src import FaultyTranscriptFilter


def createTPMMap(inputDir):
    lineCount = 0
    tpmMap = dict()
    for line in open('input/' + inputDir + '/quant.sf'):
        lineCount += 1
        if lineCount == 1:
            continue
        data = line.split('\t')
        tpmMap[data[0]] = float(data[3])
    return tpmMap


def checkTPM(inputDir):
    faultyTr = FaultyTranscriptFilter.filterFaultyTranscripts(inputDir)
    tpmMap = createTPMMap(inputDir)
    max = 0
    maxtuple = {}
    for tuple in faultyTr:
        if max < tpmMap[tuple[0]]:
            max = tpmMap[tuple[0]]
            maxtuple = tuple
    return maxtuple