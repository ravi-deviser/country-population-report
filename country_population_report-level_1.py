# ==========================================================
# Country Population Report Level 1
# Author : Ravi Deviser
# ==========================================================

import requests
import json
import csv
from openpyxl import Workbook

api_url = "https://restcountries.com/v3.1/all?fields=name,region,population"
def fetch_countries():
    resp = requests.get(api_url, timeout = 15)

    if resp.status_code != 200:
        print("API Failed with Status:", resp.status_code)
        return[]
    
    return resp.json()


def clean_and_group(countries):
    grouped = {}

    for c in countries:
        name = c.get("name",{}).get("common", "Unknown")

        region = c.get("region") or "Other"

        population = c.get("population", 0)


        country_data = {
                "Country":name,
                "Population": population
        } 


        if region not in grouped:
            grouped[region] = {
                "countries": [],
                "total_population": 0
            }

        grouped[region]["countries"].append(country_data)

        grouped[region]["total_population"] += population

    return grouped





# Save file in JSON 

def save_json(data, filename = "country_population_report_level_1.json"):
    with open(filename, "w", encoding = "utf-8") as f:
        json.dump(data, f, indent = 4)

    print("JSON file saved as :", filename)


# CSV file save 

def save_csv(data, filename = "country_population_report_level_1.csv"):
    with open(filename, "w", newline = "", encoding = "utf-8") as f:
        writer = csv.writer(f)

        writer.writerow(["Region", "Country", "Population"])

        for region, info in data.items():
            for c in info["countries"]:
                writer.writerow([
                    region,
                    c["Country"],
                    c["Population"]
                ])
    print("CSV file saved as:", filename)


# Excel report 

def save_excel(data, filename = "country_population_report_level_1.xlsx"):

    wb = Workbook()
    wb.remove(wb.active)

    for region, info in data.items():
        ws = wb.create_sheet(title = region[:31])

        ws.append(["Country", "Population"])

        for c in info["countries"]:
            ws.append([
                c["Country"],
                c["Population"]
            ])

        ws.append([])

        ws.append([
            "Total Population",
            info["total_population"]
        ])
    
    wb.save(filename)

    print("Excel file saved as :", filename)


# -----------------------------------------------------------------------------
# Main Function
# -----------------------------------------------------------------------------
def main():
    raw_data = fetch_countries()

    if not raw_data:
        print("NO DATA FETCHED")
        return
    
    grouped_data = clean_and_group(raw_data)

    # file save
    save_json(grouped_data)
    save_csv(grouped_data)
    save_excel(grouped_data)

    print("Data Extracted Successfully")

main()

