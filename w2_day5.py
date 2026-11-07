#import json

#from unittest import result

import requests
#from sqlalchemy import table

url = "https://api.postcodes.io/postcodes/B32 2RT".replace(" ", "%20")
response = requests.get(url, timeout=20)

print(response.status_code)     # 200 = success, 404 = not found, 500 = their problem
print(response.text[:200])      # the raw text that came back

data = response.json()          # turns JSON text into Python dicts and lists
print(data["status"], data["result"]["latitude"], data["result"]["longitude"])






weather_url = "https://archive-api.open-meteo.com/v1/archive"
params = {
    "latitude": 52.4862,
    "longitude": -1.8904,
    "start_date": "2026-09-01",
    "end_date": "2026-09-30",
    "daily": "temperature_2m_max,temperature_2m_min,precipitation_sum",
    "timezone": "Europe/London",
}
r = requests.get(weather_url, params=params, timeout=30)
print(r.status_code)
print(r.url)      # print the URL to see how params were glued together


import pandas as pd

weather = r.json()
daily = weather["daily"]          # a dict of lists
print(list(daily.keys()))

df = pd.DataFrame(daily)         # each list becomes a column, perfectly aligned
print(df.head())
print(df.shape)                  # (30, 4)

df["time"] = pd.to_datetime(df["time"])

print(df["temperature_2m_max"].max())        # 23.6
print(df["temperature_2m_max"].mean().round(2))   # 19.89
print(df.loc[df["precipitation_sum"].idxmax()])
print(df["precipitation_sum"].sum().round(1))     # 58.4 mm of rain


postcodes = ["B1 1BB", "B2 4QA", "B4 7XG", "B5 4BU",
             "B15 2TT", "B29 6NA", "B37 7YN", "CV1 1AA"]

r = requests.post("https://api.postcodes.io/postcodes",
                  json={"postcodes": postcodes}, timeout=20)
results = r.json()["result"]

rows = []
for item in results:
    res = item["result"]
    if res is None:                 # THIS happens in real life - one bad postcode
        print(f"⚠️ No match for {item['query']}")
        continue
    rows.append({
        "postcode": item["query"],
        "lat": res["latitude"],
        "lon": res["longitude"],
        "district": res["admin_district"],
        "region": res["region"],
    })

pc = pd.DataFrame(rows)
print(pc.shape)          # (7, 5) - CV1 1AA is invalid, we skipped it
print(pc.head())
pc.to_csv("birmingham_postcodes_lookup.csv", index=False)


print("--- Day 5 Practice ---")

#  Day 5 Practice
#  1. Look up your own postcode with postcodes.io. What district and region comes back?
postcode = "B32 2RT"  # replace with
p = requests.get(f"https://api.postcodes.io/postcodes/{postcode.replace(' ', '%20')}", timeout=20)
if p.status_code == 200:
    result = p.json()["result"]
    print(f"District: {result['admin_district']}, Region: {result['region']}")



#  2. What HTTP status code does an invalid postcode return? Try /postcodes/ZZ1 1ZZ and read response.json()["error"]
invalid_postcode = "ZZ1 1ZZ"
q = requests.get(f"https://api.postcodes.io/postcodes/{invalid_postcode.replace(' ', '%20')}", timeout=20)
if q.status_code == 404:
    print(f"Error for {invalid_postcode}: {q.json()['error']}")

#  3. Fetch Birmingham weather for a full month and convert it to a DataFrame — how many rows?
month_params = {
    "latitude": 52.4862,
    "longitude": -1.8904,
    "start_date": "2026-09-01",
    "end_date": "2026-09-30",
    "daily": "temperature_2m_max,temperature_2m_min,precipitation_sum",
    "timezone": "Europe/London",
}
r = requests.get("https://archive-api.open-meteo.com/v1/archive", params=month_params, timeout=30)
r.raise_for_status()
df_month = pd.DataFrame(r.json()["daily"])
print(df_month.shape[0])  # Number of rows in the DataFrame

#  4. What was the warmest day and the wettest day in that month?
warmest_day = df_month.loc[df_month["temperature_2m_max"].idxmax()]
wettest_day = df_month.loc[df_month["precipitation_sum"].idxmax()]
print(f"Warmest day: {warmest_day['time']} with max temp {warmest_day['temperature_2m_max']}°C")
print(f"Wettest day: {wettest_day['time']} with precipitation {wettest_day['precipitation_sum']}mm")

# 5. Include the maximum 10 m wind speed in the archive weather request.
month_params["daily"] += ",wind_speed_10m_max"
r = requests.get("https://archive-api.open-meteo.com/v1/archive", params=month_params, timeout=30)
r.raise_for_status()
df_month = pd.DataFrame(r.json()["daily"])
print(df_month.columns.tolist())

# 6. Save the raw JSON to a file with json.dump, then read it back later. Why do real pipelines keep the raw response?
import json
with open("weather_raw.json", "w") as f:
    json.dump(weather, f)
# Why: APIs change, rate-limit or go down. Saving raw responses lets you

# re-run your pipeline, debug, and prove what the source said on a given day.
# (Also: you don't hammer someone's free API while developing.)

# 7. Bulk-look up 5 more postcodes of your choice (e.g. where you've lived). Which ones return null?
additional_postcodes = ["B1 1AA", "B2 2BB", "B3 3CC", "B4 4DD", "B5 5EE"]
for pc in additional_postcodes:
    resp = requests.get(f"https://api.postcodes.io/postcodes/{pc.replace(' ', '%20')}", timeout=20)
    if resp.status_code == 200:
        result = resp.json()["result"]
        print(f"District: {result['admin_district']}, Region: {result['region']}")
    else:
        print(f"⚠️ No match for {pc}")

# 8. Wrap the whole weather fetch in try/except requests.exceptions.RequestException and print a friendly message
try:
    r = requests.get(weather_url, params=params, timeout=30)
    r.raise_for_status()
    df = pd.DataFrame(r.json()["daily"])
except requests.exceptions.RequestException as e:
    print(f"API call failed: {e}")
