# -*- coding: utf-8 -*-

"""
使用jaccard计算文本相似性


"""
def jaccard_similarity(target, source):
    """获取两个字段的相似度，数值为1表示完全相似"""
    target = list(target)
    source = list(source)
    s1 = set(target)
    s2 = set(source)
    actual_jaccard = round(len(s1.intersection(s2)) / len(s1.union(s2)), 2)
    return actual_jaccard

print(str(jaccard_similarity('北京大学法学院', '北京大学法律学系')))

print(str(jaccard_similarity('北京大学法律学系', '北京大学法律学系')))