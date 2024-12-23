# Clear the workspace
rm(list = ls())

# Load necessary libraries
library(vcfR)        # For VCF file handling
library(adegenet)    # For genlight objects and allele matrix processing
library(vegan)       # For PCA and RDA
library(qvalue)      # For post-processing LFMM output
library(psych)       # For correlation panels
library(ggplot2)     # For data visualization

# Define base directory for relative paths
base_dir <- "data/landscape_genetics"
output_dir <- "results/landscape_genetics"

# Ensure output directories exist
dir.create(output_dir, recursive = TRUE, showWarnings = FALSE)

# ===================
# Load Genetic Data
# ===================

# Load the VCF file
vcf_file <- file.path(base_dir, "bi_20missing_filtSNP_maf_005.recode.vcf")
vcf <- read.vcfR(vcf_file, verbose = FALSE)

# Convert VCF to genlight object and extract allele matrix
SNP_genlight <- vcfR2genlight(vcf)
allele_matrix <- tab(SNP_genlight, freq = FALSE, NA.method = "asis")

# Impute missing values in the allele matrix
allele_matrix <- apply(allele_matrix, 2, function(x) {
  replace(x, is.na(x), as.numeric(names(which.max(table(x)))))
})

# ==========================
# Load Environmental Data
# ==========================

# Load the environmental data
env_file <- file.path(base_dir, "Ctarsalis_sample_w_GPS_climate_average_new_filtered_id_region.csv")
env <- read.csv(env_file, row.names = 1)

# Remove unused columns and ensure alignment of genotypes and environmental data
env <- env[, !(names(env) %in% c("locID", "State", "City", "date"))]
env$vcfID <- as.character(env$vcfID)

# Subset predictors and rename columns
predictors <- env[, 18:30]
colnames(predictors) <- c(
  "eastward_wind", "northward_wind", "temperature",
  "evaporation_from_bare_soil", "high_vegetation",
  "low_vegetation", "water_retention_capacity",
  "snowfall", "surface_net_solar_radiation", "surface_runoff",
  "evaporation", "total_precipitation", "volumetric_soil_water_layer1"
)

# Check and remove multicollinearity
vif_values <- usdm::vif(predictors)
predictors <- subset(predictors, select = -c(
  surface_net_solar_radiation, evaporation_from_bare_soil,
  total_precipitation, volumetric_soil_water_layer1, snowfall
))

# ==========================
# Redundancy Analysis (RDA)
# ==========================

# Perform RDA
rda_result <- rda(allele_matrix ~ ., data = predictors, scale = TRUE)

# Extract and adjust R2
adjusted_r2 <- RsquareAdj(rda_result)

# Summarize RDA results
rda_summary <- summary(rda_result)
eigenvalues <- rda_summary$concon$importance[1, 1:5] / sum(rda_summary$concon$importance)

# Plot Screeplot
screeplot_file <- file.path(output_dir, "RDA_scree_plot.png")
png(screeplot_file, width = 8, height = 6, units = "in", res = 300)
screeplot(rda_result)
dev.off()

# ===============================
# Visualize RDA Axes and Results
# ===============================

# Define color mappings
region_colors <- c("hotpink", "skyblue", "forestgreen", "goldenrod")
predictor_colors <- c(
  "evaporation" = "#000000", "eastward_wind" = "#E69F00", 
  "northward_wind" = "#F0E442", "temperature" = "#56B4E9",
  "high_vegetation" = "#009E73", "low_vegetation" = "#D55E00",
  "water_retention_capacity" = "#CC79A7", "surface_runoff" = "#0072B2"
)

# Plot axes 1 & 2
rda_axes_file <- file.path(output_dir, "RDA_region_ax_1_2.png")
png(rda_axes_file, width = 8, height = 6, units = "in", res = 300)
plot(rda_result, type = "n", scaling = 3,
     xlab = paste("RDA1 (", round(eigenvalues[1] * 100, 2), "%)"),
     ylab = paste("RDA2 (", round(eigenvalues[2] * 100, 2), "%)"))
points(rda_result, display = "species", pch = 20, cex = 0.7, col = "gray32", scaling = 3)
legend("bottomright", legend = names(region_colors), col = region_colors, pch = 21, pt.bg = region_colors, bty = "n")
dev.off()

# ===============================
# Identify and Save Candidate SNPs
# ===============================

# Extract SNP loadings for the first 4 axes
snp_loadings <- scores(rda_result, choices = 1:4, display = "species")

# Define a function to identify outliers
identify_outliers <- function(x, z = 3) {
  limits <- mean(x) + c(-1, 1) * z * sd(x)
  which(x < limits[1] | x > limits[2])
}

# Identify candidate SNPs
candidate_snps <- list(
  axis1 = identify_outliers(snp_loadings[, 1]),
  axis2 = identify_outliers(snp_loadings[, 2]),
  axis3 = identify_outliers(snp_loadings[, 3]),
  axis4 = identify_outliers(snp_loadings[, 4])
)

# Save candidate SNPs to CSV
candidate_file <- file.path(output_dir, "rda_analysis_candidates.csv")
write.csv(candidate_snps, candidate_file, row.names = FALSE)

# ===============================
# Visualize SNPs with Predictors
# ===============================

# Plot SNPs with predictor associations
snps_plot_file <- file.path(output_dir, "RDA_snps_plot_ax_1_2.png")
png(snps_plot_file, width = 8, height = 6, units = "in", res = 300)
plot(rda_result, type = "n", scaling = 3,
     xlab = paste("RDA1 (", round(eigenvalues[1] * 100, 2), "%)"),
     ylab = paste("RDA2 (", round(eigenvalues[2] * 100, 2), "%)"))
points(rda_result, display = "species", pch = 21, cex = 1, col = "white", bg = predictor_colors, scaling = 3)
dev.off()

# ===================
# Additional Analysis
# ===================

# Add correlations between candidate SNPs and predictors
correlations <- apply(predictors, 2, function(x) cor(x, allele_matrix[, candidate_snps$axis1]))

# Save results
correlation_file <- file.path(output_dir, "rda_candidate_correlations.csv")
write.csv(correlations, correlation_file, row.names = FALSE)