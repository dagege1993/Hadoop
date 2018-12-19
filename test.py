import random

list2 = []
TrainingPercent = 0.8
for i in range(3116):
    rd = random.random()
    if rd < TrainingPercent:
        list2.append(1)
print(len(list2))
