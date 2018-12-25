# coding=utf8
# Usage:
# Training: NB.py 1 TrainingDataFile ModelFile
# Testing: NB.py 0 TestDataFile ModelFile OutFile

import sys
import os
import math

DefaultFreq = 0.1
TrainingDataFile = "nb_data.train"
ModelFile = "nb_data.model"
TestDataFile = "nb_data.test"
TestOutFile = "nb_data.out"
ClassFeaDic = {}  # P(x=谷歌|y=军事)求最大似然,最大似然就是存统计计数
ClassFreq = {}  # 记录文章的种类
WordDic = {}
ClassFeaProb = {}  # 记录每个token 在各自类中的概率,记录概率值的
ClassDefaultProb = {}
ClassProb = {}


def Dedup(items):
    tempDic = {}
    for item in items:
        if item not in tempDic:
            tempDic[item] = True
    return tempDic.keys()


def LoadData():
    """
    加载数据
    :return:每一个类别对应的词
     ClassFeaDic = {1: {1: 101, 2: 4259, 3: 1613, 4: 523, 5: 174, 6: 213, },
                    2: {2: 6969, 3: 32, 4: 681, 5: 32, 6: 20,},
                    3: {34916: 1, 2: 2899, 3: 23, 4: 116, 5: 8, 6: 9, }}
     ClassFeaDic ={运动:{跑步:101}}
     WordDic ={1: 1, 2: 1, 3: 1, 4: 1, 5: 1, 6: 1, 7: 1, 8: 1, 9: 1, 10: 1, 11: 1, 12: 1, 13: 1, 14: 1, 15: 1, 16: 1,}
     WordDic = {航空:1,航天:1}

     ClassFreq = {1: 812, 2: 832, 3: 809} 记录每个类别对应的文章数
    """
    # 统计一共读了多少篇文章
    i = 0
    infile = file(TrainingDataFile, 'r')
    sline = infile.readline().strip()
    while len(sline) > 0:
        pos = sline.find("#")  # 返回的是取到该值的索引
        if pos > 0:
            sline = sline[:pos].strip()
        words = sline.split(' ')
        if len(words) < 1:
            print "Format error!"
            break
        # 类别号，分类标签:每条样本的第一列,就财经1,汽车2,体育3复制给classid
        classid = int(words[0])
        if classid not in ClassFeaDic:  # 判断这类型文章在不在文章字典里面,不在进入if,在的话频次+1,为了求先验概率p(yi)：先验概率：每个类的文章个数/总文章数
            # 记录每个类中的每个token的计数(item理解为语句,token理解为每个词)
            ClassFeaDic[classid] = {}  # 创建一个空集合必须用 set() 而不是 { }，因为 { } 是用来创建一个空字典。
            # 记录每个token(词语)在各自类中的概率
            ClassFeaProb[classid] = {}
            # 记录每个类的文章个数
            ClassFreq[classid] = 0
        ClassFreq[classid] += 1  # ClassFreq[classid] 是每个类文章个数
        # 记录每篇文章的正文文本特征# 取第二个到最后一个,因为第一个是类别号
        words = words[1:]
        # remove duplicate words, binary distribution
        # words = Dedup(words)
        for word in words:
            if len(word) < 1:
                continue
            wid = int(word)
            # 判断词在不在我们的词语字典里,不在初始化为1,在的话就不管了
            if wid not in WordDic:
                WordDic[wid] = 1
            # 判断当前词在不在当前classid文章的字典里.不在初始化为1,在的话记录频次
            if wid not in ClassFeaDic[classid]:
                ClassFeaDic[classid][wid] = 1
            else:
                ClassFeaDic[classid][wid] += 1
        i += 1
        # 然后再读取一行继续
        sline = infile.readline().strip()
    infile.close()
    # print i, "instances loaded!"
    # print len(ClassFreq), "classes!", len(WordDic), "words!"
    # print(ClassFreq)
    # print ClassFeaDic
    # print WordDic


# 计算模型
def ComputeModel():
    sum = 0.0
    # 循环遍历不同类文章记录的字典value值,key是classid value 是该类对应的频次
    for freq in ClassFreq.values():
        # 获取三类文章总数
        sum += freq
    # 循环遍历不同类文章记录的字典的key值,key是classid value是该类对应的频次
    for classid in ClassFreq.keys():
        # p(yi)：先验概率：每个类的文章个数/总文章数
        ClassProb[classid] = (float)(ClassFreq[classid]) / (float)(sum)
        # print(ClassProb)  # 对应每个类文章的先验概率 {1: 0.33102323685283325, 2: 0.33917651854871583, 3: 0.32980024459845086}
    # p(xj|yi)
    # 遍历每个类，针对每一个类，重构ClassFeaProb为概率值
    # 循环遍历没类文章每个词频的字典中的key,key是classid,value是字典{词:词频}
    for classid in ClassFeaDic.keys():
        sum = 0.0
        # 循环遍历当前classid对应的value字典{词典,词频}
        for wid in ClassFeaDic[classid].keys():
            # 统计当前类的文章的词频次数
            sum += ClassFeaDic[classid][wid]
            # print sum
        # print ClassFeaDic  # {1: {1: 93, 2: 2817, 3: 1525}，}
        # 为了使程序健壮，防止向下溢出，这里可以把sum+1,防止分母为零
        newsum = (float)(sum + 1)  # float() 函数用于将整数和字符串转换成浮点数。
        print newsum
        # 循环遍历当前类文章的key
        for wid in ClassFeaDic[classid].keys():
            # 存入条件概率值,用体育文章举例子,体育文章中铅球的条件概率= 铅球在体育文章中的总数/体育文章的总词数
            ClassFeaProb[classid][wid] = (float)(ClassFeaDic[classid][wid] + DefaultFreq) / newsum
            print ClassFeaProb[classid][wid]
        # 每一类文章设置一个默认的条件概率,防止在测试集时候一个词在当前类文章没有,就用该值
        ClassDefaultProb[classid] = (float)(DefaultFreq) / newsum
    return


"""
训练模型数据输出格式:
共四行,第一行 classid 先验概率,默认概率
第二行 class_a tokenid 条件概率...
第三行 class_b tokenid 条件概率...
第四行 class_c tokenid 条件概率...
"""


def SaveModel():
    outfile = file(ModelFile, 'w')
    # 循环遍历类别频次字典,获取三大类类别的classid
    for classid in ClassFreq.keys():
        outfile.write(str(classid))
        outfile.write(' ')
        # 将先验概率写进去
        outfile.write(str(ClassProb[classid]))
        outfile.write(' ')
        # 默认条件概率写进去
        outfile.write(str(ClassDefaultProb[classid]))
        outfile.write(' ')
    # 第一行遍历3类文章对应不同的概率,然后换行
    outfile.write('\n')

    for classid in ClassFeaDic.keys():
        for wid in ClassFeaDic[classid].keys():
            # wordid + 对应的条件概率写入
            outfile.write(str(wid) + ' ' + str(ClassFeaProb[classid][wid]))
            outfile.write(' ')
            # 每一类文章为一行
        outfile.write('\n')
    outfile.close()


def LoadModel():
    global WordDic
    WordDic = {}
    global ClassFeaProb
    ClassFeaProb = {}
    global ClassDefaultProb
    ClassDefaultProb = {}
    global ClassProb
    ClassProb = {}
    # 读入模型
    infile = file(ModelFile, 'r')
    sline = infile.readline().strip()  # 第一行数是classid,先验概率,默认概率
    items = sline.split(' ')  # 根据空格分为三个类别的数据
    if len(items) < 6:
        print "Model format error!"
        return
    i = 0
    while i < len(items):
        classid = int(items[i])
        ClassFeaProb[classid] = {}
        i += 1
        if i >= len(items):
            print "Model format error!"
            return
        ClassProb[classid] = float(items[i])  # 每一个类别对应的先验概率
        i += 1
        if i >= len(items):
            print "Model format error!"
            return
        ClassDefaultProb[classid] = float(items[i])  # 每一个类别对应的默认概率
        i += 1
    for classid in ClassProb.keys():
        sline = infile.readline().strip()  # 读取后面三行数据,就是某一类文章的某个词的条件概率
        items = sline.split(' ')
        i = 0
        while i < len(items):
            wid = int(items[i])
            if wid not in WordDic:
                WordDic[wid] = 1
            i += 1
            if i >= len(items):
                print "Model format error!"
                return
            # 当前类文章的该词字典中加上条件概率
            ClassFeaProb[classid][wid] = float(items[i])
            i += 1
    infile.close()
    print len(ClassProb), "classes!", len(WordDic), "words!"


def Predict():
    global WordDic
    global ClassFeaProb
    global ClassDefaultProb
    global ClassProb

    TrueLabelList = []
    PredLabelList = []
    i = 0
    infile = file(TestDataFile, 'r')
    outfile = file(TestOutFile, 'w')
    sline = infile.readline().strip()  # 读取测试数据
    # 存储最后的结果：针对每一类的概率值
    # p(yi|X) = p(yj)p(X|yi)
    # p(X|yi) = p(x0|yi)*...*p(xn|yi)
    scoreDic = {}
    iline = 0
    while len(sline) > 0:
        iline += 1
        if iline % 10 == 0:
            print iline, " lines finished!\r",
        pos = sline.find("#")
        if pos > 0:
            sline = sline[:pos].strip()
        words = sline.split(' ')
        if len(words) < 1:
            print "Format error!"
            break
        classid = int(words[0])
        # 真实标签
        TrueLabelList.append(classid)  # 从测试数据把标签添加进来
        words = words[1:]
        # remove duplicate words, binary distribution
        # words = Dedup(words)
        for classid in ClassProb.keys():
            scoreDic[classid] = math.log(ClassProb[classid])
        for word in words:
            if len(word) < 1:
                continue
            wid = int(word)
            if wid not in WordDic:
                # print "OOV word:",wid
                continue
            for classid in ClassProb.keys():
                if wid not in ClassFeaProb[classid]:
                    scoreDic[classid] += math.log(ClassDefaultProb[classid])
                else:
                    scoreDic[classid] += math.log(ClassFeaProb[classid][wid])
        # binary distribution
        i += 1
        maxProb = max(scoreDic.values())  # 选取概率最大的
        for classid in scoreDic.keys():
            if scoreDic[classid] == maxProb:
                # 预测标签
                PredLabelList.append(classid)
        sline = infile.readline().strip()
    infile.close()
    outfile.close()
    print len(PredLabelList), len(TrueLabelList)
    return TrueLabelList, PredLabelList


def Evaluate(TrueList, PredList):
    accuracy = 0
    i = 0
    while i < len(TrueList):
        if TrueList[i] == PredList[i]:
            accuracy += 1
        i += 1
    # 准确率
    accuracy = (float)(accuracy) / (float)(len(TrueList))
    print "Accuracy:", accuracy


def CalPreRec(TrueList, PredList, classid):
    correctNum = 0
    allNum = 0
    predNum = 0
    i = 0
    while i < len(TrueList):
        if TrueList[i] == classid:
            allNum += 1
            if PredList[i] == TrueList[i]:
                correctNum += 1
        if PredList[i] == classid:
            predNum += 1
        i += 1
    return (float)(correctNum) / (float)(predNum), (float)(correctNum) / (float)(allNum)


if __name__ == '__main__':

    LoadData()
    ComputeModel()
    SaveModel()
    print "start testing:"
    # 加载模型
    LoadModel()
    # 预测结果,返回的是真实标签和预测标签
    TList, PList = Predict()
    i = 0
    outfile = file(TestOutFile, 'w')
    while i < len(TList):
        outfile.write(str(TList[i]))
        outfile.write(' ')
        outfile.write(str(PList[i]))
        outfile.write('\n')
        i += 1
    outfile.close()
    Evaluate(TList, PList)  # 计算概率值
    for classid in ClassProb.keys():
        pre, rec = CalPreRec(TList, PList, classid)
        print "Precision and recall for Class", classid, ":", pre, rec
else:
    print "Usage incorrect!"
