import nltk
import xlrd
import jieba
import nltk.classify.util
import matplotlib.pyplot as plt
import mplcyberpunk

# 该方法用来将评论拆分为词语，通过jieba分词
def partComm(sheet):
    rowNum = sheet.nrows
    comList = []
    for i in range(1, rowNum):
        # 前三条数据不要
        cnt = 0
        for tem in sheet.row_values(i):
            if cnt < 3:
                cnt = cnt + 1
                continue
            cut = jieba.cut(str(tem), cut_all=True)
            comList += ((','.join(cut).split(',')))
    return comList


# 该方法通过值找到字典的键
def get_key1(dct, value):
    return [k for (k, v) in dct.items() if value in v]


def draw_graphs(emotion_percentage,emotion_cnt):
    # 数据可视化
    plt.rcParams['font.sans-serif'] = ['SimHei']  # 显示中文标签
    plt.rcParams['axes.unicode_minus'] = False  # 这两行需要手动设置
    labels = [i for i in emotion_percentage[0].keys()]
    all_data = [[i for i in a.values()] for a in emotion_cnt]
    colors = ['red', 'yellow', 'orange', 'darkred', 'grey', 'blue', 'lightskyblue', 'purple']
    for i in range(len(all_data)):
        plt.figure(figsize=(12, 12))
        plt.title("各个阶段各情绪的占比：phase" + str(i + 1), fontdict={'weight': 'normal', 'size': 50})
        patches, text1, text2 = plt.pie(all_data[i],
                                        explode=(0, 0, 0, 0.1, 0.1, 0.1, 0.1, 0.1),
                                        labels=labels,
                                        colors=colors,
                                        autopct='%3.2f%%',  # 数值保留固定小数位
                                        shadow=False,  # 无阴影设置
                                        startangle=90,  # 逆时针起始角度设置
                                        pctdistance=0.6,  # 数值距圆心半径倍数距离
                                        textprops={'fontsize': 20, 'color': 'black'})
        plt.savefig(r'.\pic\piechart' + str(i + 1))
        plt.show()

    # 绘制情绪占比随着时间的变化
    #plt.style.use("cyberpunk")
    plt.figure(figsize=(12, 12))
    x = ["phase"+str(i+1) for i in range(len(emotion_cnt))]
    y = [[list(d.values())[i] for d in emotion_percentage] for i in range(8)]
    plt.xlabel("时间")
    plt.ylabel("百分比")
    plt.title("情绪占比随着时间的变化")
    for k in range(len(y)):
        plt.plot(x, y[k], marker='.', ms=10, label=list(emotion_percentage[0].keys())[k])
    plt.legend(loc="upper right")
    for curY in y:
        for x1, yy in zip(x, curY):
            plt.text(x1, yy + 1, str(yy)[0:4] + "%", ha='center', va='bottom', fontsize=15, rotation=15)
    mplcyberpunk.add_glow_effects()
    plt.savefig(r'.\pic\linechart')
    plt.show()
    # 画一个局部细节图
    plt.figure(figsize=(12, 12))
    x = ["phase" + str(i+1) for i in range(len(emotion_cnt))]
    y = [[list(d.values())[i] for d in emotion_percentage] for i in range(3,8)]
    plt.xlabel("时间")
    plt.ylabel("百分比")
    plt.title("情绪占比随着时间的变化")
    for k in range(len(y)):
        plt.plot(x, y[k], marker='.', ms=10, label=list(emotion_percentage[0].keys())[k+3])
    plt.legend(loc="upper right")
    for curY in y:
        for x1, yy in zip(x, curY):
            plt.text(x1, yy, str(yy)[0:4] + "%", ha='center', va='bottom', fontsize=15, rotation=15)
    mplcyberpunk.add_glow_effects()
    plt.savefig(r'.\pic\local_linechart')
    plt.show()



# 如果filePath为空就默认分析前四阶段
# 如果不为空就分析输入的文件
def analysis(filePath):
    # 停用词，用来减少一些常见词汇的干扰
    stop_word = ['，', '', '的', ' ', '。', ':', '了', '@', '#', '回复', '日', '月', '病毒', '是', '1', '我', '例', '、', '在', '？',
                 '！',
                 '都', '确诊', '医院', '你', '有', '人', '.', '也', '发热',
                 '01', '隔离', '病毒感染', '和', '就', '22', '口罩', '说', '21', '国家', '啊', '来自', '微', '不', '】', '博', '疫情', '还',
                 r'\\xa0', '委', '治疗', '现在', '吗', ':【', '传染', '：', '新闻', '为', '北京', '2', '目前', '河北', '我们', '医疗', '没有',
                 '岁', '人员', '这', '去', '什么', '诊病', '平安', '自己', '大家', '吧', '首例', '等', '症状', '确认', '卫', '23', '就诊', '不是',
                 '健', '要', '到', '原因', '名', '定点', '不明', '能', '专家', '机构', '病情', '人民', '武汉市', '接触', '今天', '卫生', '医疗机构',
                 '18', '中国', '工作', '一个', '真的', '染病', '5', '对', '情况', '检测', '别', '某', '已', '定点医院', 'weibo', 'com', '就是',
                 '出现', '-', '没', '已经', '19', '）', '者', '从', '被', '戴', '【']
    # 心态词典：先找一些寻常的情绪词，再在评论经过停用词筛选后，在前100频率的词汇中选出频数较高的情绪词
    emotion_dict = {
        '喜': ['高兴', '好受', '开心', '快活', '快乐', '庆幸', '舒畅', '舒服', '爽快', '甜美', '甜蜜', '痛快', '喜出望喜悦', '喜滋滋', '心花怒放',
              '心旷神怡', '愉快', '好耶', '棒', '不错', '真好', '好起来了', '太好了', '很棒', '很好', '哈哈','真好','给力'],
        '赞美': ['英雄', '感谢', '佩服', '厉害', '辛苦', '致敬', '谢谢', '致敬','天使','最美'],
        '祝福': ['加油', '希望', '平安', '愿', '康复', '挺住','恭喜'],
        '怒': ['愤慨', '愤怒', '恼火', '气愤', '不要脸', 'tm', '害人', '该骂', '滚', '呸', '可怕', '垃圾' ,'不要脸','无耻','畜生','骂','尼玛','脑残','活该'],
        '哀': ['悲伤', '悲痛', '凄惨', '伤神', '伤心', '酸楚', '气馁', '丧气', '扫兴', '哀怨', '悲愤', '悲痛', '悲酸', '哀伤', '哀戚', '哀痛', '难过',
              '怜悯', '悲哀', '沉痛', '伤感', '痛苦', '痛心', '难过', '凄凉郁闷', '不幸', '可怜', '倒霉', '难接受', '心痛'],
        '惧': ['危惧', '畏忌', '紧张', '心惧', '胆怯', '胆小', '畏缩', '发慌', '胆怯', '畏缩', '害怕', '不安', '发慌', '惊吓', '焦急', '恐怖', '恐惧',
              '急噪', '急切', '迫切', '着急', '焦虑', '心急', '迷离恍惚', '心慌', '发慌', '恐慌', '心慌意乱', '坐立不安', '局促不安', '忐忑不安',
              '方寸大乱', '心烦意乱', '六神无主', '七上八下', '神魂颠倒', '心神不定', '心乱如麻', '若有所失', '惘然若失', '长吁短叹', '心惊肉跳',
              '惶恐不安', '心惊胆颤', '不知所措', '局促不安', '心急火燎', '心急如焚', '惴惴不安', '可怕', '吓人', '骇人', '不敢', '瑟瑟发抖','紧张'],
        '烦恼、无奈': ['无语', '真的是', '服了', '哎', '唉', '烦', '求求','心累','好笑'],
        '质疑': ['怎么可能', '假新闻', '虚伪', '带节奏', '杠', '有问题', '造谣', '假的', '假消息','骗子','骗人']
    }
    comment_1 = xlrd.open_workbook(r".\doc\comments\phase1.xls").sheet_by_index(0)
    comment_2 = xlrd.open_workbook(r".\doc\comments\phase2.xls").sheet_by_index(0)
    comment_3 = xlrd.open_workbook(r".\doc\comments\phase3.xls").sheet_by_index(0)
    comment_4 = xlrd.open_workbook(r".\doc\comments\phase4.xls").sheet_by_index(0)
    comment = [comment_1, comment_2, comment_3, comment_4]
    s = "123"
    if filePath!="":
        filePaths = filePath.split(';')
        for path in filePaths:
            comment = comment+[xlrd.open_workbook(path).sheet_by_index(0)]
    # 2. 开一个情绪频率计数器
    emotion_cnt = [
        {
            '喜': 0,
            '赞美': 0,
            '祝福': 0,
            '怒': 0,
            '哀': 0,
            '惧': 0,
            '烦恼、无奈': 0,
            '质疑': 0
        } for i in range(len(comment))
    ]
    rawComment = [partComm(c) for c in comment]
    # 3. 筛选评论词
    filtered_comment = [[w for w in raw if not w in stop_word] for raw in rawComment]
    # 4. 计算所有单词的频率
    freq = [nltk.FreqDist(f) for f in filtered_comment]
    # 5. 通过字典映射，算出心态词的频率
    for cnt in emotion_cnt:
        f = freq[emotion_cnt.index(cnt)]
        for word in f:
            key = get_key1(emotion_dict, word)
            if len(key) != 0:
                for k in key:
                    cnt[k] += f.freq(word)
        print('phase' + str(emotion_cnt.index(cnt)) + str(cnt))
    # 6. 算出每个阶段 每个心态词的占比
    total_freq_singlePhase = [sum(f.values()) for f in emotion_cnt]
    emotion_percentage = emotion_cnt
    for i in range(len(emotion_percentage)):
        for d in emotion_cnt[i]:
            emotion_percentage[i][d] = round(emotion_cnt[i][d]/total_freq_singlePhase[i],4)*100
    print(emotion_percentage)
    # 数据可视化
    draw_graphs(emotion_percentage,emotion_cnt)