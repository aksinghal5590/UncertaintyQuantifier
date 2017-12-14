
def getErrorFractionAll():
    lineCount = 0
    errorMap = dict()
    for line in open('input/errorFraction_all.csv'):
        lineCount += 1
        if lineCount == 1:
            continue
        data = line.split(',')
        print(len(data))
        errorMap[data[1]] = data[2]
    return errorMap

def getErrorFractionFaulty():
    lineCount=0
    errorMap = dict()
    for line in open('input/errorFraction_faulty.csv'):
        lineCount+=1
        if lineCount ==1:
            continue
        data = line.split(',')
        print(len(data))
        errorMap[data[1]] = data[2]
    return errorMap

def createFaultyTranscriptCSV():
    lineCount =0
    faultyMap = dict()
    download_dir = "input/faultyTrData.csv"
    csv = open(download_dir, "w")
    columnTitleRow = "ID,Length,EffectiveLength,TPM,NumReads,Weight\n"
    csv.write(columnTitleRow)
    for line in open('input/quant_new.csv'):
        lineCount += 1
        if lineCount == 1:
            continue
        if lineCount%2 ==0:
            continue
        print(line)
        data = line.split('\t')
        print(len(data))
        if data[7]=='"1"\n':
            ID = data[0]
            length = data[1]
            effectiveLength = data[2]
            tpm = data[3]
            numReads = data[4]
            weight = data[6]
            row = ID + "," + length + ","+effectiveLength+","+tpm+","+numReads+","+weight+"\n"
            csv.write(row)

#createFaultyTranscriptCSV()



