import json
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.pyplot import MultipleLocator
from scipy.stats import normaltest
from scipy.stats import kstest
from scipy.stats import shapiro
import math


def remove_outliers_percentage():
    number = round(len(likes) * 0.025)

    for x in range(number):
        x = likes.index(max(likes))
        del centroids[x], tempos[x], roll_off[x], zero_crossings[x]
        likes.remove(max(likes))

        x = likes.index(min(likes))
        del centroids[x], tempos[x], roll_off[x], zero_crossings[x]
        likes.remove(min(likes))


def remove_outliers_3std():
    std = np.std(likes)
    avg = np.mean(likes)
    length = 0
    while length < len(likes):
        if likes[length] > avg + 3 * std:
            del centroids[length], tempos[length], roll_off[length], zero_crossings[length], likes[length]
        else:
            length += 1


def remove_outliers_mad():
    median = np.median(likes)
    # print(median)
    # print(np.abs(likes - median))
    mad = np.median(np.abs(likes - median))
    # print(median - 20 * mad)


def normalization(data):
    _range = np.max(data) - np.min(data)
    return (data - np.min(data)) / _range


def set_some_param(b_list, b_name):
    plt.figure(figsize=(figsize, figsize))
    plt.scatter(normalize_likes, b_list, s=1)
    # plt.xlabel('likes')
    # plt.ylabel('centroid')

    plt.xlabel("likes", size=size)
    plt.ylabel(b_name, size=size)
    plt.tick_params(labelsize=size)

    x_major_locator = MultipleLocator(0.1)
    # 把x轴的刻度间隔设置为0.1
    ax = plt.gca()
    # ax为两条坐标轴的实例
    ax.xaxis.set_major_locator(x_major_locator)
    # x轴的主刻度
    plt.xlim(0, 1)
    # x轴的刻度范围


def draw_centroid():
    # 画centroid-likes散点图
    set_some_param(centroids, 'centroids')
    y_major_locator = MultipleLocator(500)
    ax = plt.gca()
    ax.yaxis.set_major_locator(y_major_locator)
    plt.ylim(min(centroids), max(centroids))
    plt.show()


def draw_tempos():
    # 画tempo-likes散点图
    set_some_param(tempos, 'tempo')
    y_major_locator = MultipleLocator(5)
    ax = plt.gca()
    ax.yaxis.set_major_locator(y_major_locator)
    plt.ylim(min(tempos), max(tempos))

def draw_roll_off():
    # 画roll_off-likes散点图
    set_some_param(roll_off, 'roll_off')
    y_major_locator = MultipleLocator(500)
    ax = plt.gca()
    ax.yaxis.set_major_locator(y_major_locator)
    plt.ylim(min(roll_off), max(roll_off))



def draw_zero_crossings():
    # 画 zero_crossings-likes散点图
    set_some_param(zero_crossings, 'zero_crossings')
    y_major_locator = MultipleLocator(0.005)
    ax = plt.gca()
    ax.yaxis.set_major_locator(y_major_locator)
    plt.ylim(min(zero_crossings), max(zero_crossings))






def drawhist():
    # 画直方图
    plt.figure(figsize=(20, 8))
    n, bins, patches = plt.hist(x=centroids, bins='auto', color='#0504aa',alpha=0.7, rwidth=0.85)
    plt.grid(axis='y', alpha=0.75)
    plt.xlabel('centroid')
    plt.ylabel('Frequency')
    maxfreq = n.max()
    plt.ylim(plt.ylim(ymax=np.ceil(maxfreq / 10) * 15 if maxfreq % 10 else maxfreq + 10))
    for x, y in zip(bins[:-1], n):
        plt.text(x+52, y, '%d'%y, ha='center', va='bottom', fontsize=15, color='grey')
    plt.show()


def normal_distribution_test():

    centroid=0
    tempo=0
    roll_off=0
    zero_crossings=0

    # 对数据随机分组后进行正态性检验
    print("centroidTest:")
    for i in range(0,10):
        result=shapiro(c[i][1])
        p=result[1]
        if p>=0.05:
            centroid+=1
        print("group"+str(i)+"test:"+str(result))
    print("centroidTestSuccess:" + str(centroid) + " times")
    print()
    print("tempoTest:")
    for i in range(0,10):
        result = shapiro(c[i][2])
        p = result[1]
        if p>=0.05:
            tempo+=1
        print("group"+str(i)+"test:"+str(result))
    print("tempoTestSuccess:" + str(tempo) + " times")
    print()
    print("roll_offTest:")
    for i in range(0,10):
        result = shapiro(c[i][3])
        p = result[1]
        if p>=0.05:
            roll_off+=1
        print("group"+str(i)+"test:"+str(result))
    print("roll_offTestSuccess:" + str(roll_off) + " times")
    print()
    print("zero_crossingsTest:")
    for i in range(0,10):
        result = shapiro(c[i][4])
        p = result[1]
        if p>=0.05:
            zero_crossings+=1
        print("group"+str(i)+"test:"+str(result))
    print("zero_crossingsTestSuccess:" + str(zero_crossings) + " times")

    # 对整个样本进行正态性检验
    # print(shapiro(roll_off))
    # print(kstest(rvs=np.array(zero_crossings), cdf='norm', alternative='two_sided'))
    # print(normaltest(roll_off, axis=None))
if __name__ == '__main__':
    file = "./statistics.json"
    likes = []
    centroids = []
    tempos = []
    roll_off = []
    zero_crossings = []
    b = np.random.choice(range(0,4400),(10, 440),replace=False)
    source_file = open(file, encoding='utf-8')
    json_str = source_file.read()
    json_list = json.loads(json_str)
    c = np.ones(shape=(10, 5, 440), dtype=np.float64)
    for i in range(0,10):
        k=0
        for j in b[i]:
            c[i][0][k]=json_list[j]['digg_count']
            c[i][1][k]=json_list[j]['centroid']
            c[i][2][k]=json_list[j]['tempo']
            c[i][3][k]=json_list[j]['roll_off']
            c[i][4][k]=json_list[j]['zero_crossings']
            k+=1
    # del likes[0]
    # del centroids[0]
    # print(np.corrcoef(likes, zero_crossings))   # 相关性计算
    size = 16
    figsize = 10
    cnt = 0
    # for i in likes:
    #     if i < 10000:
    #         cnt += 1
    # print(len(likes) - cnt)

    normal_distribution_test() #正态分布检验

    normalize_likes = normalization(likes) #对点赞数据归一化

    # draw_centroid()
    # draw_tempos()
    # draw_roll_off()
    # draw_zero_crossings()
    # plt.show()
    # drawhist()#画直方图
    
