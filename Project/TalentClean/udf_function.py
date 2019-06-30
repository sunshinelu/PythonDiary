


def deal_field(field):
    """每个字段都需要进行的操作"""
    # 1.去除前后空格
    # 2.将无替换为null
    if field and isinstance(field, str):
        field = field.strip()
        if field == '无':
            field = None
    return field

def job_fill(item):
    if not item['job'] and item['position']:
        item['job'] = item['position']
    if item['job'] and not item['position']:
        item['position'] = item['job']

def deal_item(item):
    """
    对字段进行预先处理
    """
    item = item.map(lambda field: deal_field(field))

    # 职业与职务
    # 1.职业为None,职务不为None 职务填充职业
    # 2.职务为None,职业不为None,职业填充职务
    # 3.通过字典清洗职业字段
    job_fill(item)
    return item
