import numpy as np

with open("nodes_coordinates.csv", encoding="GBK") as f:
    fo = f.readlines()
    x = np.array(fo[1].strip("x_coor,").strip("\n").split(","))
    y = np.array(fo[2].strip("y_coor,").strip("\n").split(","))
    z = np.array(fo[3].strip("z_demand,").strip("\n").split(","))

arr1 = []
for i in np.arange(len(x)):
    for j in np.arange(len(x)):
        a = np.sqrt((eval(x[i]) - eval(x[j])) ** 2 + (eval(y[i]) - eval(y[j])) ** 2)
        arr1.append(a)

arr2 = np.array(arr1)
arr3 = arr2.reshape(len(x), len(x))
