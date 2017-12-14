import EvaluateCIFromBootstrap

#This function filters faulty transcripts by comparing mean values with poly truth value. Hence giving the
#actual count of faulty transcripts
def filterFaultyTranscripts(inputDir):
    ciMap = EvaluateCIFromBootstrap.evaluateCI(inputDir)
    lineCount = 0
    faultyTr = list()
    for line in open('input/' + inputDir + '/poly_truth.tsv'):
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


def get_faulty_txp_class(inputDir):
    ciMap = EvaluateCIFromBootstrap.get_mean_sd(inputDir)
    lineCount = 0
    faulty_txp_class = dict()
    for line in open(inputDir + '/poly_truth.tsv'):
        lineCount += 1
        if lineCount == 1:
            continue
        data = line.split('\t')
        txp_id = data[0]
        if txp_id in ciMap:
            mean = ciMap[txp_id][0]
            sd = ciMap[txp_id][1]
            if (float(data[1]) < (mean - 2*sd)):
                faulty_txp_class[txp_id] = -1
            elif (float(data[1]) > (mean + 2*sd)):
                faulty_txp_class[txp_id] = 1
            else:
                faulty_txp_class[txp_id] = 0
        else:
            faulty_txp_class[txp_id] = 0
    return faulty_txp_class