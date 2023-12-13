#
# This file contains the primary logic that calculates the CO2 emission based rating
# for vehicles. 
#
import numpy as np
import pandas as pd

WH_TO_CO2_CONVERSION_RATIO = 0.3712

MEDIAN_HYBRID_BATTERY_CAPACITY_KWH = 12.5
# Rough estimate for hybrid battery emissions
HYBRID_BATTERY_EMISSIONS = MEDIAN_HYBRID_BATTERY_CAPACITY_KWH * 73

# Approximates for the vehicle class CO2 emissions (kg CO2)
VEHICLE_CLASS_EMISSIONS = {
  'TWO-SEATER': 4400,
  'MINICOMPACT': 4400,
  'SUBCOMPACT': 4500,
  'COMPACT': 4800,
  'MID-SIZE': 5000,
  'FULL-SIZE': 5300,
  'SUV - SMALL': 5600,
  'SUV - STANDARD': 5800,
  'PICKUP TRUCK - SMALL': 5600,
  'PICKUP TRUCK - STANDARD': 5800,
  'STATION WAGON - SMALL': 5600,
  'STATION WAGON - MID-SIZE': 5800,
  'MINIVAN': 5900,
  'VAN - CARGO': 5900,
  'VAN - PASSENGER': 6000,
  'SPECIAL PURPOSE VEHICLE': 6000
}

# Ratio to convert engine size in liters to manifacturing emissions in CO2 kg
LITERS_TO_KG_CO2_APPROX_RATIO = 200

# Estimates of kgs of CO2-eq emitted per 1 kWh battery capacity production
KGS_CO2_PER_BATTERY_CAPACITY_KWH_RATIO = 160

COLUMNS = [
  'make',
  'model',
  'engine_size',
  'vehicle_class',
  'manifacture_co2',
  'co2_gkm',
  'util_z',
  'manifacture_z',
  'base_rating',
  'rating_desc'
]

CO2_EMISSIONS_VEHICLE_GAS_PATH = '../data/vehicle_co2_emissions.csv'

EV_ENERGY_CONSUMPTION_PATH = '../data/ev_energy_consumption.csv'

US_ELECTRIC_VEHICLE_DATA_PATH = '../data/us_electric_car_data.csv'

LITHIUM_CO2_PATH = '../data/lithium_battery_manufacturing.csv'


# Combine util and manifacture Z scores and shift them to 10-scale
def calculate_composite_rating(emissions_dataframe):
  df = emissions_dataframe.copy()
  composite_col = df['util_z'] + df['manifacture_z']
  max_score = max(composite_col)
  min_score = min(composite_col)

  return composite_col.apply(lambda x: 10 - (((10 * (x - min_score)) / (max_score - min_score))))

# Function to get column for some Z-score
def get_column_z_score(colname, emissions_dataframe):
  stdev = emissions_dataframe[colname].std()
  mean = emissions_dataframe[colname].mean()
  df = emissions_dataframe.copy()
  
  return df[colname].apply(lambda x: round((x - mean) / stdev, 2))


def get_gas_and_hybrid_manifacturing_column(emissions_dataframe):
  df = emissions_dataframe.copy()
  engine_emissions = df['engine_size'] * LITERS_TO_KG_CO2_APPROX_RATIO
  vehicle_base_emissions = df['vehicle_class'].apply(lambda v: VEHICLE_CLASS_EMISSIONS[v])

  return engine_emissions + vehicle_base_emissions

# Add data for EVs manifacturing costs in CO2 emissions
def get_ev_manifacturing_column(emissions_dataframe):
  df = emissions_dataframe.copy()
  # We stored battery capacity in kWh in the "manifacture_co2" field
  df['manifacture_co2'] = (df['manifacture_co2'] * KGS_CO2_PER_BATTERY_CAPACITY_KWH_RATIO).astype(int)

  return df


# Get all vehicles that are plug-in hybrid
def get_hybrid_vehicles():
  df = pd.read_csv(US_ELECTRIC_VEHICLE_DATA_PATH)
  filtered_df = df[df['Electric Vehicle Type'] == 'Plug-in Hybrid Electric Vehicle   ']
  filtered_df = filtered_df.drop_duplicates(subset=['Model'])

  return filtered_df[['Make', 'Model']]

# Callback that filters the hybrids if they exist in hybrid DF
def filter_hybrids_row(row, hybrids):
  n = 'manifacture_co2'
  model = row['model']

  if any(hybrids['Model'].isin([model.upper()])) or 'hybrid' in model.lower():
    return row[n] + HYBRID_BATTERY_EMISSIONS

  return row[n]

def include_hybrid_battery_manifacturing_cost(emissions_dataframe):
  hybrids = get_hybrid_vehicles()
  df = emissions_dataframe.copy()
  n = 'manifacture_co2'
  # Add emissions for the additional hybrid battery
  # We are using medians, because of the difficulty acquiring different
  # battery sizes for various hybrids
  df[n] = df.apply(filter_hybrids_row, axis=1, args=(hybrids,))

  return df[n]


def get_df_and_map(direct_col_map, filepath):
  df = pd.DataFrame(columns=COLUMNS)
  df_raw = pd.read_csv(filepath)

  for colname, index in direct_col_map.items():
    df[colname] = df_raw.iloc[:, index]
  
  df['model'] = df['model'].str.upper()
  df['make'] = df['make'].str.upper()

  return df

def get_ev_emissions_df():
  ev_df = get_df_and_map({
    'make': 0,
    'model': 1,
    'co2_gkm': 2,
    # Mapping battery capacity to this field for intermediary
    'manifacture_co2': 3
  }, EV_ENERGY_CONSUMPTION_PATH)

  # Convert WH/km to CO2 grams per km
  ev_df['co2_gkm'] = (ev_df['co2_gkm'] * WH_TO_CO2_CONVERSION_RATIO).astype(int)

  return ev_df


# Get total rating percentiles with descriptions
def get_vehicle_rating_brackets(car_rating_dataframe):
  worst = np.percentile(np.array(car_rating_dataframe['base_rating']), 10)
  bad = np.percentile(np.array(car_rating_dataframe['base_rating']), 30)
  good = np.percentile(np.array(car_rating_dataframe['base_rating']), 70)
  best = np.percentile(np.array(car_rating_dataframe['base_rating']), 90)

  return {
    'terrible': [0, worst],
    'bad': [worst, bad],
    'mediocre': [bad, good],
    'good': [good, best],
  }

# Determine description for a given rating
def get_vehicle_rating_description(curr_rating, rating_brackets):
  if curr_rating <= rating_brackets['terrible'][1]:
    return 'terrible'
  if curr_rating > rating_brackets['bad'][0] and curr_rating <= rating_brackets['bad'][1]:
    return 'bad'
  if curr_rating > rating_brackets['mediocre'][0] and curr_rating <= rating_brackets['mediocre'][1]:
    return 'mediocre'
  if curr_rating > rating_brackets['good'][0] and curr_rating <= rating_brackets['good'][1]:
    return 'good'
  return 'best'


def create_rating_dataframe():
  ev_emissions_dataframe = get_ev_emissions_df()
  ev_emissions_dataframe = get_ev_manifacturing_column(ev_emissions_dataframe)

  # Map CO2 emissions
  gas_emissions_dataframe = get_df_and_map({
    'make': 0,
    'model': 1,
    'vehicle_class': 2,
    'engine_size': 3,
    'co2_gkm': 11 
  }, CO2_EMISSIONS_VEHICLE_GAS_PATH)
  
  # Create manifacturing data for gas and hybrid vehicles
  gas_emissions_dataframe['manifacture_co2'] = get_gas_and_hybrid_manifacturing_column(gas_emissions_dataframe)

  # Merge EV and gas dataframes
  emissions_dataframe = pd.concat([ev_emissions_dataframe, gas_emissions_dataframe], ignore_index=True)

  # Add additional battery manifacturing costs for hybrids
  emissions_dataframe['manifacture_co2'] = include_hybrid_battery_manifacturing_cost(emissions_dataframe)

  # Get Z-score for manifacturing emissions
  emissions_dataframe['manifacture_z'] = get_column_z_score('manifacture_co2', emissions_dataframe)

  # Get Z-score for CO2 grams per KM emissions (utilization)
  emissions_dataframe['util_z'] = get_column_z_score('co2_gkm', emissions_dataframe)

  # Finally, calculate composite rating on a 10-scale
  emissions_dataframe['base_rating'] = calculate_composite_rating(emissions_dataframe)

  # Add bracket ratings
  rating_brackets = get_vehicle_rating_brackets(emissions_dataframe)
  emissions_dataframe['rating_desc'] = emissions_dataframe['base_rating'].apply(get_vehicle_rating_description, args=(rating_brackets,))
  emissions_dataframe.drop_duplicates(subset=['make', 'model', 'engine_size'], keep='first', inplace=True)

  return emissions_dataframe
