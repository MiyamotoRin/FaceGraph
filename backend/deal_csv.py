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

        #[[0行0列, 0行1列, 0行2列], [1行0列, 1行1列, 1行2列], ...]を返す
    return data, columns, indexs
