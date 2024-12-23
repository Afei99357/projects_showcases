import os
import pandas as pd
import xarray as xr
import cv2
import numpy as np

# Set the base directory for relative paths
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Define relative paths
CA_DATASET_PATH = os.path.join(BASE_DIR, "data", "CA_13_county_dataset")
FIPS_DATA_PATH = os.path.join(BASE_DIR, "data", "cali_week_wnnd.csv")
POPULATION_DATA_PATH = os.path.join(BASE_DIR, "data", "yearly", "disease_human_neuroinvasive_whole_year.csv")
CDC_DATA_PATH = os.path.join(BASE_DIR, "data", "monthly", "combine_cdc_all_environmental_variable_all_2024.csv")
ENSO_DATA_PATH = os.path.join(BASE_DIR, "data", "Historical_El_Nino_or_La_Nina_episodes_1950_present.csv")
LAND_USE_DATA_PATH = os.path.join(BASE_DIR, "data", "climate", "consensus_land_cover_data")
CLIMATE_DATA_PATH = os.path.join(BASE_DIR, "data", "climate", "new_land_monthly_data_from_1999_to_2024_02.nc")
OUTPUT_FILE_PATH = os.path.join(CA_DATASET_PATH, "CA_13_counties_04_23_impute_0.csv")

# Load the California WNV dataset
data_california = pd.read_csv(
    os.path.join(CA_DATASET_PATH, "wnv_county_onsetmonth_2004-2023.csv"),
    sep=",", index_col=0
)

# Preprocess the "County" column
data_california["County"] = data_california["County"].str.lower().str.strip()

# Select relevant columns and group data by Year, Month, and County
data_california_new = (
    data_california[["County", "Cases", "Year", "Month"]]
    .groupby(["Year", "Month", "County"], as_index=False)
    .sum()
)

# Create a full dataset with all combinations of Year, Month, and County
years = range(2004, 2024)
months = range(1, 13)
counties = data_california_new["County"].unique()

full_data = pd.DataFrame(
    [(year, month, county) for year in years for month in months for county in counties],
    columns=["Year", "Month", "County"]
)

# Merge with the existing data, filling missing cases with NaN
data_california_new = full_data.merge(data_california_new, how="left", on=["Year", "Month", "County"])

# Print ratio of missing values in the Cases column
print("NaN ratio in Cases:", data_california_new["Cases"].isna().mean())

# Load FIPS and geographic data
fips_df = pd.read_csv(FIPS_DATA_PATH, sep=",")[["County", "FIPS", "Latitude", "Longitude", "Avian Phylodiversity"]].drop_duplicates()

# Merge FIPS data
data_california_new = data_california_new.merge(fips_df, how="left", on="County")
print("Missing FIPS values:", data_california_new["FIPS"].isna().sum())

# Reorder columns
data = data_california_new[["Year", "Month", "County", "FIPS", "Latitude", "Longitude", "Cases", "Avian Phylodiversity"]]

# Load population data and preprocess
df_population = pd.read_csv(POPULATION_DATA_PATH, sep=",")
df_population = (
    df_population[df_population["State"] == "California"]
    .query("Year == 2020")
    [["County", "Population"]]
)
df_population["County"] = df_population["County"].str.lower().str.strip()

# Merge population data
data = data.merge(df_population, how="left", on="County")

# Rename "Cases" column to "Human_Disease_Count"
data.rename(columns={"Cases": "Human_Disease_Count"}, inplace=True)

# Load CDC WNV data and merge
df_cdc = pd.read_csv(CDC_DATA_PATH, sep=",").query("State == 'california'")[
    ["Total_Bird_WNV_Count", "Mos_WNV_Count", "Horse_WNV_Count", "Year", "Month", "County"]
]
data = data.merge(df_cdc, how="left", on=["Year", "Month", "County"])

# Impute missing values in "Human_Disease_Count"
data["Human_Disease_Count"].fillna(0, inplace=True)

# Add El Nino/La Nina data
print("Adding El Nino/La Nina data...")
df_enso = pd.read_csv(ENSO_DATA_PATH, sep=",")
month_names = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]
data["ONI"] = data.apply(
    lambda row: df_enso.loc[df_enso["Year"] == row["Year"], month_names[row["Month"] - 1]].values[0],
    axis=1
)
print("Finished adding El Nino/La Nina data.")

# Add land use data
print("Adding land use data...")
land_use_types = [
    "Evergreen/Deciduous Needleleaf Trees", "Evergreen Broadleaf Trees", "Deciduous Broadleaf Trees",
    "Mixed Trees", "Shrub", "Herbaceous", "Culture/Managed", "Wetland", "Urban/Built",
    "Snow/Ice", "Barren", "Water"
]
images = [
    cv2.imread(os.path.join(LAND_USE_DATA_PATH, f"consensus_full_class_{i}.tif"))[:, :, 0]
    for i in range(1, 13)
]
latitude_da = xr.DataArray(data["Latitude"].values, dims="county")
longitude_da = xr.DataArray(data["Longitude"].values, dims="county")
dataset = xr.Dataset(
    {land_use: xr.DataArray(im, coords=[np.linspace(90, -56, im.shape[0]), np.linspace(-180, 180, im.shape[1])], dims=["latitude", "longitude"])
     for land_use, im in zip(land_use_types, images)}
)
for land_use in land_use_types:
    data[land_use] = dataset[land_use].sel(latitude=latitude_da, longitude=longitude_da, method="nearest").values
print("Finished adding land use data.")

# Add climate data
print("Adding climate data...")
data["Date"] = pd.to_datetime(data[["Year", "Month"]].assign(day=1))
time_da = xr.DataArray(data["Date"].values.astype("datetime64[D]"), dims="county")
climate_ds = xr.open_dataset(CLIMATE_DATA_PATH).sortby("time")
variables = ["u10", "v10", "t2m", "lai_hv", "lai_lv", "src", "sf", "sro", "tp"]
shifted_vars = [f"{var}_1m_shift" for var in variables]
for var, shifted_var in zip(variables, shifted_vars):
    data[shifted_var] = climate_ds[var].sel(
        latitude=latitude_da, longitude=longitude_da, expver=1, method="nearest"
    ).shift(time=1).sel(time=time_da, method="nearest").values
print("Finished adding climate data.")

# Save final dataset
data.to_csv(OUTPUT_FILE_PATH, index=False)