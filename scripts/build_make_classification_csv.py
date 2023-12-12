# Script that normalizes the car gas classification for hybrid/gas vehicles
import csv

ev_source_filename = "../data/ev_energy_consumption.csv"
regular_vehicles_source_filename = "../data/vehicle_co2_emissions.csv"

combined_filename = "../data/vehicle_classification.csv"
combined_rows = []

fuel_type_map = {
    "X": "REGULAR_GASOLINE",
    "Z": "PREMIUM_GASOLINE",
    "D": "DIESEL",
    "E": "ETHANOL",
    "N": "NATURAL_GAS",
    "EV": "ELECTRIC"
}

with open(regular_vehicles_source_filename, mode="r") as csv_file:
    csv_reader = csv.DictReader(csv_file, delimiter=",")
    for i, row in enumerate(csv_reader):
        if i == 0:
            continue
        combined_rows.append([row["Make"], row["Model"], fuel_type_map[row["Fuel Type"]]])

with open(ev_source_filename, mode="r") as csv_file:
    csv_reader = csv.DictReader(csv_file, delimiter=",")
    for i, row in enumerate(csv_reader):
        if i == 0:
            continue
        combined_rows.append([row["Make"].upper(), row["Model"].upper(), fuel_type_map["EV"]])

combined_rows = sorted(combined_rows, key = lambda x : x[0])

with open(combined_filename, "w") as csv_file:
    csv_writer = csv.writer(csv_file)
    csv_writer.writerow(["Make", "Model", "Class"])
    csv_writer.writerows(combined_rows)

