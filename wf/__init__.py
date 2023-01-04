"""
A wf for  DIAMOND (Double Index Alignment of Next-Generation Sequencing Data).
"""


import subprocess
from pathlib import Path

from flytekit import LaunchPlan, workflow
from latch.types import LatchDir,LatchFile
from latch import large_task
from latch.resources.launch_plan import LaunchPlan
import os,shutil
from typing import Optional, Annotated
from flytekit.core.annotation import FlyteAnnotation

@large_task
def runwf(fasta_file: Optional[LatchFile],
    aa_sequence: Optional[str],
    output_dir: LatchDir,db: LatchFile,
    blastType: str = "blastp",sensitivity: str = "--very-sensitive",matrix: str = "BLOSUM62",
    outfmt: str = "6") -> LatchDir:

    os.mkdir('results')
    os.chdir("/root/results/")

    cmd="/root/blast/bin/"+blastType
    subprocess.run(["/root/diamond","makedb","--in",db,"-d","database"])

    if fasta_file is not None:

        subprocess.run(
            [
                "/root/diamond",
                blastType,
                "-q",
                fasta_file.local_path,
                "-d",
                "database",
                "-o",
                "output.tsv",
                sensitivity,
                "--matrix",
                matrix,
                "--outfmt",
                outfmt
            ]
        )

    else:
        text_file = open("input.txt", "w")
        text_file.write(aa_sequence)
        text_file.close()

        subprocess.run(
            [
                "/root/diamond",
                blastType,
                "-q",
                "input.txt",
                "-d",
                "database",
                "-o",
                "output.tsv",
                sensitivity,
                "--matrix",
                matrix,
                "--outfmt",
                outfmt
            ]
        )

    local_output_dir = str(Path("/root/results/").resolve())

    remote_path=output_dir.remote_path
    if remote_path[-1] != "/":
        remote_path += "/"

    return LatchDir(local_output_dir,remote_path)

#-> LatchDir
@workflow
def DIAMOND(output_dir: LatchDir,db: LatchFile,blastType: str = "blastp",
sensitivity: str = "--very-sensitive",matrix: str = "BLOSUM62",outfmt: str = "6",
input_sequence_fork: str = "file",
        fasta_file: Optional[
        Annotated[
            LatchFile,
            FlyteAnnotation(
                {
                    "rules": [
                        {
                            "regex": "(.fasta|.fa|.faa|.txt|.fas)$",
                            "message": "Only .fasta, .fa, .fas,.txt, or .faa extensions are valid",
                        }
                    ],
                }
            ),
        ]
    ] = None,
    aa_sequence: Optional[
        Annotated[
            str,
            FlyteAnnotation(
                {
                    "appearance": {
                        "type": "paragraph",
                        "placeholder": ">SequenceOne\nLESPNCDWKNNR...\n>SequenceTwo\nRLENKNNCSPDW...\n>SequenceThree\nCDWKNNENPDEA...",
                    },
                    "rules": [
                        {
                            "message": "Paste a set of sequences in fasta format. The name line must start with `>`.",
                        }
                    ],
                }
            ),
        ]
    ] = None):
    """

    A wf for  DIAMOND (Double Index Alignment of Next-Generation Sequencing Data).
    ----

    DIAMOND is an ultra-fast and sensitive sequence aligner for protein and translated DNA searches at tree-of-life scale. DIAMOND matches the alignment sensitivity of the gold-standard tool BLASTP when run in –very-sensitive and –ultra-sensitive modes, while achieving up to 360x computational speed-up.

    __metadata__:
        display_name: DIAMOND (Double Index Alignment of Next-Generation Sequencing Data)
        author:
            name: Akshay
            email: akshaysuhag2511@gmail.com
            github:
        repository:
        license:
            id: MIT
        flow:
        - section: Fasta Sequences
          flow:
            - fork: input_sequence_fork
              flows:
                file:
                    display_name: File
                    _tmp_unwrap_optionals:
                        - fasta_file
                    flow:
                        - params:
                            - fasta_file

                text:
                    display_name: Text
                    _tmp_unwrap_optionals:
                        - aa_sequence
                    flow:
                        - params:
                            - aa_sequence


        - section: Parameters
          flow:
          - params:
              - blastType
          - params:
              - db
          - params:
              - sensitivity
          - params:
              - matrix
          - params:
              - outfmt

        - section: Output Settings
          flow:
          - params:
              - output_dir




    Args:

        fasta_file:
          Select input file. This file must be in FASTA format.

          __metadata__:
            display_name: Input File

        aa_sequence:
            Fasta sequences.

            __metadata__:
                display_name: Fasta Sequence(s)

        input_sequence_fork:

            __metadata__:
                display_name: Input Sequence (AA or Nucleotide)

        blastType:
            BLAST search type. Possible options are blastp, and blastx.

            __metadata__:
                display_name: BLAST Type

        db:
             Provide the input protein reference database file in FASTA format (may be gzip compressed).
            __metadata__:
                display_name: Database

        sensitivity:
            Availaible options are --fast, --mid-sensitive, --sensitive, --more-sensitive, --very-sensitive and --ultra-sensitive. Without using any sensitivity option, the default mode will run which is designed for finding hits of >60% identity and short read alignment.
            __metadata__:
                display_name: Sensitivity mode

        matrix:
            Scoring matrix. The following matrices are supported BLOSUM45, BLOSUM50, BLOSUM62, BLOSUM80, BLOSUM90, PAM250, PAM70 and PAM30.
            __metadata__:
                display_name: Matrix

        outfmt:
            Format of the output file. The following options are supported 0, 5, 6, 100, 101, 102, and 103.
            __metadata__:
                display_name: outfmt

        output_dir:
          Where to save the results?.

          __metadata__:
            display_name: Output Directory
    """
    return runwf(fasta_file=fasta_file,aa_sequence=aa_sequence,blastType=blastType,db=db,sensitivity=sensitivity,matrix=matrix,outfmt=outfmt,output_dir=output_dir)

LaunchPlan(
    DIAMOND,
    "Test Data",
    {
        "fasta_file": LatchFile("s3://latch-public/test-data/4148/astral-scopedom-seqres-gd-sel-gs-bib-40-2.07.fa"),
        "db": LatchFile("s3://latch-public/test-data/4148/astral-scopedom-seqres-gd-sel-gs-bib-40-2.07.fa")

    },
)
