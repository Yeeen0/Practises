    # ex.1
# def my_gen(x):
#     a = 0
#     while a <= x:
#         yield a * a
#         a += 1

# N = int(input())
# gen = iter(my_gen(N))
# print(next(gen))
# print(next(gen))
# print(next(gen))

    # or

# def my_gen(x):
#     for a in range(x): yield a * a

# N = int(input())
# print(list(my_gen(N)))


    # ex.2
# def even_gen(x):
#     if x % 2 == 1: x -= 1
#     for i in range(0, x + 1, 2):
#         yield str(i)

# n = int(input())
# gen = even_gen(n)
# print(", ".join(gen))


    # ex.3
# def my_gen(x):
#     for i in range(x):
#         if i % 3 == 0 and i % 4 == 0:
#             yield str(i)

# n = int(input())
# gen = my_gen(n)
# print(", ".join(gen))
        

    # ex.4
# def squares(x, y):
#     for i in range(x, y):
#         yield i * i
# a = int(input())
# b = int(input())
# gen = squares(a, b)
# for i in gen:
#     print(i)


    # ex.5
# def my_gen(x):
#     for i in range(x, 0, -1):
#         yield str(i)
# n = int(input())
# gen = my_gen(n)
# print(", ".join(gen))