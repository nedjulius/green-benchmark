# Scraper that scrapes EV vehicle data from the ev-database.org
import requests
import csv
from bs4 import BeautifulSoup

csv_fields = ["Make", "Model", "WhKm"]
csv_rows = []
csv_filename = "../data/ev_energy_consumption.csv"

URL = "https://ev-database.org/cheatsheet/energy-consumption-electric-car"
page = requests.get(URL)

soup = BeautifulSoup(page.content, "html.parser")
core_content = soup.find_all("div", class_="core-content")
rows = core_content[0].find_all("tr")[1:]

for row in rows:
    cells = row.find_all("td")
    csv_row = cells[0].text.strip().split(" ", 1) 
    # assumes that first word in the cell is the make
    csv_row.append(cells[1].text.strip())
    csv_rows.append(csv_row)

with open(csv_filename, 'w') as csvfile:
    csvwriter = csv.writer(csvfile)
    csvwriter.writerow(csv_fields)
    csvwriter.writerows(csv_rows)

