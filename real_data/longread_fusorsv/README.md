# cendr_benchmarking

Scripts for comparing the predicted structural variants from CeNDR shortread (caller = FusorSV) and longread (callers = Assemblytics, MUM&Co, pbsv, Sniffles, and SVIM)

# Requirements

* Python 3
* bedtools (tested using v2.30.0)
* Python libraries
        * pybedtools (tested using v0.9.0)
        * pandas (tested using v1.1.3)
        * upsetplot (tested using v0.6.0)

## Steps

tar -zxvf 0_data_1.tar.gz

tar -zxvf 0_data_2.tar.gz

tar -zxvf 0_data_3.tar.gz

sh 00_scripts/0_prepare_data/0_clean_files.sh; rm *.log

sh 00_scripts/0_prepare_data/1_make_your_beds.sh | sort -u 2>&1 | tee -a logs/1_make_your_beds.log # convert output from caller to bed file with necessary data

sh 00_scripts/0_prepare_data/2_sort_cluster_beds.sh 2>&1 | tee -a logs/2_sort_cluster_beds.log # cluster variant calls to find duplicates

sh 00_scripts/0_prepare_data/3_decluster.sh 2>&1 | tee -a logs/3_decluster.log # Choose best variant call from calls with overlapping coords

sh 00_scripts/1_analyze_overlap/4_get_gene_overlap.sh | tee -a logs/4_get_gene_overlap.log # Get SVs that span structural variants

sh 00_scripts/1_analyze_overlap/5_get_caller_overlap.sh | tee -a logs/5_get_caller_overlap.log # Get overlap between callers

sh 00_scripts/1_analyze_overlap/6_create_upset_plots.sh | tee -a logs/6_create_upset_plots.log # Create upset plot
