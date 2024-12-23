Model Comparison Plot

This Python script visualizes and compares the performance of different machine learning models (SVM, Random Forest, and HGBR) in terms of  Q^2  and RMSE across various tuning years.

Features
	1.	Data Loading:
	•	Reads pre-computed  Q^2  and RMSE results for:
	•	Support Vector Machines (SVM)
	•	Random Forest (RF)
	•	Histogram-Based Gradient Boosting Regressor (HGBR)
	2.	Visualization:
	•	Generates line plots comparing  Q^2  and RMSE metrics across tuning years for the three models.
	3.	Output:
	•	Saves plots to the results/plots directory:
	•	 Q^2  comparison: multi_models_q2_comparison.png
	•	RMSE comparison: multi_models_rmse_comparison.png