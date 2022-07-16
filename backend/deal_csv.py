import pandas as pd
import numpy as np

def deal_csv(csv_path):
    #index0列目，columns0行目を想定
    data = pd.read_csv(csv_path, encoding="shift jis", index_col=0)
    columns = list(data.columns)
    indexs = list(data.index)
    #-20 ~ 20 への写像　写像ってナンスか？わかるよね？？
    for c in columns:
        data[c] = 40*(data[c] - data[c].min())/(data[c].max()-data[c].min())-20
    
    #columns, indexsの最大数の制限
    # 10個まで
    if(len(columns) > 10):
        columns = columns[0:10]
    if(len(indexs) > 10):
        indexs = indexs[0:10]


    return data, columns, indexs
