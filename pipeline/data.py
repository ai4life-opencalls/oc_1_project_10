import numpy as np
import flowkit as fk


def process_df(df):
    total_rows = len(df)
    # drop columns with too much nan values or fixed values
    drop_cols = []
    for col_name in df.columns:
        col = df[col_name]
        if col.isnull().sum() > int(total_rows * 0.25):
            drop_cols.append(col_name)
        elif np.allclose(col.mean(), col):  # fixed values
            drop_cols.append(col_name)

    return df, drop_cols


def get_df(sample_file):
    sample = fk.Sample(sample_file)
    df = sample.as_dataframe(source="raw")
    df.columns = df.columns.droplevel(1)  # drop pns
    df, drop_cols = process_df(df)

    return df, drop_cols
