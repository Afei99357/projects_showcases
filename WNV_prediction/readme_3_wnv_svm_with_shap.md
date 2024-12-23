SVM Tuning and SHAP Analysis for West Nile Virus (WNV) Prediction

This Python script uses Support Vector Regression (SVR) to predict West Nile Virus (WNV) human disease cases in California counties. It integrates hyperparameter tuning results, evaluates model performance, and employs SHAP (SHapley Additive exPlanations) to analyze feature importance.

Features
	1.	Data Preprocessing:
	•	Scales features using StandardScaler.
	•	Drops unnecessary columns and handles missing values.
	2.	Hyperparameter Tuning:
	•	Loads the best hyperparameters for SVR from a precomputed CSV file.
	•	Evaluates model performance using  Q^2  (R-squared) and Root Mean Squared Error (RMSE).
	3.	Prediction Results:
	•	Predicts WNV human disease cases on test data (2019 and later).
	•	Saves predictions to a CSV file.
	4.	Feature Importance Analysis with SHAP:
	•	Generates global feature importance plots.
	•	Creates individual SHAP plots for each test sample, highlighting the contribution of features to predictions.

Input Data

1. Dataset
	•	Input File: data/CA_13_county_dataset/CA_13_counties_04_23_no_impute_daylight.csv
	•	Columns:
	•	Features: Environmental, land-use, and climate variables.
	•	Target: Human_Disease_Count (WNV human disease cases).
	•	Metadata: Year, month, county, latitude, longitude, etc.

2. Hyperparameter Tuning Results
	•	Input File: results/SVM/hyperparameter_tuning_best.csv
	•	Columns:
	•	tuning_year, C, epsilon, gamma, kernel.

Output

1. Predictions
	•	Output File: results/SVM/svm_predictions.csv
	•	Columns:
	•	FIPS, Month, Year, Human_Disease_Count, Predicted_Human_Disease_Count.

2. Tuning Results
	•	Output File: results/SVM/svm_tuning_results.csv
	•	Columns:
	•	tuning_year, q2, RMSE, C, epsilon, gamma, kernel.

3. SHAP Plots
	•	Global Plot:
	•	Path: results/SVM/shap_plots/svm_global_shap_plot.png.
	•	Local Plots:
	•	Directory: results/SVM/shap_plots/individual/.
	•	Files: One plot per test sample, named as svm_local_shap_plot_<year>_<month>_<FIPS>.png.