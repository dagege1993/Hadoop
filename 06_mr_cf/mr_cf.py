# encoding=utf8
import math
import sys

with open('part-00151', 'r') as f:
    data = f.readlines()

cur_item = None
user_score_list = []

for line in data:
    ss = line.strip().split(',')
    if len(ss) != 3:
        continue
    u, i, s = ss
    # print(ss)
    # print("%s\t%s\t%s") % (i, u, s)  # 这样输出结果完成了转置
    # 2reduce
    # item, user, score = line.strip().split('\t')
    user, item, score = ss
    if not cur_item:  # 最开始 if not None,啥意思
        cur_item = item
    if item != cur_item:  # 如果两个Item不相等,如果相等,直接就添加进列表
        sum = 0.0
        for tuple in user_score_list:
            (u, s) = tuple
            sum += pow(s, 2)  # pow() 方法返回 xy（x的y次方） 的值。
        sum = math.sqrt(sum)
        for tuple in user_score_list:
            (u, s) = tuple
            print("%s\t%s\t%s") % (u, cur_item, float(s / sum))  # 进来是Iu,出去编程ui矩阵
        user_score_list = []
        cur_item = item
    user_score_list.append((user, float(score)))
print(user_score_list)
# 完成了归一化
# sum = 0.0
# for tuple in user_score_list:
#     (u, s) = tuple
#     sum += pow(s, 2)
# sum = math.sqrt(sum)
