SVM Bootstrapping for West Nile Virus (WNV) Prediction

This Python script uses Support Vector Regression (SVR) to predict West Nile Virus (WNV) human disease cases in California counties. It applies bootstrapping to train the model on multiple samples and evaluates the model’s performance using metrics such as  Q^2  (R-squared) and Root Mean Squared Error (RMSE).

Features
	•	Bootstrapping:
	•	Generates 1,000 bootstrapped samples from training data for robust evaluation.
	•	SVM Regression:
	•	Implements SVR with predefined hyperparameters (from 2009 optimization).
	•	Performance Metrics:
	•	Evaluates  Q^2  (R-squared) and RMSE for each iteration.
	•	Calculates mean values and confidence intervals for the metrics.
	•	Visualization:
	•	Generates histograms of  Q^2  and RMSE distributions with 95% confidence intervals.

Input Data

The script requires a dataset containing WNV-related features and human disease case counts. It uses the following file:
	•	Input File: data/CA_13_county_dataset/CA_13_counties_04_23_no_impute.csv
	•	Columns:
	•	Features: Various environmental, land-use, and climate variables.
	•	Target: Human_Disease_Count (WNV human disease cases).
	•	Metadata: Year, month, county, latitude, longitude, etc.

Output

The script saves performance evaluation plots in the following directory:
	•	Output Directory: results/plots/train_before_2019_predict_2019/using_2009_model_best_hyperparameter
	•	Q2 Distribution Plot: bootstrapping_svm_q2_distribution.png
	•	RMSE Distribution Plot: bootstrapping_svm_rmse_distribution.png