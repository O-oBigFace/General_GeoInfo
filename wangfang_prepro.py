"""
    预处理万方学者源数据、
    将excel表中的机构数据去重，汇总成表格并保存下来
"""
from settings import *
import pickle
import os
import pandas as pd
from Logger import logger

def get_wangfang_affi():
    # check existence
    if os.path.exists(pkl_affi_wangfang_path):
        logger.info("EXISTED - Wangfang affiliation information has EXISTED!")
        return pickle.load(open(pkl_affi_wangfang_path, "rb"))

    table = pd.read_excel(xlsx_wangfang_path)
    affi_set = list(set(table.iloc[:,4].tolist()))
    for ix, item in enumerate(affi_set):
        affi_set[ix] = item.replace("\\", " ").replace("/", " ").replace(":", " ")

    pickle.dump(affi_set, open(pkl_affi_wangfang_path, "wb"))
    logger.info("EXTRACT - Wangfang affiliation information has been EXTRACTED!")
    return affi_set

if __name__ == '__main__':
    get_wangfang_affi()
