# EHR-HeaderDetector-AnnotationAnalyser: Electronic Health Record (EHR) Header Detector and Annotation Analyser #

## Digital Object Identifier (DOI)

## Introduction

This project is about (pre-)annotation of section headers in EHR. It includes different scripts to: 
(i) annotate and normalize section headers in EHR, 
(ii) generate statistical analysis on the annotated files. 

These scripts were used to identify and normalise section headers in discharge reports. 
The generated annotations can be loaded in the BRAT tool.


## Prerequisites
In Linux
<pre>
sudo apt-get install python3-dev python3-pip git
</pre>

For header_detector script
<pre>
pip3 install unidecode
</pre>

For analysis_annotatedHeaders script
<pre>
pip3 install numpy
pip3 install pandas
pip3 install matplotlib
</pre>


## Directory structure

- [**`scripts/`**](scripts/): 
This folder contains the scripts needed to detect headers, calculate statistical analysis of headers 
and comparing different annotations records (different annotators have done that) for the same file
and finally comparing the manually annotated files with pre-annotated files by [SpaCTeS tool](https://github.com/siabar/SpaCTeS).

  - [**`header_detector.py`**](scripts/header_detector.py): Annotate and normalize section headers in EHR. 
    For detecting the section headers, we need the list of headers that is available of [data](data/) directory. 
    Input is in [TXT](documents/TXT) direcotry and 
    output is in [XML_SECTION](documents/XML_SECTION) directory and [ANN_SECTION](documents/ANN_SECTION) Directory.

  - [**`analysis_annotatedHeaders.py`**](scripts/analysis_annotatedHeaders.py): Generate statistical analysis on the annotated files (output of header_detector.py).
    Input is [XML files](documents/XML_SECTION) and output is CSV and PLOT in analysis_headers directory.
    The script creates analysis_headers folder for output files.
    
- [**`data/`**](data/)
This folder contains relevant information for annotating and normalizing section headers in EHR:

  - **headers.txt**: This file contains a list of allowed headers for your EHRs. 
	The normalizer tries to match detected header candidates to this list.
	This file has three columns that have been separated by TAB ("\t"):
	<pre>
	"ARQUETYPE"[TAB]"HEADER"[TAB]"HEADER VARIATION" 
	</pre>
  - **importat_headers.txt**: This file contains a list of necessary headers that EHRs should have them (doing statistical analysis just on these files).
    <pre>
    Each line one Header
    </pre>
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
      ```
      {Bunch-Number}_analysis_files.csv: Showing all detected headers in each text file. 
      {Bunch-Number}_analysis_headers.csv: Showing all files that contain a specific header. 
      {Bunch-Number}_analysis_header_co-occurrence.csv: It is a matrix which shows how many times two headers co-occurrence.
      {Bunch-Number}_top_10_header_co-occurances.csv: Showing top 10 co-occurances headers.
      {Bunch-Number}_analysis_original_headers_in_report.csv: Showing the original section in the EHR that script detects it as a header (By similarity method).
      ```



## Usage

**To annotate and normalize section headers in EHR, use following command:**

    python3 header_detector.py --set NUMBER

<pre>
--set       (Mandatory) Number of bunch [For example: 01] 
</pre>


**To Generate a statistical analysis on the annotated files, use following command:**

    python3 analysis_annotatedHeaders.py --set NUMBER [options] 

Options:
<pre>
--filter    Select/filter the files that have all needed headers (important_headers.txt in Data directory) [True/False]
--strict    Analysis just of selected files (--filter) [True/False]
--set       (Mandatory) Number of the bunch [For example 01]
</pre>

## Examples

**To annotate and normalize section headers:**
<pre>
$ python3 analysis_annotatedHeaders.py --set 01
</pre>

**To generate a statistical analysis:**
<pre>
$ python3 header_detector.py --set 01
</pre>

## Contact

Siamak Barzegar (siamak.barzegar@bsc.es)

## License
MIT License

Copyright (c) 2020 Text Mining Unit at BSC

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
