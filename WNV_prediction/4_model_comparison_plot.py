import os
import pandas as pd
from matplotlib import pyplot as plt

# Define base directory and paths
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
RESULTS_DIR = os.path.join(BASE_DIR, "results", "plots")
os.makedirs(RESULTS_DIR, exist_ok=True)

# Define file paths for model results
svm_results_path = os.path.join(
    BASE_DIR, "data", "SVM", "hyperparameter_tuning_q2_rmse.csv"
)
rf_results_path = os.path.join(
    BASE_DIR, "data", "RF", "hyperparameter_tuning_q2_rmse.csv"
)
hgbr_results_path = os.path.join(
    BASE_DIR, "data", "HGBR", "hgbr_tuning_q2_rmse.csv"
)

# Load results
svm_results = pd.read_csv(svm_results_path)
rf_results = pd.read_csv(rf_results_path)
hgbr_results = pd.read_csv(hgbr_results_path)

# Plot Q^2 comparison between SVM, RF, and HGBR
plt.figure(figsize=(10, 5))

plt.plot(svm_results["tuning_year"], svm_results["q2"], label="SVM", color="red")
plt.plot(rf_results["tuning_year"], rf_results["q2"], label="RF", color="blue")
plt.plot(hgbr_results["tuning_year"], hgbr_results["q2"], label="HGBR", color="green")

plt.xlabel("Tuning year")
plt.ylabel("$Q^2$")
plt.title("$Q^2$ Comparison Between SVM, RF, and HGBR")
plt.xticks(svm_results["tuning_year"].astype(int))
plt.legend(loc="upper left")

q2_comparison_path = os.path.join(RESULTS_DIR, "multi_models_q2_comparison.png")
plt.savefig(q2_comparison_path, dpi=300)
plt.show()

# Plot RMSE comparison between SVM, RF, and HGBR
plt.figure(figsize=(10, 5))

plt.plot(svm_results["tuning_year"], svm_results["RMSE"], label="SVM", color="red")
plt.plot(rf_results["tuning_year"], rf_results["RMSE"], label="RF", color="blue")
plt.plot(hgbr_results["tuning_year"], hgbr_results["RMSE"], label="HGBR", color="green")

plt.xlabel("Tuning year")
plt.ylabel("RMSE")
plt.title("RMSE Comparison Between SVM, RF, and HGBR")
plt.xticks(svm_results["tuning_year"].astype(int))
plt.legend(loc="upper left")

rmse_comparison_path = os.path.join(RESULTS_DIR, "multi_models_rmse_comparison.png")
plt.savefig(rmse_comparison_path, dpi=300)
plt.show()