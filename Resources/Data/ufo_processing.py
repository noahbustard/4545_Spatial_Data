import json 

with open("ufo_01.geojson", "r") as f:
    data = json.load(f)
    
for banana in data["features"]:
    print(banana["properties"]["city"])
    
    
    
