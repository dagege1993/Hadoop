# encoding=utf8
import os
import sys

os.system('tar xvzf jieba.tgz > /dev/null')  # 会执行括号中的命令，如果命令成功执行，这条语句返回0，否则返回1,/dev/null不产生日志
reload(sys)  # Python2.5 初始化后删除了 sys.setdefaultencoding 方法，我们需要重新载入
sys.setdefaultencoding('utf-8')

sys.path.append('./')
import jieba
import jieba.posseg
import jieba.analyse

# with open(r'C:\Users\hlz\Desktop\Hadoop\04_mr_fenci\test', 'r', encoding='utf-8') as f:
# f = open(r'C:\Users\hlz\Desktop\Hadoop\04_mr_fenci\test', 'r', encoding='utf-8')
# lines = f.readlines()

for line in sys.stdin:
    # for line in lines:
    ss = line.strip().split()
    if len(ss) != 2:
        continue
    music_id = ss[0].strip()
    music_name = ss[1].strip()
    result_list = []
    for x, w in jieba.analyse.extract_tags(music_name, withWeight=True):  # withWeight 为是否一并返回关键词权重值，默认值为 False
        result_list.append(':'.join([x, str(round(w, 3))]))  # round() 方法返回浮点数x的四舍五入值。
    print music_name + "==>" + ' '.join(result_list)
