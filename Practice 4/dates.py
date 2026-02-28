import datetime

    # ex.1
# x = datetime.datetime.now()
# fivedays = x - datetime.timedelta(days = 5)
# print(fivedays)


    # ex.2
# x = datetime.datetime.now()
# print(x - datetime.timedelta(days = 1))
# print(x)
# print(x + datetime.timedelta(days = 1))


    # ex.3
# n = int(input())
# x = datetime.datetime.now()
# print(x - datetime.timedelta(microseconds = n))


    # ex.4
# d1 = datetime.date.fromisoformat(input("YYYY-MM-DD: "))
# d2 = datetime.date.fromisoformat(input("YYYY-MM-DD: "))
# time = d1 - d2
# print(time.total_seconds())
