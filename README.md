* The project is developed in Python 3.6.

* Pre-requisites: 
	Few python packages like sklearn, statistics etc. are required. 
	If 'missing package' error occurs please use: sudo pip install <package-name> to install the package.
	
* Execution:

	* Before execution please copy folder containing input files quant.sf, quant_bootstraps.tsv and eq_classes.txt to "input" folder inside project directory.

	For e.g. to copy files of poly_mo - quant.sf,quant_bootstraps.tsv and eq_classes.txt,I will copy the entire folder poly_mo into the "input" folder

	
	* Execute the following command:
		
		python src/error_addition.py <name_of_directory>
	
		For eg: python src/error_addition.py poly_ro
		
	* New bootstrap file will be available in "output" folder in project directory with the name "quant_bootstraps_new.tsv"
		
* Verification:
	
	To verify number of faulty transcripts after new file has been created, run the following command:
	
		python src/verify_faulty_transcripts.py <name_of_directory>
		
	Note: Please add poly_truth.tsv to input directory before running the verification command.
	

* Commands and Output:
```
D:\SBU\UncertaintyQuantifier>python src/error_addition.py poly_mo
Loading Files and Processing....................................................................................................................
Predicting Faulty Transcripts...................................................................................................................
Classification started
Classification done
Processing to reduce the faulty transcripts count...............................................................................................
Predicting Error values for faulty transcripts..................................................................................................
Error values predicted.
Error Values predicted.
Creating new quant_bootstrap.tsv................................................................................................................
New file created at: output/quant_bootstraps_new.tsv
Process finished.

D:\SBU\UncertaintyQuantifier>python src/verify_faulty_transcripts.py poly_mo
Counting faulty Transcripts in new quant_bootstrap.tsv..........................................................................................
Faulty Transcripts Count in the new file: 10871
Process finished.

```