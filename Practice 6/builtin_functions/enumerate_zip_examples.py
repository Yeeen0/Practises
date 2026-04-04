import zipfile

with zipfile.ZipFile('example.zip', 'r') as z:
    for i, name in enumerate(z.namelist(), 1):
        print(f"{i}. {name}")