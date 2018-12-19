# encoding=utf-8
import sys
import os
import random

WordList = []
WordIDDic = {}
TrainingPercent = 0.8

# inpath = sys.argv[1]
# OutFileName = sys.argv[2]
inpath = 'data'
OutFileName = 'nb_data'
trainOutFile = file(OutFileName + ".train", "w")
testOutFile = file(OutFileName + ".test", "w")


def ConvertData():
    i = 0
    tag = 0
    for filename in os.listdir(inpath):
        if filename.find("business") != -1:
            tag = 1
        elif filename.find("auto") != -1:
            tag = 2
        elif filename.find("sport") != -1:
            tag = 3
        i += 1
        rd = random.random()
        outfile = testOutFile
        if rd < TrainingPercent:
            outfile = trainOutFile

        if i % 100 == 0:  # 这个参数是干啥的
            print i, "files processed!\r",

        infile = file(inpath + '/' + filename, 'r')
        outfile.write(str(tag) + " ")
        content = infile.read().strip()
        content = content.decode("utf-8", 'ignore')
        words = content.replace('\n', ' ').split(' ')
        for word in words:
            if len(word.strip()) < 1:  # 把一些符号之类的过滤掉
                continue
            if word not in WordIDDic:  # 最开始这是一个空字典
                WordList.append(word)  # 开始是一个空列表
                WordIDDic[word] = len(WordList)
            outfile.write(str(WordIDDic[word]) + " ")
        outfile.write("#" + filename + "\n")
        infile.close()

    print i, "files loaded!"
    print len(WordList), "unique words found!"


ConvertData()
trainOutFile.close()
testOutFile.close()
