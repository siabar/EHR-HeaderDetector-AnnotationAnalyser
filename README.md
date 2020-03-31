# EHR-HeaderDetector-AnnotationAnalyser: Electronic Health Record (EHR) Header Detector and Annotation Analyser #



## Introduction

This project is about (pre-)annotation of section headers in EHR. It includes different scripts to: 
(i) annotate and normalize section headers in EHR, 
(ii) generate statistical analysis on the annotated files, 

These scripts were used to identify and normalise section headers in discharge reports. 
The generated annotations can be loaded in the BRAT tool.


## Directory structure

- [**`Scripts/`**](Scripts/): 
This folder contains the scripts needed to detect headers, calculate statistical analysis of headers 
and comparing different annotations records (different annotators have done that) for the same file
and finally comparing the manually annotated files with pre-annotated files by [SpaCTeS tool](https://github.com/siabar/SpaCTeS).

  - [**`header_detector.py`**](Scripts/header_detector.py): Annotate and normalize section headers in EHR. 
    For detecting the section headers, we need the list of headers that is available of [data](data/) directory. 
    Input is in [TXT](documents/TXT) direcotry and 
    output is in [XML_SECTION](documents/XML_SECTION) directory and [ANN_SECTION](documents/ANN_SECTION) Directory.

  - [**`analysis_annotatedHeaders.py`**](Scripts/analysis_annotatedHeaders.py): Generate statistical analysis on the annotated files (output of header_detector.py).
    Input is [XML files](documents/XML_SECTION) and output is CSV and PLOT in analysis_headers directory.
    The script creates analysis_headers folder for output files.
    
- [**`data/`**](data/)
This folder contains relevant information for annotating and normalizing section headers in EHR:

  - **headers.txt**: This file contains a list of allowed headers for your EHRs. 
	The normalizer tries to match detected header candidates to this list.
  - **importat_headers.txt**: This file contains a list of necessary headers that EHRs should have them (doing statistical analysis just on these files).

- [**`documents/`**](documents/)
  - [**`txt/`**](documents/txt/): It is text files directory, this folder can have several sub-direcotries for each annotator
    and each annotator must have a sub-directory for each bunch.

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

  - [**`XML_SECTION/`**](documents/XML_SECTION/): Output of header_detector.py script.
  - [**`ANN_SECTION/`**](documents/ANN_SECTION/): Output of header_detector.py script.

- [**`analysis_headers/`**](analysis_headers/)
"analysis_annotatedHeaders" script creates this folder.
And it contains the results (Plot and CVS) of statistical analysis based on the detected headers.
  -  [**`PLOT/`**](analysis_headers/PLOT/):
    Showing how many headers have been detected on the given corpus.
  -  [**`CSV/`**](analysis_headers/CSV/):
    {Corpus-Name}_analysis_files.csv: Showing all detected headers in each text file. 
    {Corpus-Name}_analysis_headers.csv: Showing all files that contain a specific header. 
    {Corpus-Name}_analysis_header_co-occurrence.csv: It is a matrix which shows how many times two headers co-occurrence.
    {Corpus-Name}_top_10_header_co-occurances.csv: Showing top 10 co-occurances headers.
    {Corpus-Name}_analysis_original_headers_in_report.csv: Showing the original section in the EHR that script detects it as a header (By similarity method).


## Usage

**annotate and normalize section headers in EHR, use following command:**

    python3 header_detector.py [options] 

Options:
<pre>
--set       Number of bunch [For example: 01]
</pre>


**For Generating statistical analysis on the annotated files, use follwoing command:**

    python3 analysis_annotatedHeaders.py [options] 

Options:
<pre>
--filter    Select/filter the files that have all needed headers (importat_headers.txt in Data directory) [True/False]
--strict    Analysis just of selected files (--filter) [True/False]
--set       Number of the bunch [For example 01]
</pre>


## Contact

Siamak Barzegar (siamak.barzegar@bsc.es)
