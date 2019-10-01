# EHR-HeaderDetector: Electronic Health Record (EHR) Header Detector     



## Introduction
------------

This script performs EHR normalization by detecting headers from documents and mapping those sections into any desired archetype. It can also restore the lines that have been truncated by a conversion process from the original document to txt.
The detected headers also will save in a BRAT file with their begin and end spans.

Alos there is a script for doing statistical analysis on the detected headers in the given corpus.


## Directory structure
-------------------

<pre>
data/
This folder contains relevant information for the conversion process:

  - headers.txt: This file contains a list of allowed headers for your EHRs. The 
  normalizer tries to match detected header candidates to this list.
  - importat_headers.txt: This file contains a list of needed headers for doing statistical analysis.


documents/
Default root folder of source TXT files. It is mandatory to place all your TXT
files inside a "TXT-{Corpus Name}" folder. Your "TXT-{Corpus Name}" folder can be TXT files from different corpora 
  - Note: Replace {Corpus Name} wit the name of corpus, For Instance "TXT-SonEspases"

Output XML and BRAT files are stored in "XML-{Corpus Name}" and "BRAT-{Corpus Name}" folders.
  - Note: Replace {Corpus Name} wit the name of corpus, For Instance "BRAT-SonEspases"


scripts/
This folder contains the scripts needed to detect headers and calculate statistical analysis

analysis/
This folder contains the result (Plot and CVS) of statiscial analysis based on the detected headers.
  - PLOT/
  Showing how many headers we detec on the given corpus
  - CVS/
  {Corpus-Name}_analysis_files.csv: Showing all detected headers in each text file. 
  {Corpus-Name}_analysis_headers.csv: Showing all files that contain a specefic header. 
  {Corpus-Name}_analysis_header_co-occurrence.csv: Is it a matrix which showing how many times two headers co-occurrened
  {Corpus-Name}_analysis_original_headers_in_report.csv: Showing the original text in the EHR that script detect it as a header (By similarity method) 

</pre> 


## Usage
-----

For Detecting Header we use this commad:

	Python3 header-detector.py [options] 

Options:
<pre>
-c      Type of Corpus [For example: Aquas or SonEspases]
</pre>


For statistical Analysis of headers we use this commad:

	Python3 parser.py [options] 

Options:
<pre>
--filter     Filter files based on needed headers
--strict     Show just analysis of filtered headers
-c      Type of Corpus [For example: Aquas or SonEspases]
</pre>


For concatenate two ann files to together. 
	python3 concatenate.py [options] 

Options:
<pre>
-c      Type of Corpus [For example: Aquas or SonEspases]
</pre>


## Contact
------

Siamak Barzegar (siamak.barzegar@bsc.es)


## License
-------

Copyright (c) 2017-2018 Secretaría de Estado para el Avance Digital (SEAD)

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

