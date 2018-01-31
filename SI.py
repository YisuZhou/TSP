import random
import numpy as np
import math


location=np.loadtxt('city_location.txt')
num_ant=200 #蚂蚁个数
num_city=30 #城市个数
alpha=1 #信息素影响因子
beta=1  #期望影响因子
info=0.1 #信息素的挥发率
Q=1 #常数

count_iter = 0
iter_max = 500
#dis_new=1000
#==========================================
#对称矩阵，两个城市之间的距离
def distance_p2p_mat():
    dis_mat=[]
    for i in range(num_city):
        dis_mat_each=[]
        for j in range(num_city):
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
        dis=dis_mat[each[num_city-1]][each[0]]+dis#回家
        dis_list.append(dis)
    return dis_list

#==========================================
#点对点距离矩阵
dis_list=distance_p2p_mat()
dis_mat=np.array(dis_list)#转为矩阵
#期望矩阵
e_mat_init=1.0/(dis_mat+np.diag([10000]*num_city))#加对角阵是因为除数不能是0
diag=np.diag([1.0/10000]*num_city)
e_mat=e_mat_init-diag#还是把对角元素变成0
#初始化每条边的信息素浓度，全1矩阵
pheromone_mat=np.ones((num_city,num_city))
#初始化每只蚂蚁路径，都从0城市出发
path_mat=np.zeros((num_ant,num_city)).astype(int)


#while dis_new>400:
while count_iter < iter_max:
    for ant in range(num_ant):
        visit=0#都从0城市出发
        unvisit_list=list(range(1,30))#未访问的城市
        for j in range(1,num_city):
            #轮盘法选择下一个城市
            trans_list=[]
            tran_sum=0
            trans=0
            for k in range(len(unvisit_list)):
                trans +=np.power(pheromone_mat[visit][unvisit_list[k]],alpha)*np.power(e_mat[visit][unvisit_list[k]],beta)
                trans_list.append(trans)
                tran_sum =trans
            
            rand=random.uniform(0,tran_sum)#产生随机数

            for t in range(len(trans_list)):
                if(rand <= trans_list[t]):
                    visit_next=unvisit_list[t]


                    break
                else:
                    continue
            path_mat[ant,j]=visit_next#填路径矩阵

            unvisit_list.remove(visit_next)#更新
            visit=visit_next#更新

    #所有蚂蚁的路径表填满之后，算每只蚂蚁的总距离
    dis_allant_list=cal_newpath(dis_mat,path_mat)

    #每次迭代更新最短距离和最短路径        
    if count_iter == 0:
        dis_new=min(dis_allant_list)
        path_new=path_mat[dis_allant_list.index(dis_new)].copy()      
    else:
        if min(dis_allant_list) < dis_new:
            dis_new=min(dis_allant_list)
            path_new=path_mat[dis_allant_list.index(dis_new)].copy() 

    # 更新信息素矩阵
    pheromone_change=np.zeros((num_city,num_city))
    for i in range(num_ant):
        for j in range(num_city-1):
            pheromone_change[path_mat[i,j]][path_mat[i,j+1]] += Q/dis_mat[path_mat[i,j]][path_mat[i,j+1]]
        pheromone_change[path_mat[i,num_city-1]][path_mat[i,0]] += Q/dis_mat[path_mat[i,num_city-1]][path_mat[i,0]]
    pheromone_mat=(1-info)*pheromone_mat+pheromone_change
    count_iter += 1 #迭代计数+1，进入下一次


        
print('最短距离：',dis_new)
print('最短路径：',path_new)





