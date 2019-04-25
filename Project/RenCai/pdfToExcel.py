#-*- conding: utf-8 -*-

import tabula

df = tabula.read_pdf("/Users/sunlu/Documents/创新研究院/工单/人才事业部/20190314/2018年泰山学者特聘专家计划申报书-徐东升330cfabc-a1d8-4d26-a569-209c22ec441b.pdf", encoding='gbk', pages='all')
print(df)
# for indexs in df.index:
#     #遍历打印企业名称
    # print(df.loc[indexs].values[1].strip())