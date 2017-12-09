from src import EvaluateCIFromBootstrap


def filterFaultyTranscripts(inputDir):
    ciMap = EvaluateCIFromBootstrap.evaluateCI(inputDir)
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


