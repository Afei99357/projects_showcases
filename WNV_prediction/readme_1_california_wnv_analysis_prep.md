California West Nile Virus Data Preprocessing Script

This Python script preprocesses and integrates various datasets to analyze West Nile Virus (WNV) cases in California counties from 2004 to 2023. The processed dataset includes information about WNV human cases, population data, climate conditions, land use, and El Niño/La Niña events, enabling further analysis or modeling of WNV dynamics.

Features
	•	Data Cleaning: Preprocesses county names, handles missing data, and ensures consistent formatting.
	•	Case Summarization: Aggregates WNV human case data by year, month, and county.
	•	Data Enrichment:
	•	Adds FIPS codes, geographic information (latitude and longitude), and avian phylodiversity data.
	•	Integrates population data for California counties.
	•	Merges environmental variables (bird, mosquito, and horse WNV counts) from CDC data.
	•	Incorporates El Niño/La Niña Oceanic Niño Index (ONI) data to indicate climatic conditions.
	•	Maps land use types (e.g., forests, urban areas) based on geographic coordinates using raster datasets.
	•	Adds climate variables (e.g., temperature, wind speed, precipitation) from NetCDF climate files.

Input Files
	1.	WNV Case Data: CSV file with WNV human case data by county and month (wnv_county_onsetmonth_2004-2023.csv).
	2.	FIPS Data: CSV file containing county-level FIPS codes, latitude, longitude, and avian phylodiversity (cali_week_wnnd.csv).
	3.	Population Data: CSV file with population information for California counties (disease_human_neuroinvasive_whole_year.csv).
	4.	CDC Environmental Data: CSV file with bird, mosquito, and horse WNV counts by state and month (combine_cdc_all_environmental_variable_all_2024.csv).
	5.	El Niño/La Niña Data: CSV file with historical ONI values (Historical_El_Nino_or_La_Nina_episodes_1950_present.csv).
	6.	Land Use Data: Raster files representing various land use types (consensus_full_class_1.tif to consensus_full_class_12.tif).
	7.	Climate Data: NetCDF file with monthly climate variables (new_land_monthly_data_from_1999_to_2024_02.nc).

Output

The script produces a consolidated CSV file (CA_13_counties_04_23_impute_0.csv) containing:
	•	Year, Month, County, FIPS code
	•	Latitude, Longitude
	•	WNV human case counts (Human_Disease_Count)
	•	Avian phylodiversity
	•	Population data
	•	Environmental variables (e.g., bird/mosquito/horse WNV counts)
	•	ONI values for El Niño/La Niña conditions
	•	Land use types (e.g., forest, urban, water)
	•	Climate variables (e.g., temperature, wind speed, precipitation)