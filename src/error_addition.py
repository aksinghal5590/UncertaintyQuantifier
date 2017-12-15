import sys
import predict_errorValue
import pandas as pd

#This function modifies the mean according to the error value and also modifies quant_bootstrap.tsv
def error_addition(inputDir):
    print("Loading Files and Processing....................................................................................................................")
    predict_errorValue.predict_error_value(inputDir)
    print("Error Values predicted.")
    df2 = pd.read_csv("bin/pred_errorValue_" + inputDir + ".csv", sep="\t")

    i = 0
    for err in df2["Predicted_ErrorValue"]:
        if err < 0:
            df2.ix[i,"Diff"] = df2.ix[i,"Mean"] - (df2.ix[i,"Predicted_ErrorValue"])*(0.65)
        if err > 0:
            df2.ix[i,"Diff"] = df2.ix[i,"Mean"] + (df2.ix[i,"Predicted_ErrorValue"])*(0.65)
        i+=1
    names = df2["Name"].tolist()
    data_frame = pd.read_csv('input/' + inputDir + '/quant_bootstraps.tsv', sep='\t')
    new_names = list(data_frame.columns.values)
    # i = 0
    # print(len(names))
    print("Creating new quant_bootstrap.tsv................................................................................................................ ")
    for name in new_names:
        if name in names:
            loc = names.index(name)
            if df2.ix[loc,"Predicted_ErrorValue"] < 0:
                data_frame[name] = data_frame[name] - ((df2.ix[loc,"Predicted_ErrorValue"]) * 0.65)
            if df2.ix[loc,"Predicted_ErrorValue"] > 0:
                data_frame[name] = data_frame[name] + ((df2.ix[loc, "Predicted_ErrorValue"]) * 0.65)
    data_frame.to_csv('output/quant_bootstraps_new.tsv', sep='\t',index=False)
    print("New file created at: " + 'output/quant_bootstraps_new.tsv')
    print("Process finished.")


error_addition(sys.argv[1])
