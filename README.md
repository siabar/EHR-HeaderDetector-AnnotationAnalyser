# EHR-HeaderDetector-AnnotationAnalyser: Electronic Health Record (EHR) Header Detector and Annotation Analyser #



## Introduction

This project is about (pre-)annotation of section headers in EHR. It includes different scripts to: 
(i) annotate and normalize section headers in EHR, 
(ii) generate statistical analysis on the annotated files, 
(iii) merge the annotations in BRAT and 
(iv) to monitor and assess the eventual manual annotation task done on the pre-annotated documents.

These scripts were used to identify and normalise section headers in discharge reports. 
The generated annotations can be loaded in the BRAT tool and merged with additional annotations.
Once all annotations are loaded in BRAT, expert humans can do the eventual 
manual annotation (by validating and|or editing the automatic pre-annotations). 
The project includes a script that computes inter-annotation agreement (IAA) and 
compares the pre-annotations with the eventual manual annotations to monitor the human annotation task.


## Directory structure

- [**`scripts/`**](scripts/): 
This folder contains the scripts needed to detect headers, calculate statistical analysis of headers 
and comparing different annotations records (different annotators have done that) for the same file
and finally comparing the manually annotated files with pre-annotated files by [SpaCTeS tool](https://github.com/siabar/SpaCTeS).

  - [**`header_detector.py`**](script/header_detector.py): Annotate and normalize section headers in EHR, (Electronic Health Records). 
    For detecting the section headers, we need the list of headers that is available of [data](data/) directory. 
    Input is in [TXT](documents/TXT) direcotry and 
    output is in [XML_SECTION](documents/XML_SECTION) directory and [ANN_SECTION](documents/ANN_SECTION) Directory.

  - [**`parser.py`**](script/parser.py): Generate statistical analysis on the annotated files (output of header_detector.py).
    Input is [XML files](documents/XML_SECTION) and output is CSV and PNG in analysis_headers directory.
    analysis_headers folder will be created after running "parser" script.

  - [**`concatenate.py`**](script/concatenate.py): Merge the annotations in BRAT format (ANN files in root/documents/ANN_SECTION) with
    output of [pre_annotated files --BRAT files (ANN)](documents/ANN_VARIABLE) of [SpaCTeS tool](https://github.com/siabar/SpaCTeS).
    Output of this script is at [ANN_FINAL](documents/ANN_FINAL) directory.

  - [**`comparing_ann.py`**](script/comparing_ann.py): Monitor and assess the eventual manual annotation task done on the pre-annotated documents.
      1) Computes inter-annotation agreement (IAA)
       Outputs are:
       [IAA Directory](Annotated/IAA), which are ANN files with manual annotations of all annotators for given files and
       [CSV Directory](Annotated/post_processing_csv), which show all opinion of annotators for each annotations of given files.
    2) Compares the the eventual manual annotations [annotated files](Annotated/annotators) with [the pre-annotations](Annotated/cTAKES) by [SpaCTeS tool](https://github.com/siabar/SpaCTeS)
       to monitor the human annotation task.
       It detects which pre-annotated variables have been changed, accepted, removed and 
       which variables have been added by annotators.
       Also, calculate statistical analysis on how many variables have been added/accepted/changed/removed.
       The output is in [analysis](Annotated/analysis) directory

    **Note**: All output directories of this part creates after running "comparing_ann.py" script.
    
- [**`data/`**](data/)
This folder contains relevant information for the conversion process:

  - **headers.txt**: This file contains a list of allowed headers for your EHRs. 
	The normalizer tries to match detected header candidates to this list.
  - **importat_headers.txt**: This file contains a list of needed headers for doing statistical analysis.

- [**`documents/`**](documents/)
  - [**`txt/`**](documents/txt/): Text files directory, this folder can have several sub-direcotries for each annotator
    and each annotator must have sub-directory for difference bunch

    Example of format of TXT directory (All other directories in documents also follow this format):
    ```
    - TXT/
      - Annotator1/
        - 01/
          - file1.txt
          - file2.txt
          - ...
        - 02/
          - file4.txt
          - file5.txt
          - ...
        - ...

      - Annotator2/
        - 01/
          - file3.txt
          - file2.txt
          - ...
        - 02/
          - file6.txt
          - file7.txt
          - ...
        - ...
      - ...
    ```

  - [**`XML_SECTION/`**](documents/XML_SECTION/): Output of header_detector.py script
  - [**`ANN_SECTION/`**](documents/ANN_SECTION/): Output of header_detector.py script and input for concatenate.py script
  - [**`ANN_VARIABLE/`**](documents/ANN_VARIABLE/): Output of [SpaCTeS tool](https://github.com/siabar/SpaCTeS), which would be ANN files and input for concatenate.py script
  - [**`ANN_FINAL/`**](documents/ANN_FINAL/): Outout of concatenate.py script

- [**`analysis_headers/`**](analysis_headers/)
This folder creates after running "parser" script.
And it contains the results (Plot and CVS) of a statistical analysis based on the detected headers.
  -  [**`PLOT/`**](analysis_headers/PLOT/):
    Showing how many headers we detect on the given corpus
  -  [**`CSV/`**](analysis_headers/CSV/):
    {Corpus-Name}_analysis_files.csv: Showing all detected headers in each text file. 
    {Corpus-Name}_analysis_headers.csv: Showing all files that contain a specific header. 
    {Corpus-Name}_analysis_header_co-occurrence.csv: Is it a matrix which shows how many times two headers co-occurrence
    {Corpus-Name}_analysis_original_headers_in_report.csv: Showing the original text in the EHR that script detects it as a header (By similarity method) 

- [**`Annotated/`**](Annotated/)
This folder contains the results of comparing different annotations records (different annotators have done that) 
for the same file and comparing the manually annotated files with pre-annotated files by [SpaCTeS tool](https://github.com/siabar/SpaCTeS).

  - [**`annotators/`**](Annotated/annotators/): original files for each annotator.
  - [**`pre_processing/`**](Annotated/pre_processing/): directory for cleaned ANN files after removing un-necassery annotations.
  - [**`IAA/`**](Annotated/IAA/):  Result of comparing annotators' acitivies in ANN files (ANN files with all acitivity of all annotators for given files)
  - [**`post_processing_csv/`**](Annotated/post_processing_csv/):  Result of comparing annotators' activities in csv files
    (acitivities of all annotators have been shown for all annotated tokens).
  - [**`analysis/`**](Annotated/analysis/): Comparing the manually [annotated files](Annotated/annotators) with [pre-annotated file](Annotated/cTAKES) by [SpaCTeS tool](https://github.com/siabar/SpaCTeS)
    For detecting which pre-annotated variables have been changed, accepted, removed and 
    which variables have been added by annotators.
    Also, calculate statistical analysis on how many variables have been added/accepted/changed/removed.

## Usage

**annotate and normalize section headers in EHR, use following command:**

    python3 header-detector.py [options] 

Options:
<pre>
--set       Number of bunch [For example: 01]
</pre>


**For Generating statistical analysis on the annotated files, use follwoing command:**

    python3 parser.py [options] 

Options:
<pre>
--filter     Filter files based on needed headers
--strict     Show just analysis of filtered headers
--set       Number of the bunch [For example 01]
</pre>


**For merging the annotations in BRAT, use follwoing command:**

    python3 concatenate.py [options] 

Options:
<pre>
--set       Number of bunch [For example: 01]
</pre>


**For monitor and assess the eventual manual annotation task done on the pre-annotated documents, use following command**: 

    python3 comparing_ann.py [options] 

Options:
<pre>
--set      Number of bunch that we want to do comparing [For example: 01]
</pre>


## Contact

Siamak Barzegar (siamak.barzegar@bsc.es)
