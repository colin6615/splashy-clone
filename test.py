"""
from operator import attrgetter


class geeks:
    def __init__(self, experience, salary):
        self.experience = experience
        self.salary = salary


object1 = geeks(2, 50000)
object2 = geeks(3, 60000)
object3 = geeks(1, 20000)
object4 = geeks(4, 75000)

l = [object4, object3, object2, object1]
max_attr = max(l, key=attrgetter("salary"))
print(max_attr.salary)
"""
from operator import attrgetter

pad_with_min_y = min(Pad.list, key=attrgetter("center_y")))
print(pad_with_min_y.center_y)