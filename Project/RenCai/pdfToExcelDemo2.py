import camelot

file_path = "/Users/sunlu/Documents/创新研究院/工单/人才事业部/20190314/2018年泰山学者特聘专家计划申报书-徐东升330cfabc-a1d8-4d26-a569-209c22ec441b.pdf"
# 从PDF中提取表格
tables = camelot.read_pdf(file_path, pages='2', flavor='stream')


print(tables[0])
# 绘制PDF文档的坐标，定位表格所在的位置
# tables[0].plot('text')

print(tables[0].df)

print("===========")

print(tables[0].parsing_report)