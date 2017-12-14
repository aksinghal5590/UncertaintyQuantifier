* The project is developed in Python 3.6.

* Pre-requisites: 
	Few python packages like sklearn, statistics etc. are required. 
	If 'missing package' error occurs please use: sudo pip install <package-name> to install the package.
	
* Execution:

	* Before execution please copy folder containing input files quant.sf, quant_bootstraps.tsv and eq_classes.txt to "input" folder inside project directory.
	
	* Execute the following command:
		
		python src/error_addition.py <name_of_directory>
	
		For eg: python src/error_addition.py poly_ro
		
	* New bootstrap file will be available in "output" folder in project directory.
		
* Verification:
	
	To verify number of faulty transcripts after new file has been created, run the following command:
	
		python FaultyTranscriptFilter <name_of_directory>
		
	Note: Please add poly_truth.tsv to input directory before running the verification command.
	