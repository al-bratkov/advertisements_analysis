import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import scipy.stats as stats


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
    # find price outliers
    iqr = df["price"].quantile(0.75) - df["price"].quantile(0.25)
    whisker_h = df["price"].quantile(0.75) + 1.5 * iqr
    whisker_l = df["price"].quantile(0.25) - 1.5 * iqr
    out_price = df[(df["price"] > whisker_h) | (df["price"] < whisker_l)]
    if out_price.shape[0] > 15:
        print("There are more than 15 cars having too high or low price. Check the dataframe manually")
    else:
        for i in out_price.index:
            print(f"Enter 1 if {df.loc[i, 'brand']} {df.loc[i, 'model']} for {df.loc[i, 'price']} is not right note. Enter any other key if it is")
            print(df.loc[i, 'link'])
            inpt = input()
            if inpt == '1':
                df.drop(i, inplace=True)

    iqr = df["mileage"].quantile(0.75) - df["mileage"].quantile(0.25)
    whisker_h = df["mileage"].quantile(0.75) + 1.5 * iqr
    whisker_l = df["mileage"].quantile(0.25) - 1.5 * iqr
    out_miles = df[(df["mileage"] > whisker_h) | (df["mileage"] < whisker_l)]
    if out_miles.shape[0] > 15:
        print("There are more than 15 cars having too high or low mileage. Check the dataframe manually")
    else:
        for i in out_miles.index:
            print(f"Enter 1 if {df.loc[i, 'brand']} {df.loc[i, 'model']} for {df.loc[i, 'price']} is not right note. Enter any other key if it is")
            print(df.loc[i, 'link'])
            inpt = input()
            if inpt == '1':
                df.drop(i, inplace=True)


def show_distribution(df):
    print("Let's look at distribution of quantitative data: price, mileage, age and horsepower")
    fig, ax = plt.subplots(2, 2)



