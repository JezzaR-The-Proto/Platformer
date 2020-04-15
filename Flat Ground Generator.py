# Platformer Flat Ground Generator
import json
data = {}
data["ground"] = []
x = 35
while x < 1315:
    y = 35
    data["ground"].append({
        'x': x,
        'y': 35,
        'tex': "ground"
    })
    x += 70
with open('level1.json', 'w') as outfile:
    json.dump(data, outfile)
