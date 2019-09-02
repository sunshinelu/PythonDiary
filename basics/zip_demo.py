# -*- coding: utf-8 -*-

"""
 @Author  : sunlu 
 @Date    : 19/8/29 下午9:01 
 @File    : zip_demo.py
 @Note    : 
 
 """
import numpy as np

list1 = [10, 56, 83, 32, 78, 106, 94, 178, 173, 15]
list2 = [0.051022112232299445, 0.027634261858268252, 0.02677423296680635, 0.024720285856013838, 0.0235918656211924, 0.017828227101178002, 0.015427769078100437, 0.0143188299334326, 0.014318110758298412, 0.012701194944699252]

list3 = list(zip(list1,list2))
print(type(list3))
for i in list3:
    print(i)

arr1 = np.array(list3)
print(arr1)

print("-------------------------------")
vocabArray = ['中国', '我们', '一个', '自己', '可以', '没有', '美国', '市场', '企业', '问题', '汽车', '学生', '进行', '可能', '产品', '已经', '认为', '如果', '一些', '发展', '专业', '就是', '他们', '记者', '日本', '工作', '情况', '目前', '国家', '考生', '这种', '这样', '车型', '这个', '方面', '表示', '开始', '今年', '俄罗斯', '公司', '因为', '系统', '主要', '价格', '学校', '要求', '需要', '北京', '招生', '通过', '10', '现在', '同时', '这些', '成为', '社会', '轿车', '能力', '时间', '考试', '影响', '不是', '销售', '重要', '由于', '一定', '不能', '志愿', '出现', '技术', '计划', '还是', '活动', '使用', '自主', '发现', '不会', '虽然', '发动机', '男人', '其中', '能够', '对于', 'civic', '作战', '比较', '国内', '什么', '学习', '世界', '作为', '上市', '以及', '增加', '品牌', '进入', '甚至', '女人', '30', '经济', '提高', '应该', '全国', '但是', '教育', '2006', '奇瑞', '患者', '标准', '研发', '手术', '孩子', '那么', '治疗', '生产', '达到', '很多', '所以', '成功', '直接', '不同', '非常', '录取', '海军', '报道', '比如', '攻击', '设计', '根据', '未来', '了解', '军事', '消费者', '受到', '组织', '万元', '方式', '大学', '提供', '车辆', '资料', '时候', '一种', '选择', '21', '明显', '其他', '20', '包括', '专家', '装备', '环境', '12', '增长', '还有', '美军', '费用', '而且', '之后', '超过', '广州', '希望', '分钟', '参加', '这是', '不要', '结果', '军队', '另外', '研究', '之子', '11', '任何', '万辆', '结尾', '战略', '文章', '目标', '丰田', '以上', '发生', '有关', '具有', '比赛', '基础', '医生', '感觉', '保持', '推出', '必须', '拥有', '公布', '这次', '军事演习', '保护', '女性', '越来越', '完成', '填报', '部分', '不少', '车主', '成本', '一直', '实施', '当时', '战争', '只有', '一次', '许多', '航母', '最终', '左右', '凯美瑞', '因此', '大国', '最后', '国际', '带来', '新车', '正在', '得到', '看到', '政策', '觉得', '政府', '优势', '方法', 'gt', '此次', '知识', '联合', '重点', '告诉', '为了', '研究生', '特别', '导致', '规定', '建设', '战斗机', '实力', '来自', '十分', '其实', '强大', '过程', '相关', '作用', '比分', '或者', '产生', '竞争', '安全', '内容', '期间', '整个', '经过', '知道', '信息', '肿瘤', '阅读', '去年', '全球', '不过', '开发', '以往', '领先', '造成', '以来', '相当', '现代', '表现', '生活', '完全', '决定', '中心', '武器', '五一', '比例', '裁判', '才能', '报名', '随着', '存在', '变化', '消息', '利用', '需求', '基本', '两个', '来源', '重新', '朋友', '调查', '形成', '分析', '导弹', '一位', '对手']
list4 = []
for i in list1:
    # print(i)
    # print(type(i))
    # print(vocabArray[i])
    list4.append(vocabArray[i])

print(list4)
for i in list4:
    print(i)
print("-------------------------------")


# list4 = list(zip(list1,list2)).map(lambda a,b: (a,vocabArray(int(a)),b))
#
# map(lambda x, y: x + y, [1, 3, 5, 7, 9], [2, 4, 6, 8, 10])
# print(list4)
# for i in list4:
#     print(i)