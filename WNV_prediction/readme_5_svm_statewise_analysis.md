SVM Statewise Analysis with Subsampling

This Python script trains and evaluates a Support Vector Machine (SVM) model to analyze West Nile Virus (WNV) neuroinvasive disease cases for each U.S. state. It uses subsampling to balance classes and generates various metrics and visualizations for performance assessment.

Features
	1.	Data Preprocessing:
	•	Cleans the population data by removing commas and spaces, converting it to numeric.
	•	Handles missing values in the dataset.
	2.	Class Balancing:
	•	Balances the dataset by either:
	•	Downsampling the majority class, or
	•	Upsampling the minority class.
	3.	SVM Training and Evaluation:
	•	Trains an SVM model for each state on data from before 2018.
	•	Evaluates the model on data from 2018 onward using:
	•	Mean Squared Error (MSE)
	•	Mean Squared Log Error (MSLE)
	•	 Q^2  (R-squared) score.
	4.	Visualization:
	•	Creates bar plots for:
	•	MSLE and  Q^2  scores by state.
	•	Positive  Q^2  scores by state.
	•	Total and non-zero data rows by state.
	5.	Output:
	•	Saves results and visualizations to SVM_each_state_subsampling in the project directory.
