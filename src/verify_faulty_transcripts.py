import EvaluateCIFromBootstrap
import sys

#This function filters faulty transcripts by comparing mean values with poly truth value. Hence giving the
#actual count of faulty transcripts
def filterFaultyTranscripts(inputDir):
    print("Counting faulty Transcripts in new quant_bootstrap.tsv.......................................................................................... ")
    ciMap = EvaluateCIFromBootstrap.evaluateCI_new_quant(inputDir)
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
    print("Faulty Transcripts Count in the new file:",len(faultyTr))
    print("Process finished.")

filterFaultyTranscripts(sys.argv[1])