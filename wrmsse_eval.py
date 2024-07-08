import pandas as pd
import numpy as np


def convert_to_42840(df, cols, groups):
    """
    Transforms the original 30490 time-series data into 42840 time-series
    by grouping based on the 12-level hierarchy.

    Parameters:
    df (pd.DataFrame): Original time-series dataframe.
    cols (list): Columns representing the time-series data.
    groups (list): Grouping keys for the hierarchical levels.

    Returns:
    pd.DataFrame: Transformed 42840 time-series data.
    """
    series_gen = {}
    for i, grp in enumerate(groups):
        # Group by hierarchical levels and sum the sales for each day
        tmp = df.groupby(grp)[cols].sum()
        # Store the aggregate sales values for each group
        for j in range(len(tmp)):
            series_gen[gen_series_name(tmp.index[j])] = tmp.iloc[j].values
    return pd.DataFrame(series_gen).T




def gen_series_name(name):
    """
    Generates a unique string name for each group.

    Parameters:
    name (tuple or str): Group name, which can be a tuple or a single string.

    Returns:
    str: Unique string name for the group.
    """
    if isinstance(name, str) | isinstance(name, int):
        return str(name)
    else:
        return "__".join(name)



def compute_weights(train_df,valid_df,weight_cols,groups,fix_cols, calendar_df, prices_df):
    weights_map = {}
    weight_df = train_df[["item_id", "store_id"] + weight_cols]
    weight_df = pd.melt(weight_df,id_vars=["item_id", "store_id"],var_name='d',value_name='sales')
    weight_df = weight_df.merge(calendar_df[['wm_yr_wk','d']], on='d', how='left')
    weight_df = weight_df.merge(prices_df, how="left", on=["item_id", "store_id", "wm_yr_wk"])
    #computing dollar sales
    weight_df["dollar_sales"] = weight_df["sales"] * weight_df["sell_price"]
    weight_df = weight_df.set_index(["item_id", "store_id", "d"]).unstack(level=2)["dollar_sales"]
    weight_df = weight_df.loc[zip(train_df.item_id, train_df.store_id), :].reset_index(drop=True)
    weight_df = pd.concat([train_df[fix_cols], weight_df],
                          axis=1, sort=False)
    #computing the weights for each group keys
    for i,grp in enumerate(groups):
        ser_weight = weight_df.groupby(grp)[weight_cols].sum().sum(axis=1)
        ser_weight = ser_weight / ser_weight.sum()
        for j in range(len(ser_weight)):
            weights_map[gen_series_name(ser_weight.index[j])] = np.array([ser_weight.iloc[j]])
    weights = pd.DataFrame(weights_map).T / len(groups) #creating a dataframe with weights corresponding to each group keys of 42840 hierachical time-series
    return weights

# def compute_weights(train_df, weight_cols, groups, fix_cols, calendar_df, prices_df):
#     """
#     Computes the weights for each of the 42840 series using the last 28 days
#     of sales and their prices.
#
#     Parameters:
#     train_df (pd.DataFrame): Training dataset.
#     weight_cols (list): Columns representing the last 28 days of data.
#     groups (list): Grouping keys for the hierarchical levels.
#     fix_cols (list): Fixed identifier columns.
#     calendar_df (pd.DataFrame): Calendar dataframe.
#     prices_df (pd.DataFrame): Prices dataframe.
#
#     Returns:
#     pd.DataFrame: Weights for the 42840 series.
#     """
#     weights_map = {}
#     weight_df = train_df[["item_id", "store_id"] + weight_cols]
#     weight_df = weight_df.melt(id_vars=["item_id", "store_id"], var_name='d', value_name='sales')
#     weight_df = weight_df.merge(calendar_df[['wm_yr_wk', 'd']], on='d', how='left')
#     weight_df = weight_df.merge(prices_df, on=["item_id", "store_id", "wm_yr_wk"])
#     weight_df["dollar_sales"] = weight_df["sales"] * weight_df["sell_price"]
#     weight_df = weight_df.set_index(["item_id", "store_id", "d"]).unstack(level=2)["dollar_sales"]
#     weight_df = weight_df.loc[zip(train_df.item_id, train_df.store_id), :].reset_index(drop=True)
#     weight_df = pd.concat([train_df[fix_cols], weight_df], axis=1, sort=False)
#
#     for i,grp in enumerate(groups):
#         ser_weight = weight_df.groupby(grp)[weight_cols].sum().sum(axis=1)
#         ser_weight = ser_weight / ser_weight.sum()
#         for j in range(len(ser_weight)):
#             weights_map[gen_series_name(ser_weight.index[j])] = np.array([ser_weight.iloc[j]])
#     return pd.DataFrame(weights_map).T / len(groups)

def compute_rmsse(train_df, valid_df, pred_df):
    """
    Computes the Root Mean Squared Scaled Error (RMSSE).

    Parameters:
    train_df (pd.DataFrame): Training dataset.
    valid_df (pd.DataFrame): Validation dataset (true values).
    pred_df (pd.DataFrame): Predicted values.

    Returns:
    pd.Series: RMSSE for each series.
    """
    scales = []
    for i in range(len(train_df)):
        val = train_df.iloc[i].values
        val = val[np.argmax(val != 0):]
        scale = ((val[1:] - val[:-1]) ** 2).mean()
        scales.append(scale)
    scale_arr = np.array(scales)
    mse = ((pred_df - valid_df) ** 2).mean(axis=1)
    rmsse = np.sqrt(mse / scale_arr)
    return rmsse


def calculate_wrmsse_score(train_df, valid_df, pred_df, weights):
    """
    Computes the final Weighted Root Mean Squared Scaled Error (WRMSSE).

    Parameters:
    train_df (pd.DataFrame): Training dataset.
    valid_df (pd.DataFrame): Validation dataset (true values).
    pred_df (pd.DataFrame): Predicted values.
    weights (pd.DataFrame): Weights for each series.

    Returns:
    float: WRMSSE score.
    """
    rmsse = compute_rmsse(train_df, valid_df, pred_df)
    weighted_rmsse = pd.concat([weights, rmsse], axis=1, sort=False).prod(axis=1)
    return np.sum(weighted_rmsse)