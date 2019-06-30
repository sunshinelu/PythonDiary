# -*- coding: utf-8 -*-

"""
中英文标点符号之间的互换
"""



def en_trans_to_ch(string):
    """
    英文符号转中文符号
    """
    E_pun = u',.!?[]()<>"\''
    C_pun = u'，。！？【】（）《》“‘'
    table = {ord(f): ord(t) for f, t in zip(E_pun, C_pun)}
    return string.translate(table)


def ch_trans_to_en(string):
    """
    中文符号转英文符号
    """
    E_pun = u',.!?[]()<>"\''
    C_pun = u'，。！？【】（）《》“‘'
    table = {ord(f): ord(t) for f, t in zip(C_pun, E_pun)}
    return string.translate(table)

if __name__ == '__main__':
    print(ch_trans_to_en("【]")) # []
    print(en_trans_to_ch("【]")) # 【】