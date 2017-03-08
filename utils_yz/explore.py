# -*- coding: utf-8 -*-
import numpy as np
import pandas as pd

import utils_yz.base
import utils_yz.preprocessing


def df_col_is_unique_key(df, col):
    return df[col].unique().shape[0] == df.shape[0]


# numerical

def describe_numerical(x, percentiles=np.linspace(0, 1, 5)):
    d1 = {
        'count': x.shape[0],
        'mean': x.mean(),
        'sd': x.std(),
        'percent_nulls': x.isnull().sum() / float(x.shape[0]),
    }
    s1 = pd.Series(d1)
    s2 = x.dropna().quantile(percentiles)
    return pd.concat([s1, s2])


def df_describe_numerical_cols(df, cols):
    return df[cols].apply(describe_numerical)


# numerical by categorical


def df_describe_numerical_cols_by_categorical_col(df, numerical_cols, categorical_col,
                                                  percentiles=np.linspace(0, 1, 5)):
    return df.groupby(categorical_col)[numerical_cols].apply(lambda x: x.dropna().quantile(percentiles))


# categorical


def describe_categorical(x):
    return pd.Series(
        {
            'count': x.shape[0],
            'num_unique_value': x.nunique(),
            'percent_nulls': x.isnull().sum() / float(x.shape[0]),
        }
    )


def df_describe_categorical_cols(df, cols):
    return df[cols].apply(describe_categorical)


def df_categorical_col_value_percent(df, col):
    return df[col].value_counts(dropna=False).sort_values(ascending=False) / df.shape[0]


def df_describe_categorical_col_by_categorical_col(df, col_1, col_2):
    tb = utils_yz.base.df_table_r(df, col_1, col_2)
    return tb / tb.sum(axis=0)


if __name__ == '__main__':
    df = utils_yz.base.make_test_df()
    df = utils_yz.preprocessing.preprocess_test_df(df)
    print df.sample(5)
    print '-' * 50

    print 'df_col_is_unique_key'
    print df_col_is_unique_key(df, 'user_id')
    print '-' * 50

    target = 'has_churned'
    numerical_features = ['income', 'total_purchase']
    numerical_cols = [target] + numerical_features

    print 'df_describe_numerical_cols'
    print df_describe_numerical_cols(df, numerical_cols)
    print '-' * 50

    print 'df_describe_numerical_cols_by_categorical_col'
    print df_describe_numerical_cols_by_categorical_col(df, numerical_features, target)
    print '-' * 50

    categorical_features = ['price_plan', 'product_purchased', 'region']
    categorical_cols = [target] + ['price_plan', 'product_purchased', 'region']
    print 'df_describe_categorical_cols'
    print df_describe_categorical_cols(df, categorical_cols)
    print '-' * 50

    print 'df_categorical_col_value_percent'
    for col in categorical_cols:
        print df_categorical_col_value_percent(df, col)
    print '-' * 50

    print df['has_churned'].dtype

    print 'df_describe_categorical_col_by_categorical_col'
    for col in categorical_features:
        print df_describe_categorical_col_by_categorical_col(df, col, target)
    print '-' * 50