
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
