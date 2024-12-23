Redundancy Analysis (RDA) for Landscape Genetics

This R script performs Redundancy Analysis (RDA) to investigate the relationship between genetic variation and environmental predictors in a landscape genetics context. The analysis identifies candidate SNPs associated with local adaptation and visualizes the results using various plots.

Features
	1.	Genetic Data Processing:
	•	Reads genetic data from a VCF file and converts it into a genlight object.
	•	Imputes missing values in the allele matrix with the most frequent allele.
	2.	Environmental Data Integration:
	•	Loads and preprocesses environmental predictor data.
	•	Removes highly correlated variables to avoid multicollinearity.
	3.	Redundancy Analysis (RDA):
	•	Performs RDA to relate genetic variation to environmental predictors.
	•	Computes adjusted  R^2  values and examines canonical eigenvalues.
	•	Identifies environmental predictors most correlated with RDA axes.
	4.	Visualization:
	•	Creates scree plots of canonical eigenvalues.
	•	Generates RDA plots for SNPs and environmental predictors across axes.
	•	Highlights candidate SNPs and their association with environmental variables.
	5.	Candidate SNP Identification:
	•	Identifies SNPs that load significantly on the RDA axes.
	•	Correlates candidate SNPs with environmental predictors.
	•	Outputs results to CSV files.

Directory Structure

Input Files
	1.	Genetic Data:
	•	VCF file: data/landscape_genetics/bi_20missing_filtSNP_maf_005.recode.vcf
	2.	Environmental Data:
	•	CSV file: data/landscape_genetics/Ctarsalis_sample_w_GPS_climate_average_new_filtered_id_region.csv

Output Files
	1.	Plots:
	•	Scree plot: results/landscape_genetics/RDA_scree_plot.png
	•	RDA axes and SNP plots: results/landscape_genetics/RDA_region_ax_1_2.png, etc.
	2.	CSV Files:
	•	Candidate SNPs: results/landscape_genetics/rda_analysis_candidates.csv
	•	SNP-environment correlations: results/landscape_genetics/rda_candidate_correlations.csv
