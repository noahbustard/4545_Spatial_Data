

import json

with open("world_cities_large.json","r") as f:
    data = json.load(f)
    
print(len(data))

sum = 0
for cc,cities in data.items():
    print(cc,end=" ")
    print(len(cities))
    sum += len(cities)

print(f"Total Cities: {sum}")