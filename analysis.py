# -*- coding: utf-8 -*-

from __future__ import absolute_import

import pandas as pd
import argparse
import os

DATA_ROOT = os.path.join(os.environ['HOME'], 'data')
valid_jobs = ['u', 'd']

def parse_args():
    parser = argparse.ArgumentParser(description='Perform basic analytics.')
    parser.add_argument('-f', '--file', dest='data_file', required=True, 
                        help='the name of the data file under ~/data')
    parser.add_argument('-o', '--output', dest='out_file', required=True,
                        help='path to the output file')
    parser.add_argument('-c', '--category', dest='category',
                        help='the category whose distribution we want to get')
    return vars(parser.parse_args())

def insert_or_update(data_key, distribution_dict):
    if data_key in distribution_dict.keys():
        distribution_dict[data_key] += 1
    else:
        distribution_dict[data_key] = 1
    return distribution_dict

def get_data_distribution(data_list):
    distribution = dict()
    total_count = float(len(data_list))
    for data_point in data_list:
        distribution = insert_or_update(data_point, distribution)
    for key in distribution.keys():
        distribution[key] /= total_count
    return distribution

def write_dictionary_data(dictionary, out_file):
    with open(out_file, 'w') as f:
        f.write('category,percentage\n')
        for key in dictionary.keys():
            f.write('{},{}\n'.format(key, dictionary[key]))

def count_unique_job(dataframe, out_file):
    # count the number of unique entries for each column in the dataframe
    headers = dataframe.columns.values.tolist()
    with open(out_file, 'w') as f:
        f.write('column_name,unique_count\n')
        for column_name in headers:
            count = len(dataframe[column_name].unique())
            f.write('{},{}\n'.format(column_name, count))

def category_distribution_job(dataframe, category, out_file):
    # calculate the distribution of categorical data entries in the dataframe
    if category is None:
        raise KeyError('Category name is not provided! Check --help.')
    elif category not in dataframe.columns.values:
        msg = 'Category "{}" does not exist in the data file! Check --help.'
        raise ValueError(msg.format(category))
    else:
        categorical_distribution = get_data_distribution(dataframe[category])
        write_dictionary_data(categorical_distribution, out_file)

def user_select_job_mode():
    # prompt user to select a valid job mode and return the user's selection
    prompt = '''
    Please select one of the following analytical jobs:
        1) To count number of unique column entries, enter "u"
        2) To get distribution of categorical data, enter "d"
    '''
    user_input = None
    while not user_input:
        user_input = raw_input(prompt).lower()
        if user_input not in valid_jobs:
            print('Invalid job mode! Please select from {}'.valid_jobs)
            user_input = None
    # return the user-selected job mode
    return user_input


if __name__ == '__main__':
    args_dict = parse_args()
    data_file = os.path.join(DATA_ROOT, args_dict['data_file'])
    out_file = args_dict['out_file']
    df = pd.read_csv(data_file)
    job_mode = user_select_job_mode()

    if job_mode == 'u':
        count_unique_job(df, out_file)
    elif job_mode == 'd':
        category = args_dict.get('category', None)
        category_distribution_job(df, category, out_file)

