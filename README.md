# EHR-HeaderDetector: Electronic Health Record (EHR) Header Detector     



## Introduction

This project has several scripts, one of them performs EHR normalization 
by detecting headers from documents and mapping those sections into 
any desired archetype. 
The detected headers also will save in a BRAT file with their begin and end spans.

Alos there is a script for doing statistical analysis on the detected headers in the given corpus
and comparing manually annotated files by annotators with pre-annotated files and 
do statistical analysis on the results.


## Directory structure

scripts/
This folder contains the scripts needed to detect headers, calculate statistical analysis of headers 
and compraing different annotations records (that has been done by different annotators) for a same file
and finally comparing the manually annotated files with pre-annotated files by [SpaCTeS tool](https://github.com/siabar/SpaCTeS).

  - header_detector.py: For detecting headers of EHR (Electronich Health Records). 
	We need the list of headers that is available of [data directory](data/). 
	Input is [TXT files](documents/TXT) and 
	output is [XML files](documents/XML_SECTION) and [BRAT files (ANN)](documents/ANN_SECTION) .

  - parser.py: For calulating statistical analysis on the headers of XML files (output of header_detector.py).
	Input is [XML files](documents/XML_SECTION) and output is CSV and PNG in analysis_headers directory.
	analysis_headers folder will be create after running "parser" script.

  - concatenate.py: For concatenating outout of header_detector (ANN files in root/documents/ANN_SECTION) with
	output of [pre_annotated files --BRAT files (ANN)](documents/ANN_VARIABLE) of [SpaCTeS tool](https://github.com/siabar/SpaCTeS).
	Output of this script will be [ANN_FINAL](documents/ANN_FINAL).

  - comparing_ann.py: For
	1) comparing the activity of annotators with together. 
	   Output of this part will be saved [IAA files](Annotated/IAA),
 	   which are ANN files with all acitivity of all annotators for given files
	   and [CSV Directory](Annotated/post_processing_csv), which acitivities of all annotators 
	   have been shown for all annotated tokens.
	2) Comparing the manually [annotated files](Annotated/annotators) with [pre-annotated file](Annotated/cTAKES) by [SpaCTeS tool](https://github.com/siabar/SpaCTeS)
	   For detecing which pre-annoted variables have been changed, accepted, removed and 
	   which variables have been added by annotators.
	   Also calulate statistical analysis on how many variables have been added/accepted/changed/removed.
	   Output of this part will be saved at [analysis](Annotated/analysis)

	Note: All output directories of this part will be created after running this script
 
data/
This folder contains relevant information for the conversion process:

  - headers.txt: This file contains a list of allowed headers for your EHRs. The 
  normalizer tries to match detected header candidates to this list.
  - importat_headers.txt: This file contains a list of needed headers for doing statistical analysis.


documents/

  - TXT/: Text files directory, this folder can have several sub-direcotries for each annotator
	and it is mandatory that each annotator has sub-directory for difference bunch

	Example of format of TXT directory (All other directories in documents also follow this format):

	TXT/
	   - Annotator1
		-01
		-02
		- ...
	   - Annotator2
		-01
		-02


  - XML_SECTION/: Output of header_detector.py script
  - ANN_SECTION/: Output of header_detector.py script and input for concatenate.py script
  - ANN_VARIABLE/: Output of [SpaCTeS tool](https://github.com/siabar/SpaCTeS), which would be ANN files and input for concatenate.py script
  - ANN_FINAL/: Outout of concatenate.py script


analysis_headers/
This folder will be create after running "parser" script.
and it contains the result (Plot and CVS) of statiscial analysis based on the detected headers.
  - PLOT/:
	Showing how many headers we detec on the given corpus
  - CVS/:
	{Corpus-Name}_analysis_files.csv: Showing all detected headers in each text file. 
	{Corpus-Name}_analysis_headers.csv: Showing all files that contain a specefic header. 
	{Corpus-Name}_analysis_header_co-occurrence.csv: Is it a matrix which showing how many times two headers co-occurrened
	{Corpus-Name}_analysis_original_headers_in_report.csv: Showing the original text in the EHR that script detect it as a header (By similarity method) 

Annotated/
This folder contains the results of compraing different annotations records (that has been done by different annotators) 
for a same file and comparing the manually annotated files with pre-annotated files by [SpaCTeS tool](https://github.com/siabar/SpaCTeS).

  - annotators/: original files for each annotator.
  - cTAKES/: pre-annotated ANN files (output of [SpaCTeS tool](https://github.com/siabar/SpaCTeS)).
  - pre-processing/: directory for cleaned ANN files after removing un-necassery annotations.
  - IAA/:  Result of comparing annotators' acitivies in ANN files (ANN files with all acitivity of all annotators for given files)
  - post_processing_csv/:  Result of comparing annotators' activities in csv files
    (acitivities of all annotators have been shown for all annotated tokens).
  - analysis/: Comparing the manually [annotated files](Annotated/annotators) with [pre-annotated file](Annotated/cTAKES) by [SpaCTeS tool](https://github.com/siabar/SpaCTeS)
    For detecing which pre-annoted variables have been changed, accepted, removed and 
    which variables have been added by annotators.
    Also calulate statistical analysis on how many variables have been added/accepted/changed/removed.




## Usage

For Detecting Header we use this commad:

	Python3 header-detector.py [options] 

Options:
<pre>
--set       Number of bunch [For example: 01]
</pre>


For statistical Analysis of headers we use this commad:

	Python3 parser.py [options] 

Options:
<pre>
--filter     Filter files based on needed headers
--strict     Show just analysis of filtered headers
--set       Number of bunch [For example: 01]
</pre>


For concatenate two ann files to together. 
	python3 concatenate.py [options] 

Options:
<pre>
--set       Number of bunch [For example: 01]
</pre>


For comparing different ann files. 
	python3 comparing_ann.py [options] 

Options:
<pre>
--set      Number of bunch that we want to do comparing [For example: 01]
</pre>


## Contact

Siamak Barzegar (siamak.barzegar@bsc.es)


## License

Copyright (c) 2017-2018 Secretaría de Estado para el Avance Digital (SEAD)

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

