# Scraper that scrapes EV vehicle data from the ev-database.org
import requests
from bs4 import BeautifulSoup
import pandas as pd

csv_fields = ["make", "model", "wh_km", "capacity_kwh"]
csv_rows = []
csv_filename = "../data/ev_energy_consumption.csv"

URL_CONSUMPTION = "https://ev-database.org/cheatsheet/energy-consumption-electric-car"
URL_CAPACITY = "https://ev-database.org/cheatsheet/useable-battery-capacity-electric-car"

def scrape_table(columns, url):
  df = pd.DataFrame(columns=columns)
  dom = BeautifulSoup(requests.get(url).content, 'html.parser')
  core_content = dom.find_all('div', class_='core-content')
  rows = core_content[0].find_all('tr')[1:]
  for row in rows:
    cells = row.find_all('td')
    appendable_row = cells[0].text.strip().split(' ', 1)
    appendable_row.append(cells[1].text.strip())

    appendable_row[0] = appendable_row[0].upper().strip()
    appendable_row[1] = appendable_row[1].upper().strip()

    df.loc[len(df)] = appendable_row

  return df

consumption_df = scrape_table(['make', 'model', 'wh_km'], URL_CONSUMPTION)
capacity_df = scrape_table(['make', 'model', 'capacity_kwh'], URL_CAPACITY)
merged_df = pd.merge(consumption_df, capacity_df, on=['make', 'model'])

merged_df.dropna().to_csv('../data/ev_energy_consumption.csv', index=False)


