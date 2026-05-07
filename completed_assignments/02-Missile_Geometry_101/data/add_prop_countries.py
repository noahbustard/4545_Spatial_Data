"""
Hackish script to add more properties per country to our countries.geojson file.
"""

import json
import glob


def create_data_by_countries():
    with open("countries.geojson", "r") as f:
        data = json.load(f)

    country_dict = {}

    for country in data["features"]:
        country_dict[country["properties"]["ADMIN"]] = {}

    with open("data_by_country.json", "w") as f:
        json.dump(country_dict, f)


def smart_cast(value: str):
    try:
        return int(value)
    except ValueError:
        try:
            return float(value)
        except ValueError:
            return value  # leave as string


replace = {
    "expectancy": "lifeExpectancy",
    "landlocked": "isLandLocked",
    "population": "population",
    "temperature": "avgTemperatureCels",
    "density": "popDensity",
}

if __name__ == "__main__":

    with open("data_by_country.json", "r") as f:
        country_data = json.load(f)

    files = glob.glob("./country-by-datatype/*.json")
    for file in files:
        with open(file, "r") as f:
            data = json.load(f)

        print(file)
        for info in data:

            print(info)
            name = info["country"]
            del info["country"]

            if not name in country_data:
                country_data[name] = {}

            if not "name" in country_data[name]:
                country_data[name]["name"] = name
            key = list(info.keys())[0]
            val = list(info.values())[0]
            if val:
                country_data[name][replace[key]] = smart_cast(str(val))
            else:
                country_data[name][replace[key]] = val
            print(country_data[name])
    with open("data_by_country2.json", "w") as f:
        json.dump(country_data, f, indent=3)

    with open("countries.geojson", "r") as f:
        data = json.load(f)

    for country in data["features"]:
        if len(country_data[country["properties"]["ADMIN"]]) > 0:
            country["properties"] = country_data[country["properties"]["ADMIN"]]
            country["properties"]["ISO_A3"] = country["properties"]["ISO_A3"]
        else:
            country["properties"]["name"] = country["properties"]["ADMIN"]
            del country["properties"]["ADMIN"]

    with open("countries2.geojson", "w") as f:
        json.dump(data, f, indent=3)
