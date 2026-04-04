from functools import reduce

nums = [1, 2, 3, 4, 5]

squared = list(map(lambda x: x**2, nums))  # [1, 4, 9, 16, 25]

evens = list(filter(lambda x: x % 2 == 0, nums))  # [2, 4]

total = reduce(lambda x, y: x + y, nums)  # 15

print(f"Квадраты: {squared}\nЧетные: {evens}\nСумма: {total}")