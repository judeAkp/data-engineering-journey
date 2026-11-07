# Build w2_pipeline.py that:

# Reads postcodes from birmingham_postcodes.csv
# Looks up lat/lon for each with postcodes.io (skipping invalid ones)
# For each valid postcode, fetches one month of daily weather from Open-Meteo (Sept 2026 works — use a past month, not today)
# Combines everything into one DataFrame with columns: postcode, area, district, date, temp_max, temp_min, precipitation, fetched_at
# Saves to weather_birmingham.csv (and raw JSON to data/raw/)
# Loads it into SQL Server table dbo.weather_birmingham
# Prints a 5-line summary: rows loaded, date range, warmest area, wettest area, total rain

# Build order (don't skip the sequence)
#30 min — Get one postcode working end-to-end and print the DataFrame. One record before many.
# import os

# import pandas as pd
# import requests
# import time
# from sqlalchemy import create_engine
# from sqlalchemy.engine import URL

# start, end = "2026-09-01", "2026-09-30"


# def get_database_engine():
#     required_settings = ("SQL_SERVER", "SQL_DATABASE", "SQL_USER", "SQL_PASSWORD")
#     missing_settings = [name for name in required_settings if not os.environ.get(name)]
#     if missing_settings:
#         raise RuntimeError(
#             "Set these environment variables before loading to SQL Server: "
#             + ", ".join(missing_settings)
#         )

#     connection_url = URL.create(
#         "mssql+pyodbc",
#         username=os.environ["SQL_USER"],
#         password=os.environ["SQL_PASSWORD"],
#         host=os.environ["SQL_SERVER"],
#         port=1433,
#         database=os.environ["SQL_DATABASE"],
#         query={"driver": "ODBC Driver 17 for SQL Server"},
#     )
#     return create_engine(connection_url)


# def get_postcode_info(postcode):
#     p = requests.get(f"https://api.postcodes.io/postcodes/{postcode.replace(' ', '%20')}", timeout=20)
#     if p.status_code == 200:
#         result = p.json()["result"]
#         return {
#             "postcode": postcode,
#             "lat": result["latitude"],
#             "lon": result["longitude"],
#             "district": result["admin_district"],
#             "region": result["region"],
#         }
#     else:
#         print(f"⚠️ No match for {postcode}: {p.json()['error']}")
#         return None

# def get_weather(lat, lon, start, end):
#     month_params = {
#         "latitude": lat,
#         "longitude": lon,
#         "start_date": start,
#         "end_date": end,
#         "daily": "temperature_2m_max,temperature_2m_min,precipitation_sum",
#         "timezone": "Europe/London",
#     }
#     r = requests.get("https://api.open-meteo.com/v1/forecast", params=month_params, timeout=20)
#     return pd.DataFrame(r.json()["daily"])

# def main():
#     postcodes_df = pd.read_csv("birmingham_postcodes.csv")
#     all_data = []

#     for postcode in postcodes_df['postcode']:
#         info = get_postcode_info(postcode)
#         if info:
#             weather_df = get_weather(info['lat'], info['lon'], start, end)
#             weather_df['postcode'] = info['postcode']
#             weather_df['district'] = info['district']
#             weather_df['region'] = info['region']
#             weather_df['fetched_at'] = pd.Timestamp.now()
#             all_data.append(weather_df)
#             time.sleep(1)  # Respect API rate limits

#     final_df = pd.concat(all_data, ignore_index=True)
#     final_df.rename(columns={
#         'temperature_2m_max': 'temp_max',
#         'temperature_2m_min': 'temp_min',
#         'precipitation_sum': 'precipitation'
#     }, inplace=True)

#     final_df.to_csv("weather_birmingham.csv", index=False)

#     engine = get_database_engine()
#     try:
#         final_df.to_sql(
#             "weather_birmingham",
#             con=engine,
#             schema="dbo",
#             if_exists="replace",
#             index=False,
#         )
#     finally:
#         engine.dispose()

#     print(f"Rows loaded: {len(final_df)}")
#     print(f"Date range: {final_df['time'].min()} to {final_df['time'].max()}")
#     warmest_area = final_df.loc[final_df['temp_max'].idxmax()]['district']
#     wettest_area = final_df.loc[final_df['precipitation'].idxmax()]['district']
#     total_rain = final_df['precipitation'].sum()
#     print(f"Total rain: {total_rain:.2f} mm")
#     print(f"Warmest area: {warmest_area}")


# if __name__ == "__main__":
#     main()

import time
import requests
import pandas as pd
from sqlalchemy import create_engine

START, END = "2026-09-01", "2026-09-30"


def get_coordinates(postcodes):
    r = requests.post("https://api.postcodes.io/postcodes",
                      json={"postcodes": postcodes}, timeout=20)
    r.raise_for_status()
    rows = []
    for item in r.json()["result"]:
        res = item["result"]
        if res is None:
            print(f"⚠️ Skipping invalid postcode {item['query']}")
            continue
        rows.append({"postcode": item["query"], "lat": res["latitude"],
                     "lon": res["longitude"], "district": res["admin_district"]})
    return pd.DataFrame(rows)


def get_weather(lat, lon, start, end):
    params = {"latitude": lat, "longitude": lon, "start_date": start,
              "end_date": end, "daily": "temperature_2m_max,temperature_2m_min,"
              "precipitation_sum", "timezone": "Europe/London"}
    r = requests.get("https://archive-api.open-meteo.com/v1/archive",
                     params=params, timeout=30)
    r.raise_for_status()
    return pd.DataFrame(r.json()["daily"])


def main():
    areas = pd.read_csv("birmingham_postcodes.csv")
    coords = get_coordinates(areas["postcode"].tolist())
    coords = coords.merge(areas, on="postcode", how="left")

    frames = []
    for _, row in coords.iterrows():
        try:
            w = get_weather(row["lat"], row["lon"], START, END)
        except requests.exceptions.RequestException as e:
            print(f"⚠️ Weather failed for {row['postcode']}: {e}")
            continue
        w["postcode"] = row["postcode"]
        w["area"] = row["area"]
        w["district"] = row["district"]
        frames.append(w)
        print(f"✅ {row['postcode']} - {len(w)} days")
        time.sleep(1)

    df = pd.concat(frames, ignore_index=True)
    df = df.rename(columns={"time": "date", "temperature_2m_max": "temp_max",
                            "temperature_2m_min": "temp_min",
                            "precipitation_sum": "precipitation"})
    df["date"] = pd.to_datetime(df["date"])
    df["fetched_at"] = pd.Timestamp.now()
    df = df.sort_values(["postcode", "date"]).reset_index(drop=True)

    df.to_csv("weather_birmingham.csv", index=False)

    engine = create_engine("mssql+pyodbc://localhost/DE_Learning"
                           "?driver=ODBC+Driver+18+for+SQL+Server"
                           "&Encrypt=yes&TrustServerCertificate=yes")
    df.to_sql("weather_birmingham", engine, if_exists="replace", index=False)

    print(f"\n📊 Rows loaded: {len(df)}")
    print(f"📅 Date range: {df['date'].min().date()} to {df['date'].max().date()}")
    area_max = df.groupby("area")["temp_max"].max()
    print(f"🌡️ Warmest area: {area_max.idxmax()} ({area_max.max()}°C)")
    print(f"☔ Total rain: {df['precipitation'].sum():.1f} mm")


if __name__ == "__main__":
    main()
