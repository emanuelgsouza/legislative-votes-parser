from functools import reduce
from operator import concat


def flat_lists(lists):
    return reduce(concat, lists, [])


def save_data(df, filepath):
    df.to_csv(filepath, index=False)
