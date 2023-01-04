# DIAMOND (Double Index Alignment of Next-Generation Sequencing Data) workflow

#### **Summary**
This repository contains a latch wf for  BDIAMOND (Double Index Alignment of Next-Generation Sequencing Data).

#### **Input**

* Input Data
    - Input squneces in fasta format.
    
* Blast Type
    - BLAST search type. Possible options are blastn, and blastx.
    
 
* Database
    - Provide the input protein reference database file in FASTA format (may be gzip compressed).

* Sensitivity mode
    - Availaible options are --fast, --mid-sensitive, --sensitive, --more-sensitive, --very-sensitive and --ultra-sensitive. Without using any sensitivity option, the default mode will run which is designed for finding hits of >60% identity and short read alignment.

* Scoring matrix
    - The following matrices are supported BLOSUM45, BLOSUM50, BLOSUM62, BLOSUM80, BLOSUM90, PAM250, PAM70 and PAM30.

* Output format
    - Format of the output file. The following options are supported 0, 5, 6, 100, 101, 102, and 103.
        
#### **Output**
Alignment file. 

#### **Latch workflow link**
https://console.latch.bio/explore/83551/info
