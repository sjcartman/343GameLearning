import matplotlib.pyplot as plt
my_file = open("f1.txt","r")
f = my_file.readlines()
y = []
for i in f:
    y.append(float(i))
x = range(0,len(y))
plt.plot(x,y)
plt.xlabel('generation')
plt.ylabel('fitness')
plt.show()