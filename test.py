import random

random.seed(10)
what = []
for i in range(10):
    what.append(random.randrange(2, 10))
print(what)
print(type(what))
