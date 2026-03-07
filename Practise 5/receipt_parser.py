import re

with open('/Users/enu/Documents/Practises/Practise 5/raw.txt', 'r', encoding='utf-8') as file:
    txt = file.read()

    # ex.1
# prices = r"^\d+,00$"
# result = re.findall(prices, txt, re.M)
# print(result) 

    # ex.2
# pattern = """^\d+\.\n(.+)"""
# x = re.findall(pattern, txt, re.M)
# print(x)

    # ex.3
# x = re.findall(r"^И.+:\n(.+)", txt, re.M)
# print(x)

    # ex.4
# data = re.findall(r"\d{2}\.\d{2}\.\d{4}", txt, re.M)
# time = re.findall(r"\d{2}\.\d{2}\.\d{2}", txt, re.M)
# print(data, time)

    # ex.5
# pattern = r"\b(наличные|карта|картой)\b"
# x = re.search(pattern, txt, re.M)
# print(x.group())