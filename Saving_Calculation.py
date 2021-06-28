import copy
from Distance_Calculation import *


def saving(i, j):  # 计算任意两点之间的节约值
    saving_value = arr3[i][len(arr3) - 3] + arr3[j][len(arr3) - 3] - arr3[i][j]
    return saving_value


ls = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30,
      31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 58,
      59, 60, 61, 62, 63, 64, 65, 66, 67, 68, 69, 70, 71, 72, 73, 74, 75, 76, 77, 78, 79, 80, 81, 82]  # 这是车库负责供应除冰液的节点

cell = []
k = 0

for i in ls:
    lt = copy.deepcopy(ls)
    lt = list(filter(lambda x: x > i, lt))
    for j in lt:
        cell.append([[i + 1, j + 1], saving(i, j)])
cell.sort(key=lambda x: x[1], reverse=-1)

routes = [0]
demand = []

idx = 0  # 注意使用计数器，避免使while成为死循环！
additional = 0  # 之所以要定义这个additional变量，是因为每条子路径确定后，routes变量的就又“固定”了一部分，对于新合并的子路径，其起始位置不再是1了
while len(routes) - 1000 < len(ls) and idx < 50000:  # 这里使用序贯节约里程法，相较于并行节约里程法，它的编程实现更加简单，每次搜索只生成一条路径。
    # 只要表示路径的routes变量的长度比节点数量要少，就会一直遍历整个cell列表
    # 这里减了1000，是为了保证每个节点都能被配送。后续会删去因此而产生的多余的0
    idx += 1
    for i in cell:
        if i[0][0] not in routes and i[0][1] not in routes and routes[
            -1] == 0:  # 当某条路径的两个端点不包含在route变量中，且为最每条子路径最初之二点时，才会继续往下考虑
            demand.extend(
                [
                    z[i[0][0] - 1], z[i[0][1] - 1]
                ]
            )
            routes.extend(i[0])

        elif i[0][0] == routes[1 + additional - 1] and i[0][
            1] not in routes:  # 如待检测路径的左端点与routes的左端点相同，比如，6-8和0-6-3-4-0
            demand.extend(
                [
                    z[i[0][1] - 1]
                ]
            )
            routes.insert(1, i[0][1])  # 那么把待检测路径的右端点插到routes的左端点位置，即0-8-6-3-4-0

        elif i[0][1] == routes[1 + additional - 1] and i[0][0] not in routes:  # 如待检测路径的右端点与routes的左端点相同
            demand.extend(
                [
                    z[i[0][0] - 1]
                ]
            )
            routes.insert(1, i[0][0])

        elif i[0][0] == routes[-1] and i[0][1] not in routes:  # 如待检测路径的左端点与routes的右端点相同
            demand.extend(
                [
                    z[i[0][1] - 1]
                ]
            )
            routes.append(i[0][1])

        elif i[0][1] == routes[-1] and i[0][0] not in routes:  # 如待检测路径的右端点与routes的右端点相同
            demand.extend(
                [
                    z[i[0][0] - 1]
                ]
            )
            routes.append(i[0][0])

        if sum([int(x) for x in demand]) > 5:
            # 这个5是车辆的容量。当某条路径当前的总需求量大于车辆容量时，之前的5条判断作废，删除demand列表和routes列表中新增加的元素
            # if i[0][0] not in routes and i[0][1] not in routes and routes[-1] == 0:  # 如果是在子路径的首端添加了两个元素
            if set([0, i[0][0], i[0][1]]) == set(routes[-3:]):
                demand = []
            else:
                del demand[-1]  # 超出车辆容量，删掉刚刚在demand里写入的那个节点的需求量

            # if i[0][0] not in routes and i[0][1] not in routes and routes[-1]==0: # 如果是在子路径的首端添加了两个元素
            if set([0, i[0][0], i[0][1]]) == set(routes[-3:]):
                del routes[-2:]
            # elif set(i[0])==set(routes[1+additional-1:3+additional-1]):
            elif set(i[0]) == set(routes[(1 + additional):(3 + additional)]):
                del routes[1 + additional]
            elif set(i[0]) == set(routes[-2:]):
                del routes[-1]

        if i == cell[-1]:  # 最后检测是否已循环到节约值列表的最后一行，如是，则结束本次循环对应的那条路径，在其后补0，清空demand列表
            additional = len(routes)
            routes.append(0)
            demand = []
        else:
            pass

# 记住！在这下面写个循环，删除多余的0！要使用反向遍历！思路就是，反向遍历时，记住最后一个0出现的位置index！
global num
num = 0
for i in range(len(routes) - 1, -1, -1):
    if routes[i] == 0:
        pass
    else:
        num = i + 2  # num表示倒数第二个0出现的位置，之所以不是倒数第一个，是因为routes右端点需要保留一个0，表示车辆最后回到车库
        break
del routes[num:]

print("This is the final_routes:", "\n", routes)
