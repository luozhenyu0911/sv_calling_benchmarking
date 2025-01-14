#!/usr/bin/python3
# Script for converting SVSIM .bedpe files into VCF format compatible with Structural Variation Engine
# Kyle Lesack
# 2020-01-29
# Requires VCF_Header.txt in same working directory that Python is invoked from
# NOTE: The reported SV length and coordinates vary between sv callers in SVE
# E.g. In Tigra, SV_LEN = end_coordinate - start_coordinate
# E.g. In cnmops, SV_LEN = end_coordinate - start_coordinate + 1


import argparse
import csv
import datetime
import re

parser = argparse.ArgumentParser()
parser.add_argument("input", help="input BED file (xxx.bedpe)")
parser.add_argument("sample_name", help="sample name, usually xxx part of xxx.event")

args = parser.parse_args()

date = datetime.datetime.now()
current_date = (str(date.year) + "-" + str(date.month) + "-" + str(date.day))

# Read VCF Header file
with open('VCF_Header.txt', 'r') as header_file :
	header_data = header_file.read()

# Replace the target string
header_data = header_data.replace('DATE', current_date) # Write the correct date in vcf header

REF_ALLELE = "N" # VCF files have a reference allele field, I don't think that SVE needs this. I don't want to find it in the FASTA file.
VARIANT_QUAL = "." # Simulated data, so a "." (unknown quality) is used
VARIANT_FILTER = "PASS" # Simulated data, so PASS is used for filter field
sample_name = args.sample_name

print(header_data, end='') # print the VCF header

with open(args.input) as fd:
	rd = csv.reader(fd, delimiter="\t", quotechar='"')

with open(args.input) as fd:
	rd = csv.reader(fd, delimiter="\t", quotechar='"')
	for row in rd:
		if "DEL" in row[6]:
			variant_type="DEL"
		elif "DUP" in row[6]:
			variant_type="DUP"
		elif "INV" in row[6]:
			variant_type="INV"
		else:
			print("Could not find variant type")

		chromosome = row[0]

		if variant_type == "DUP": # Coordinates reported for duplications coded differently than other variants
			end_coord = row[2]
			start_coord = row[4]
		else:
			start_coord = row[2]
			if variant_type == "DEL":
				end_coord = row[4]
			elif variant_type == "INV":
				end_coord = row[5]

		sv_length = abs(int(end_coord) - int(start_coord)) # Get the variant length

		if variant_type == "DEL":
			call_id_col=row[6]
			try:
				call_id = variant_type + re.search('DEL(.+?):', call_id_col).group(1) # Check if DEL in string
			except AttributeError:
				call_id = ''

		if variant_type == "DUP":
			call_id_col=row[6]
			try:
				call_id = variant_type + re.search('DUP(.+?):', call_id_col).group(1) # Check if DUP in string
			except AttributeError:
				call_id = ''

		if variant_type == "INV":
			call_id_col=row[6]
			try:
				call_id = variant_type + re.search('INV(.+?):', call_id_col).group(1) # Check if INV in string
			except AttributeError:
				call_id = ''

		variant_id = "SVSIM_" + call_id + "_" + str(sv_length) + "bp" # Rename variant name with size
		alt_allele = "<" + variant_type + ">" # ALT field is used to store the variant type in the VCF file
		variant_info = "DBVARID;" + "CALLID=" + variant_id + ";" + "SVTYPE=" + variant_type + ";" + "EXPERIMENT=1;" + "SAMPLE=" + sample_name + ";" + "END=" + end_coord + ";" + "REGION=NA"
		vcf_row = chromosome + "\t" + start_coord + "\t" + variant_id + "\t" + REF_ALLELE + "\t" + alt_allele + "\t" + VARIANT_QUAL + "\t" + VARIANT_FILTER + "\t" + variant_info # New row for vcf file

		if variant_type == "INV": # Inversion are included twice in each bedpe file. Each record alternates between + and - in the 9th column. The + strand is selected arbitrarily to print 1 record
			strand_info =  row[8]
			if strand_info == "+":
				print(vcf_row) # Print inversion line to screen
		else:
			print(vcf_row) # Print DEL and DUP lines to screen
