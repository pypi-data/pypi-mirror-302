#  Copyright (c) 2023. ISTMO Center S.A.  All Rights Reserved
#

import datetime
import os
import time
from typing import Any, Dict, Type
import pandas as pd
from tqdm import tqdm

from .df_utils import add_df_totals

from .log_utils import Logger

logger = Logger(log_dir='./logs/', logger_name=__name__, log_file=f'{__name__}.log')


def convert_value_pairs(row):
    if row['value_type'] == "datetime":
        converted_value = datetime.datetime.strptime(row['value'], '%Y-%m-%d %H:%M:%S')
    elif row['value_type'] == 'str':
        converted_value = row['value']
    else:
        converted_value = eval(f"{row['value_type']}({row['value']})")
    return converted_value


def get_timeseries_params(df_params) -> Any:
    index_col = None
    ts_params = df_params
    if ts_params.get("datetime_index", False):
        index_col = ts_params.get('index_col', None)
        pop_cols = ['datetime_index', 'index_col']
        for p in pop_cols:
            ts_params.pop(p, None)
    return index_col, ts_params


def format_fields(df, format_options):
    for fld_name, fld_type in format_options.items():
        if fld_name in df.columns:
            df[fld_name] = df[fld_name].values.astype(fld_type)
    return df


def fillna_fields(df, fill_options):
    for fld_name, fill_value in fill_options.items():
        if fld_name in df.columns:
            df.fillna({fld_name: fill_value}, inplace=True)
    return df


def cast_cols_as_categories(df, threshold=100):
    for col in df.columns:
        if df[col].dtype in ['object', 'string'] and len(df[col].unique()) < threshold:
            df[col] = df[col].astype(pd.CategoricalDtype())
    return df


def load_as_timeseries(df, **options):
    index_col = options.get("index_col", None)
    if index_col is not None and df.index.name != index_col:
        if index_col in df.columns:
            df.reset_index(inplace=True)
            df.set_index(index_col, inplace=True)
    rule = options.pop("rule", "D")
    index = options.pop("index", df.index)
    cols = options.pop("cols", None)
    vals = options.pop("vals", None)
    totals = options.pop("totals", False)
    agg_func = options.pop("agg_func", 'count')
    df = df.pivot_table(index=index, columns=cols, values=vals, aggfunc=agg_func).fillna(0)
    df = df.resample(rule=rule).sum()
    df.sort_index(inplace=True)
    if totals:
        df = add_df_totals(df)
    return df


def fix_fields(df, fields_to_fix, field_type):
    field_attributes = {
        'str': {'default_value': '', 'dtype': str},
        'int': {'default_value': 0, 'dtype': int},
        'date': {'default_value': pd.NaT, 'dtype': 'datetime64[ns]'},
        'datetime': {'default_value': pd.NaT, 'dtype': 'datetime64[ns]'}
    }

    if field_type not in field_attributes:
        raise ValueError("Invalid field type: {}".format(field_type))

    attr = field_attributes[field_type]
    fields = [field for field in fields_to_fix if field in df.columns]
    df[fields] = df[fields].fillna(attr['default_value']).astype(attr['dtype'])


def merge_lookup_data(classname, df, **kwargs):
    """
    kwargs={
        'source_col':'marital_status_id',
        'lookup_description_col':'description',
        'lookup_col':'id',
        'source_description_alias':'marital_status_description',
        'fillna_source_description_alias': True
    }
    :param classname:
    :param df:
    :param kwargs:
    :return:
    """
    if df.empty:
        return df
    source_col = kwargs.pop('source_col', None)
    lookup_col = kwargs.pop('lookup_col', None)
    lookup_description_col = kwargs.pop('lookup_description_col', None)
    source_description_alias = kwargs.pop('source_description_alias', None)
    fillna_source_description_alias = kwargs.pop('fillna_source_description_alias', False)
    fieldnames = kwargs.get('fieldnames', None)
    column_names = kwargs.get('column_names', None)

    if source_col is None or lookup_description_col is None or source_description_alias is None or lookup_col is None:
        raise ValueError(
            'source_col, lookup_col, lookup_description_col and source_description_alias must be specified')
    if source_col not in df.columns:
        # raise ValueError(f'{source_col} not in dataframe columns')
        return df
    ids = list(df[source_col].dropna().unique())
    if not ids:
        return df
    if fieldnames is None:
        kwargs['fieldnames'] = (lookup_col, lookup_description_col)
    if column_names is None:
        kwargs['column_names'] = ['temp_join_col', source_description_alias]
    kwargs[f'{lookup_col}__in'] = ids
    result = classname(live=True).load(**kwargs)
    if 'temp_join_col' in kwargs.get("column_names"):
        temp_join_col = 'temp_join_col'
    else:
        temp_join_col = lookup_col

    df = df.merge(result, how='left', left_on=source_col, right_on=temp_join_col)
    if fillna_source_description_alias:
        if source_description_alias in df.columns:
            df.fillna({source_description_alias: ''}, inplace=True)
    if 'temp_join_col' in df.columns:
        df.drop(columns='temp_join_col', inplace=True)
    return df


