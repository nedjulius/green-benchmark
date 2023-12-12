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

COLUMNS = [
  'make',
  'model',
  'engine_size',
  'vehicle_class',
  'manifacture_co2',
  'co2_gkm',
  'util_z',
  'manifacture_z',
  'base_rating'
]

CO2_EMISSIONS_VEHICLE_GAS_PATH = '../data/vehicle_co2_emissions.csv'

LITHIUM_CO2_PATH = '../data/lithium_battery_manufacturing.csv'

# Function to get column for some Z-score
def get_column_z_score(colname, emissions_dataframe):
  stdev = emissions_dataframe[colname].std()
  mean = emissions_dataframe[colname].mean()
  df = emissions_dataframe.copy()
  
  return df[colname].apply(lambda x: round((x - mean) / stdev, 2))

def get_gas_and_hybrid_manifacturing_column(emissions_dataframe):
  df = emissions_dataframe.copy()
  engine_emissions = df['engine_size'] * 200
  vehicle_base_emissions = df['vehicle_class'].apply(lambda v: VEHICLE_CLASS_EMISSIONS[v])

  return engine_emissions + vehicle_base_emissions

def include_hybrid_battery_manifacturing_cost(emissions_dataframe):
  df = emissions_dataframe.copy()
  n = 'manifacture_co2'
  # Add emissions for the additional hybrid battery
  # We are using medians, because of the difficulty acquiring different
  # battery sizes for various hybrids
  df[n] = df.apply(lambda row: row[n] + HYBRID_BATTERY_EMISSIONS if 'hybrid' in row['model'].lower() else row[n], axis=1)

  return df[n]

# Combine util and manifacture Z scores and shift them to 10-scale
def calculate_composite_rating(emissions_dataframe):
  df = emissions_dataframe.copy()
  composite_col = df['util_z'] + df['manifacture_z']
  max_score = max(composite_col)
  print(max_score)
  min_score = min(composite_col)
  print(min_score)

  return composite_col.apply(lambda x: 10 - (((10 * (x - min_score)) / (max_score - min_score))))

def get_gas_and_hybrid_vehicle_emissions_dataframe():
  emissions_dataframe = pd.DataFrame(columns=COLUMNS)
  emissions_dataframe_raw = pd.read_csv(CO2_EMISSIONS_VEHICLE_GAS_PATH)

  direct_col_map = {
    'make': 0,
    'model': 1,
    'vehicle_class': 2,
    'engine_size': 3,
    'co2_gkm': 11 
  }

  # Mapping existing columns
  for colname, index in direct_col_map.items():
    emissions_dataframe[colname] = emissions_dataframe_raw.iloc[:, index]
  
  # Create manifacturing data for gas and hybrid vehicles
  emissions_dataframe['manifacture_co2'] = get_gas_and_hybrid_manifacturing_column(emissions_dataframe)

  # Add additional battery manifacturing costs for hybrids
  emissions_dataframe['manifacture_co2'] = include_hybrid_battery_manifacturing_cost(emissions_dataframe)

  # Get Z-score for manifacturing emissions
  emissions_dataframe['manifacture_z'] = get_column_z_score('manifacture_co2', emissions_dataframe)

  # Get Z-score for CO2 grams per KM emissions (utilization)
  emissions_dataframe['util_z'] = get_column_z_score('co2_gkm', emissions_dataframe)

  # Finally, calculate composite rating on a 10-scale
  emissions_dataframe['base_rating'] = calculate_composite_rating(emissions_dataframe)

  print(emissions_dataframe.loc[emissions_dataframe['base_rating'].idxmin()])
  print(max(emissions_dataframe['base_rating']))
  emissions_dataframe.to_csv('../data/test.csv', index=False)

  return emissions_dataframe

get_gas_and_hybrid_vehicle_emissions_dataframe()

def get_electric_vehicle_emissions_dataframe():
  return

def main():
  return

# Calculation that gets emission rating based on CO2
def calculate_vehicle_emission_rating(emissions, worst_case_emissions, decimal_places = 2):
  rating = 10 - (emissions / worst_case_emissions)
  rounded_rating = rating.round(decimal_places)
  return rounded_rating.clip(lower=0)

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
