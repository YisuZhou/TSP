import random
import numpy as np
import math

num_city=30#城市总数
table_len=20#禁忌表长度
location=np.loadtxt('city_location.txt')
taboo_table=[]


#==========================================
#对称矩阵，两个城市之间的距离
def distance_p2p_mat():
    dis_mat=[]
    for i in range(30):
        dis_mat_each=[]
        for j in range(30):
            dis=math.sqrt(pow(location[i][0]-location[j][0],2)+pow(location[i][1]-location[j][1],2))
            dis_mat_each.append(dis)
        dis_mat.append(dis_mat_each)
   # print(dis_mat)
    return dis_mat

#计算所有路径对应的距离
def cal_newpath(dis_mat,path_new):
    dis_list=[]
    for each in path_new:
        dis=0
        for j in range(num_city-1):
            dis=dis_mat[each[j]][each[j+1]]+dis
        dis=dis_mat[each[29]][each[0]]+dis#回家
        dis_list.append(dis)
    return dis_list

#寻找上一个最优路径对应的所有领域解
def find_newpath(path_best):
    path_new=[]
    for i in range(1,num_city-1):
        for j in range(i+1,num_city):
            path=path_best.copy()
            path[i],path[j]=path[j],path[i]
            path_new.append(path)
    return path_new


#==========================================
#点对点距离矩阵
dis_mat=distance_p2p_mat()

#设置初始解
path_initial=[]
initial=list(range(30))
path_initial.append(initial)
#print(path_initial)

#加入禁忌表
taboo_table.append(initial)

#求初始解的路径长度
dis_list=cal_newpath(dis_mat,path_initial)
dis_best=min(dis_list)#最短距离
path_best=path_initial[dis_list.index(dis_best)]#对应的最短路径方案
#print(path_best)

#初始期望
expect_dis=dis_best
expect_best=path_best
for iter in range(5000):#迭代
    #寻找全领域新解
    path_new=find_newpath(path_best)
    #print(path_new)

    #求出所有新解的路径长度
    dis_new=cal_newpath(dis_mat,path_new)
#    print(dis_new)

    #选择路径
    dis_best=min(dis_new)#最短距离
    path_best=path_new[dis_new.index(dis_best)]#对应的最短路径方案
    if dis_best < expect_dis:#最短的<期望
        expect_dis=dis_best
        expect_best=path_best#更新两个期望
        if path_best in taboo_table:
            taboo_table.remove(path_best)
            taboo_table.append(path_best)
        else:
            taboo_table.append(path_best)
    else:#最短的还是不能改善期望
        if path_best in taboo_table:#在禁忌表里
            dis_new.remove(dis_best)
            path_new.remove(path_best)
            dis_best=min(dis_new)#求不在禁忌表中的最短距离
            path_best=path_new[dis_new.index(dis_best)]#对应的最短路径方案
            taboo_table.append(path_best)
        else:#不在禁忌表
            taboo_table.append(path_best)
    if len(taboo_table)>=table_len:
        del taboo_table[0]
        
print('最短距离',expect_dis)
print('最短路径：',expect_best)






