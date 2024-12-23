import os
from sklearn.svm import SVR
from sklearn import metrics
import pandas as pd
import shap
from matplotlib import pyplot as plt
import numpy as np
from sklearn.preprocessing import StandardScaler

# Set the base directory for relative paths
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Define file paths
DATA_PATH = os.path.join(BASE_DIR, "data", "CA_13_county_dataset", "CA_13_counties_04_23_no_impute_daylight.csv")
HYPERPARAMS_PATH = os.path.join(BASE_DIR, "results", "SVM", "hyperparameter_tuning_best.csv")
RESULTS_DIR = os.path.join(BASE_DIR, "results", "SVM")
PREDICTION_RESULTS_PATH = os.path.join(RESULTS_DIR, "svm_predictions.csv")
TUNING_RESULTS_PATH = os.path.join(RESULTS_DIR, "svm_tuning_results.csv")
GLOBAL_SHAP_PLOT_PATH = os.path.join(RESULTS_DIR, "shap_plots", "svm_global_shap_plot.png")
LOCAL_SHAP_PLOTS_DIR = os.path.join(RESULTS_DIR, "shap_plots", "individual")

# Ensure directories exist
os.makedirs(RESULTS_DIR, exist_ok=True)
os.makedirs(os.path.dirname(GLOBAL_SHAP_PLOT_PATH), exist_ok=True)
os.makedirs(LOCAL_SHAP_PLOTS_DIR, exist_ok=True)

# Load the dataset
data = pd.read_csv(DATA_PATH, index_col=False)

# Drop unnecessary columns and target columns
data.drop(columns=["Date", "County", "Latitude", "Longitude", "Total_Bird_WNV_Count", "Mos_WNV_Count", "Horse_WNV_Count"], inplace=True, errors='ignore')

# Drop columns with all NaN or zero variance
data.dropna(axis=1, how='all', inplace=True)
zero_variance_cols = data.columns[data.var() == 0]
print(f"Columns with zero variance: {zero_variance_cols.tolist()}")
data = data.loc[:, data.var() != 0]

# Impute missing values in the target column
data["Human_Disease_Count"].fillna(0, inplace=True)

# Split data into training and testing sets
train = data[data['Year'] < 2019].dropna().reset_index(drop=True)
test = data[data['Year'] >= 2019].dropna().reset_index(drop=True)

# Separate labels and features
train_labels = train.pop("Human_Disease_Count").values
test_labels = test.pop("Human_Disease_Count").values

# Drop non-feature columns
test_FIPS_list = test.pop("FIPS").values
test_month_list = test.pop("Month").values
test_year_list = test.pop("Year").values
train.drop(columns=["Month", "FIPS", "Year"], inplace=True)

# Scale data
scaler = StandardScaler()
train = pd.DataFrame(scaler.fit_transform(train), columns=train.columns)
test = pd.DataFrame(scaler.transform(test), columns=test.columns)

# Load hyperparameters
best_hyperparameters = pd.read_csv(HYPERPARAMS_PATH)

# Initialize results storage
tuning_year_q2_rmse_list = []

for index, row in best_hyperparameters.iterrows():
    tuning_year = row['tuning_year']
    model = SVR(
        C=float(row['C']),
        epsilon=float(row['epsilon']),
        gamma=row['gamma'],
        kernel=row['kernel']
    )

    # Train the model and predict
    model.fit(train, train_labels)
    predictions = model.predict(test)

    # Save predictions
    prediction_results = pd.DataFrame({
        "FIPS": test_FIPS_list,
        "Month": test_month_list,
        "Year": test_year_list,
        "Human_Disease_Count": test_labels,
        "Predicted_Human_Disease_Count": predictions
    })
    prediction_results.to_csv(PREDICTION_RESULTS_PATH, index=False)

    # Calculate metrics
    q2 = metrics.r2_score(test_labels, predictions)
    rmse = np.sqrt(metrics.mean_squared_error(test_labels, predictions))
    tuning_year_q2_rmse_list.append([tuning_year, q2, rmse, row['C'], row['epsilon'], row['gamma'], row['kernel']])
    print(f"Tuning Year: {tuning_year}, Q^2: {q2:.2f}, RMSE: {rmse:.2f}")

# Save tuning results
tuning_results_df = pd.DataFrame(
    tuning_year_q2_rmse_list, columns=["tuning_year", "q2", "RMSE", "C", "epsilon", "gamma", "kernel"]
)
tuning_results_df.to_csv(TUNING_RESULTS_PATH, index=False)

# Define SHAP explainer
explainer = shap.Explainer(lambda X: model.predict(X), test)(test)

# Plot global SHAP values
plt.figure(figsize=(30, 10))
shap.plots.bar(explainer, show=False, max_display=18)
plt.tight_layout()
plt.savefig(GLOBAL_SHAP_PLOT_PATH)
plt.close()

# Plot individual SHAP values
for i in range(len(test)):
    plt.figure(figsize=(60, 20))
    plt.subplots_adjust(left=0.4, right=0.6, top=0.9, bottom=0.1)

    shap.plots.bar(explainer[i], show=False, max_display=17)
    sample_plot_path = os.path.join(
        LOCAL_SHAP_PLOTS_DIR, f"svm_local_shap_plot_{test_year_list[i]}_{test_month_list[i]}_{test_FIPS_list[i]}.png"
    )
    plt.tight_layout()
    plt.savefig(sample_plot_path)
    plt.close()