# encoding=utf-8
import sys

sys.path.append("../")
import jieba
import jieba.posseg
import jieba.analyse

seg_list = jieba.cut("我来到北京清华大学", cut_all=False)
print("default Mode:" + "/".join(seg_list))  # 默认模式
