# -*- coding: utf-8 -*-

from __future__ import absolute_import

import pandas as pd
import os

def count_unique(column):
    # return the number of unique values in a column
    return len(column.unique())

if __name__ == '__main__':
    data_file = os.path.join(os.environ['HOME'], 'data/merchants.csv')
    df = pd.readcsv(data_file)
    headers = df.df.columns.values.tolist()
    print('column_name,unique_count')
    for column_name in headers:
        count = count_unique(df[column_name])
        print('{},{}'.format(column_name, count))
