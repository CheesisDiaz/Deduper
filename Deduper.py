#!/usr/bin/env python
import re
import argparse

def get_args():
    parser = argparse.ArgumentParser(description= "This program takes in a mapped and sorted by Left most position (Column 4) reads and will remove any PCR duplicates which will be written to a new file")
    parser.add_argument("-f", "--file", help="Input the filename of the sam file to dedupe", type=str, required=True)
    parser.add_argument("-o", "--outfile", help="Input the filename of the new deduped sam file", type=str, required=True)
    parser.add_argument("-u", "--umi", help="Input the filename for the file with the known UMIs", type=str, required=True)
    return parser.parse_args()

args = get_args()
og_sam = args.file
new_sam = args.outfile
umi_file = args.umi

#VARIABLES
ban_set = set()
counting = {"Wrong_UMI":0, "Duplicate":0, "Unique":0}

#FUNCTIONS

def strand_flag(flag:int) -> str: #Ask if I can use operators + and -
    '''This function will take the integer of bit flag and return the stranded direction'''
    if (int(flag) & 16) == 16:
        strand = "-"
    else:
        strand = "+"
    return(strand)

def read_sam(sam: str) -> list:
    ''''This function will read through the SAM file per record and will return a list with the data we need for deduping'''
    while True:
        record = sam.readline()
        if record == "":
            return 0
        if "@" in record:
            return (False, record)
        else:
            chrom = record.split("\t")[2]
            pos = record.split("\t")[3]
            b_flag = record.split("\t")[1]
            stranded = strand_flag(b_flag)
            clip = record.split("\t")[5]
            umi = record.split("\t")[0].split(":")[-1]
        return (chrom,pos,stranded,clip,umi,record)

cigar_dict={"S":0, "M":0, "N":0, "D":0}
def pos_clip(pos:int, strand:str, cigar:str) -> int:
    '''This function will consider Left most position the strand direction and the cigar string to return the correct start position of the read (will sum up when on negative strand and remove when on the positive strand)'''
    total = 0
    if str(strand) == "+":
        if re.match("[0-9]{1,4}S", cigar):
            x = cigar.split("S")[0]
            pos = int(pos) - int(x)
        else:
            pos = int(pos)
    elif str(strand) == "-":
        if re.match("[0-9]{1,4}S", cigar):
            new_cigar=cigar.split("S",1)[1]
            new_cigar = re.split("([0-9]{1,4}[A-Z])", new_cigar)
            new_cigar = " ".join(new_cigar).split()
            for letter in new_cigar:
                cig_letter = str(letter[-1])
            if str(cig_letter) in cigar_dict.keys():
                cigar_dict[cig_letter] += int(letter[:-1])
            for key,values in cigar_dict.items():
                total += int(values)
            # if cigar_dict["I"] != 0:
            #     total = total - cigar_dict["I"]
            pos = int(pos) + int(total)
                                 
        else:
            y = re.split("([0-9]{1,4}[A-Z])", cigar)
            y = " ".join(y).split()
            for letter in y:
                cig_letter = letter[-1]
                if cig_letter in cigar_dict.keys():
                    cigar_dict[cig_letter] += int(letter[:-1])
            for key,values in cigar_dict.items():
                total += int(values)
            pos = int(pos) + int(total)            
        cigar_dict.clear()
    return(pos)

#CODE
og_f = open(og_sam,"r")
nw_f = open(new_sam,"w")
umi_f = open(umi_file,"r")
prev_chrom = None
#List of known UMIs
umi_set = set()
for line in umi_f:
    umi_set.add(line.strip())

while True:
    S1 = read_sam(og_f)
    if S1 == 0:
        break
    #If the line starts with an @, it means its a header and should be passed to the new file
    if S1[0] == False:
        nw_f.write(S1[1])
    #For the actual records you need to pass it through functions    
    else:
        #First need to adjust the position for soft clipping in the original list. 
        curr_chrom,pos,stranded,cigar,umi,record = S1
        new_pos = pos_clip(pos, stranded, cigar)
        #Renaming variables to better understand the flow
        compare_data = (new_pos, stranded, umi)
        if curr_chrom != prev_chrom:
            prev_chrom = curr_chrom
            if prev_chrom != None:
                ban_set.clear()
        if umi in umi_set:
            if compare_data not in ban_set:
                ban_set.add(compare_data)
                nw_f.write(record)
                count["Unique"] += 1
            else:
                counting["Duplicate"] += 1
        else:
            counting["Wrong_UMI"] += 1
        
print(counting)
og_f.close()
nw_f.close()
umi_f.close()