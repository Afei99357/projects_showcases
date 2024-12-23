import os
import pandas as pd
from sklearn.svm import SVR
from sklearn.preprocessing import StandardScaler
from sklearn.utils import resample
from sklearn import metrics
from plotly.subplots import make_subplots
import plotly.graph_objects as go

# Set base directory and output directory
BASE_DIR = "/Users/ericliao/Desktop/WNV_project_files/WNV/CDC_data"
RESULT_DIR = os.path.join(BASE_DIR, "human/result/SVM_each_state_subsampling")
os.makedirs(RESULT_DIR, exist_ok=True)

# Load dataset
data_path = os.path.join(BASE_DIR, "human/cdc_human_1999_to_2023/WNV_human_and_non_human_yearly_climate_demographic_bird.csv")
data = pd.read_csv(data_path, index_col=0)

# Clean and preprocess the population column
data["Population"] = data["Population"].str.replace(",", "").str.strip()
data["Population"] = pd.to_numeric(data["Population"], errors='coerce')

# Function to balance classes by subsampling
def balance_classes(data, target_column):
    """
    Balances the dataset classes by downsampling the majority class
    or upsampling the minority class to match the smaller class size.
    """
    majority = data[data[target_column] == 0]
    minority = data[data[target_column] > 0]

    if len(majority) > len(minority):
        majority_downsampled = resample(majority, replace=False, n_samples=len(minority), random_state=123)
        return pd.concat([majority_downsampled, minority])
    else:
        minority_upsampled = resample(minority, replace=True, n_samples=len(majority), random_state=123)
        return pd.concat([majority, minority_upsampled])

# Function to train and evaluate an SVM model
def svm_model(data, target_column, state):
    """
    Trains an SVM model for a specific state and evaluates it on test data.
    """
    state_data = data[data["State"] == state]
    date_index = state_data.columns.get_loc("Date")

    predictors = state_data.iloc[:, date_index + 1:].copy()
    predictors['Year'] = state_data['Year']
    predictors[target_column] = state_data[target_column]
    predictors = predictors.dropna().reset_index(drop=True)

    # Balance classes
    predictors = balance_classes(predictors, target_column)

    # Train/test split
    train = predictors[predictors["Year"] < 2018]
    test = predictors[predictors["Year"] >= 2018]

    train_labels = train.pop(target_column).values
    test_labels = test.pop(target_column).values
    train.pop("Year")
    test.pop("Year")

    if train.empty or test.empty:
        print(f"State: {state} has no data for training or testing.")
        return None, None, None, None, None

    # Standardize data
    scaler = StandardScaler()
    train = scaler.fit_transform(train)
    test = scaler.transform(test)

    # Train SVM model
    model = SVR(epsilon=0.3, gamma=0.002, kernel="rbf", C=100)
    model.fit(train, train_labels)
    predictions = model.predict(test)
    predictions = [max(0, p) for p in predictions]

    # Calculate evaluation metrics
    mse = metrics.mean_squared_error(test_labels, predictions)
    msle = metrics.mean_squared_log_error(test_labels, predictions)
    q2 = metrics.r2_score(test_labels, predictions)

    print(f"State: {state}, MSE: {mse}, MSLE: {msle}, Q2: {q2}")
    return mse, msle, q2, len(predictors), len(predictors[predictors[target_column] > 0])

# Evaluate SVM for each state
state_results = {}
for state in data["State"].unique():
    mse, msle, q2, total_rows, non_zero_rows = svm_model(data, "Neuroinvasive_disease_cases", state)
    if mse is not None:
        state_results[state] = {"mse": mse, "msle": msle, "q2": q2, "total_rows": total_rows, "non_zero_rows": non_zero_rows}

# Prepare results for visualization
results_df = pd.DataFrame.from_dict(state_results, orient='index').reset_index()
results_df.rename(columns={"index": "State"}, inplace=True)

# Map full state names to abbreviations
state_map = {  # Add more states as necessary
    "alabama": "AL", "california": "CA", "texas": "TX", "new york": "NY"
}
results_df["State"] = results_df["State"].map(state_map)

# Visualize results
def create_plot(data, x_col, y_col, title, file_name):
    fig = go.Figure(data=go.Bar(x=data[x_col], y=data[y_col], name=y_col))
    fig.update_layout(title_text=title, height=600, width=1000)
    fig.write_image(os.path.join(RESULT_DIR, file_name), scale=2)

create_plot(results_df, "State", "msle", "MSLE by State Using SVM with Subsampling", "msle_by_state.png")
create_plot(results_df, "State", "q2", "Q2 by State Using SVM with Subsampling", "q2_by_state.png")

# Filter positive Q2 results and visualize
positive_q2_df = results_df[results_df["q2"] > 0]
create_plot(positive_q2_df, "State", "q2", "Positive Q2 by State Using SVM with Subsampling", "positive_q2_by_state.png")