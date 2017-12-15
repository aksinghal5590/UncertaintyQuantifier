import FaultyTranscriptFilter
import dataForGraphs
import csv
import EvaluateCIFromBootstrap

def parseEQClass(inputDir):
    trCount = 0
    lineCount = 0
    trMap = dict()
    trEqMap = dict()
    i = 0
    j = 0
    for line in open('input/' + inputDir + '/eq_classes.txt'):
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


def getUniqueAndAmbiguousMaps(inputDir):
    uniquely_mapped_tr_list = []
    weight_map = dict()
    faultyList = FaultyTranscriptFilter.filterFaultyTranscripts(inputDir)
    errorMap = dataForGraphs.get_AllTrancriptsError_CSV(inputDir)
    mean_sd = EvaluateCIFromBootstrap.get_mean_sd(inputDir)

    trEQMap = parseEQClass(inputDir)
    for tr in faultyList:
        if tr in trEQMap.keys():
            eq_tuple = trEQMap[tr]
            if eq_tuple[1] == 1:
                if eq_tuple[2] == 1:
                    uniquely_mapped_tr_list.append(tr)
    for tr in trEQMap.keys():
        weight_map[tr] = trEQMap[tr][3]

    print("EQ list length: ", len(trEQMap))
    print("Faulty list length: ", len(faultyList))
    print("Uniquely mapped faulty list length: ", len(uniquely_mapped_tr_list))

    v = open('input/' + inputDir + '/quant.sf',"r")
    r = csv.reader(v,delimiter="\t")
    write = open("bin/quant_new_" + inputDir + ".csv", "w")
    writer = csv.writer(write,dialect='excel',delimiter='\t',quoting=csv.QUOTE_ALL)
    for row in r:
        tr = row[0].split('\t')[0]
        if tr != "Name":
            # if tr in uniquely_mapped_tr_list:
            #     row.append(True)
            # else:
            #     row.append(False)
            if tr in mean_sd:
                row.append(mean_sd[tr][0])
            if tr in mean_sd:
                row.append((mean_sd[tr][1])**2)
            if tr in weight_map.keys():
                row.append(weight_map[tr])
            else:
                row.append(0)
            # if tr in errorMap.keys():
            #     row.append(errorMap[tr]*10000)
            # else:
            #     row.append(0)
            if tr in faultyList:
                row.append(True)
            else:
                row.append(False)
        else:
            # row.append("UniqueMap")
            row.append("Mean")
            row.append("Variance")
            row.append("Weight")
            # row.append("ErrorFraction")
            row.append("Faulty")
        writer.writerow(row)
    v.close()
    write.close()


def getUniqueAndAmbiguousMaps_predicted(inputDir):
    uniquely_mapped_tr_list = []
    weight_map = dict()
    mean_sd = EvaluateCIFromBootstrap.get_mean_sd(inputDir)

    trEQMap = parseEQClass(inputDir)
    for tr in trEQMap.keys():
        eq_tuple = trEQMap[tr]
        if eq_tuple[1] == 1:
            if eq_tuple[2] == 1:
                uniquely_mapped_tr_list.append(tr)

    for tr in trEQMap.keys():
        weight_map[tr] = trEQMap[tr][3]

    v = open('input/' + inputDir + '/quant.sf',"r")
    r = csv.reader(v,delimiter="\t")
    write = open("bin/quant_new_" + inputDir + ".csv", "w")
    writer = csv.writer(write,dialect='excel',delimiter='\t',quoting=csv.QUOTE_ALL)
    for row in r:
        tr = row[0].split('\t')[0]
        if tr != "Name":
            if tr in mean_sd:
                row.append(mean_sd[tr][0])
            if tr in mean_sd:
                row.append((mean_sd[tr][1])**2)
            # if tr in uniquely_mapped_tr_list:
            #     row.append(True)
            # else:
            #     row.append(False)
            if tr in weight_map.keys():
                row.append(weight_map[tr])
            else:
                row.append(0)
        else:
            # row.append("UniqueMap")
            row.append("Mean")
            row.append("Variance")
            row.append("Weight")
        writer.writerow(row)
    v.close()
    write.close()


def get_unique_ambiguous_maps(inputDir):
    uniquely_mapped_tr_list = []
    weight_map = dict()
    faulty_txp_class = FaultyTranscriptFilter.get_faulty_txp_class(inputDir)

    trEQMap = parseEQClass(inputDir)
    for tr in faulty_txp_class.keys():
        if tr in trEQMap.keys():
            eq_tuple = trEQMap[tr]
            if eq_tuple[1] == 1:
                if eq_tuple[2] == 1:
                    uniquely_mapped_tr_list.append(tr)
    for tr in trEQMap.keys():
        weight_map[tr] = trEQMap[tr][3]

    v = open('input/' + inputDir + '/quant.sf',"r")
    r = csv.reader(v,delimiter="\t")
    write = open("bin/quant_new_" + inputDir + ".csv", "w")
    writer = csv.writer(write,dialect='excel',delimiter='\t',quoting=csv.QUOTE_ALL)
    for row in r:
        tr = row[0].split('\t')[0]
        if tr != "Name":
            if tr in uniquely_mapped_tr_list:
                row.append(True)
            else:
                row.append(False)
            if tr in weight_map.keys():
                row.append(weight_map[tr])
            else:
                row.append(0)
            if tr in faulty_txp_class.keys():
                row.append(faulty_txp_class[tr])
            else:
                row.append(0)
        else:
            row.append("UniqueMap")
            row.append("Weight")
            row.append("Faulty")
        writer.writerow(row)
    v.close()
    write.close()
