import pandas as pd
import numpy as np


def the_biggest(df):
    oldest = df[df["car_year"] == df["car_year"].min()][["brand", "model", "region", "city", "car_year", "link"]]
    cheapest = df[df["price"] == df["price"].min()][["brand", "model", "region", "city", "price", "link"]]
    exp = df[df["price"] == df["price"].max()][["brand", "model", "region", "city", "price", "link"]]
    longest_km = df[df["mileage"] == df["mileage"].max()][["brand", "model", "region", "city", "mileage", "link"]]
    colors = df.value_counts("color")
    rare_col = colors[colors == colors.min()].index[0]
    summary = {"oldest": oldest, "most_expensive": exp, "cheapest": cheapest, "most_mileage": longest_km, "rarest_color": colors[colors == colors.min()]}
    print(f"The oldest car in the dataset is {oldest['brand']} {oldest['model']} from {oldest['city']} - \
          {oldest['region']}. The car is manufactured in {oldest['car_year']}. \n{oldest['link']}")
    print(f"The most expensive car in the dataset is {exp['brand']} {exp['model']} from {exp['city']} - \
          {exp['region']}. The price is {exp['price']}. \n{exp['link']}")
    print(f"The cheapest car in the dataset is {cheapest['brand']} {cheapest['model']} from {cheapest['city']} - \
          {cheapest['region']}. The price is {cheapest['price']}. \n{cheapest['link']}")
    print(f"The maximum mileage is in the dataset {longest_km['mileage']}. The car is {longest_km['brand']} \
          {longest_km['model']} from {longest_km['city']} - {longest_km['region']}. \n{longest_km['link']}")
    print(f"The rarest color is in the dataset {rare_col}")
    return summary


def find_outliers(df):

