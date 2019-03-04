from functools import reduce
from operator import concat


def flat_lists(lists):
    return reduce(concat, lists, [])


def save_data(df, filepath):
    df.to_csv(filepath, index=False)


def get_states(df):
    return df['sigla_uf'].unique()


def get_legend_composition(df):
    return df['composicao_legenda'].unique()


def get_parties_by_coligation(coligation):
    return coligation.split(' / ')


def omit(obj, _key):
    return { key:val for key, val in obj.items() if key != _key }
