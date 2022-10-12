# Deduper Pseudocode

## Problem
PCR duplicates are created when a certain molecule is overexpressed during the PCR Amplification stage, in this case we need to only mantain one.

## How to identify it
PCR duplicates will bind to the same region of the DNA and specifically will have the same following features
    - Chromosome
    - Start position
    - Strand
    - UMI Identifier

## Considerations

- Must read SAM/BAM file
- Consider the features listed above
- Adjust start position by soft clipping
- Don't store all of the data *Use a ban position list*

### Input example

*Sequence 1*
K00337:83:HJK:8:1101:2808:1191:ACTACTG    99  5   76364474    255 101M    =   76364565    191     GNCCGCATGCCAACTGAGCGATTCTTTCTGGCCATCCCCTTCCTCTCGCA A#AFFJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJ

*Sequence 2; Reverse Complement Seq 1*
K00337:83:HJK:8:1101:2808:1191:ACTACTG    16  5   76364474    255 101M    =   76364565    191     GNCCGCATGCCAACTGAGCGATTCTTTCTGGCCATCCCCTTCCTCTCGCA A#AFFJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJ

*Sequence 3; Different start position by CIGAR as Seq 1(starts with S)*
K00337:83:HJK:8:1101:2808:1191:ACTACTG    99  5   76364474    255 2S101M    =   76364565    191     GNCCGCATGCCAACTGAGCGATTCTTTCTGGCCATCCCCTTCCTCTCGCA A#AFFJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJ

*Sequence 4; Different start position*
K00337:83:HJK:8:1101:2808:1191:ACTACTG    99  5   76364471    255 101M    =   76364565    191     GNCCGCATGCCAACTGAGCGATTCTTTCTGGCCATCCCCTTCCTCTCGCA A#AFFJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJ

*Sequence 5; Different UMI as Seq1*
K00337:83:HJK:8:1101:2808:1191:ACTAGTG    99  5   76364474    255 101M    =   76364565    191     GNCCGCATGCCAACTGAGCGATTCTTTCTGGCCATCCCCTTCCTCTCGCA A#AFFJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJ

*Sequence 6; Unknown UMI*
K00337:83:HJK:8:1101:2808:1191:ACTAGTGNNN    99  5   76364474    255 101M    =   76364565    191     GNCCGCATGCCAACTGAGCGATTCTTTCTGGCCATCCCCTTCCTCTCGCA A#AFFJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJ

*Sequence 7; Same as Seq 1*
K00337:83:HJK:8:1101:2808:1191:ACTACTG    99  5   76364474    255 101M    =   76364565    191     GNCCGCATGCCAACTGAGCGATTCTTTCTGGCCATCCCCTTCCTCTCGCA A#AFFJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJ

### Output Example

*Sequence 1*
K00337:83:HJK:8:1101:2808:1191:ACTACTG    99  5   76364474    255 101M    =   76364565    191     GNCCGCATGCCAACTGAGCGATTCTTTCTGGCCATCCCCTTCCTCTCGCA A#AFFJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJ

*Sequence 2*
K00337:83:HJK:8:1101:2808:1191:ACTACTG    16  5   76364474    255 101M    =   76364565    191     GNCCGCATGCCAACTGAGCGATTCTTTCTGGCCATCCCCTTCCTCTCGCA A#AFFJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJ

*Sequence 3*
K00337:83:HJK:8:1101:2808:1191:ACTACTG    99  5   76364474    255 2S101M    =   76364565    191     GNCCGCATGCCAACTGAGCGATTCTTTCTGGCCATCCCCTTCCTCTCGCA A#AFFJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJ

*Sequence 4*
K00337:83:HJK:8:1101:2808:1191:ACTACTG    99  5   76364471    255 101M    =   76364565    191     GNCCGCATGCCAACTGAGCGATTCTTTCTGGCCATCCCCTTCCTCTCGCA A#AFFJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJ

*Sequence 5*
K00337:83:HJK:8:1101:2808:1191:ACTAGTG    99  5   76364474    255 101M    =   76364565    191     GNCCGCATGCCAACTGAGCGATTCTTTCTGGCCATCCCCTTCCTCTCGCA A#AFFJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJ



### Functions

*Here I list the probable functions that i will use for my actual code*

#### Function Read_SAM
Read a SAM File by line and obtain the following variables
    umi = col 1 #UMI Identifier
    #QNAME.strip("\n").split(":")[-1] or [7]
    str = col 2 #Sense of the strand (+ or -)
    chr = col 3 #Which chromosome are we looking at
    pos = col 4 #Left most position of the sequence
    clip = col 6 # CIGAR String
return list(umi,chr,pos,str,clip)
return record

Input example.- K00337:83:HJK:8:1101:2808:1191:ACTACTG    99  5   76364474    255 101M    =   76364565    191     GNCCGCATGCCAACTGAGCGATTCTTTCTGGCCATCCCCTTCCTCTCGCA A#AFFJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJ

Return example.- (ACTACTG, 5, 76364474, 99, 101M)

#### Function strand_flag
Read the bitflag given and determine the direction of the strand (+ or -)
    if flag has 16 
        strand is "-"
    else
        strand is "+"
return strand direction

Input example
a) 16
b) 99
c) 256

Return example
a) -
b) +
c) +


#### Pos_clip
Reads strandedness, cigar string and left most position and returns the adjusted start position of sequence.
    If strand "+"
        If starts with X"S" #X being any number
            new_pos = pos - X
        else
            new_pos = pos
    elif strand "-"
        If starts with X"S" #X being any number
            ignore the X value and sum any number pertaining to a operator except "I" and Y being the sum of all those values:
            new_pos = pos + Y
        else
            any number pertaining to a operator except "I" and Y being the sum of all those values:
            new_pos = pos + Y

Input example
a) -, 100M, 1000
b) +, 100M, 1000
c) -, 2S100M, 1000
d) +, 2S100M, 1000
e) -, 100M2S, 1000
f) +, 100M2S, 1000
g) -, 2S100M30I2S, 1000
h) +, 2S100M30I2S, 1000

Output example
a) 1100
b) 1000
c) 1100
d) 998
e) 1102
f) 1000
g) 1102
h) 998


### Pseudocode

Sort SAM file

Create a list of UMI names UMI_List

Create an empty set of ban list to have a string that will store the following info
ban_list = () # "chr-pos-str-umi"

Read SAM File with the function and obtain # One record at a time
    - Chromosome
    - Start position
    - Strand direction
    - UMI
    from the return list create a string in the format chr-pos-str-umi
    
    If UMI in UMI_List:
        If "chr-pos-str-umi" not in ban_list:
            write record to new_sam_file
            ban_list.append("chr-pos-str-umi")

