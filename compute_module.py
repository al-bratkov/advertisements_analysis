import pandas as pd
import numpy as np
import scipy.stats as stats
from pandasql import sqldf

from datetime import date


def transform_input_values_for_sql(values):
    """
    Get a dictionary including values of features chosen by user.
    Returns the dictionary of values for applying in sql query
    :param values: a dictionary including values of features chosen by user
    :return: a dictionary of values for applying in sql query
    """
    cat_features = ("brand", "owners", "model", "body_type", "gearbox", "steering_wheel", "wheel_drive", "color")
    quant_features = ("power", "mileage", "car_year")
    features_for_sql = {}
    for key in cat_features:
        if values[key] != 'Не имеет значения':
            features_for_sql[key] = f"= '{values[key]}'"
    if values["is_climate"] == "true":
        features_for_sql[key] = f"= '{values[key]}'"
    for key in quant_features:
        if not values[key]:
            continue
        if key == "car_year" and values["year_sign"] == "younger":
            features_for_sql[key] = f">= {int(values[key])}"
        elif key == "power" and values["power_sign"] == "more":
            features_for_sql[key] = f">= {int(values[key])}"
        else:
            features_for_sql[key] = f"<= {int(values[key])}"
    return features_for_sql


def apply_settings(df, features):
    """

    :param df: a DataFrame for filtering
    :param features: a dictionary where keys are columns
    :return: a DataFrame cut for machine learning
    """
    ind = ["region", ]
    ind.extend(features.keys())
    df_cut = df.copy()
    cur_year = date.today().year
    df_cut["age"] = cur_year - df_cut["car_year"]
    for fea, val in features.items():
        query = f"SELECT * " \
                f"FROM df_cut " \
                f"WHERE {fea} {val}"
        df_cut = sqldf(query)
    return df_cut


def check_enough_number(df):
    """
    Find out which regions have enough number of notes in data
    :param df:
    :return:
    """
    reg_enough = df["region"].value_counts()
    reg_enough = reg_enough[reg_enough > 4]  # need to find out enough number
    df_enough = df[df["region"].isin(reg_enough.index)]
    return df_enough


def find_the_cheapest(df):
    prices = df.groupby("region")["price"].agg(("mean", "count")).sort_values("mean")
    mean_price = df.price.mean()
    prices["dif"] = mean_price - prices["mean"]
    cheap_regions = prices[prices.dif >= 0]
    return cheap_regions




#features = {"brand": "= 'ВАЗ (LADA)'", "model": "= 'Granta'", "age": , "mileage": , "count_owners": , "body_type": , "gearbox_type": , "en_power":,
#"gearbox_type": , "wheel_drive": , "steering_wheel": , "en_type": , "air_condition": , "color": }
# training_cols = ["brand", "model", "car_year", "mileage", "count_owners", "body_type", "gearbox_type", "en_power", "gearbox_type", "wheel_drive", "steering_wheel", "en_type", "is_climate", "color", "price"]