import json

with open('sample-data.json', 'r', encoding = 'utf-8') as file:
    data = json.dump(file, indent = 4)

print(data)