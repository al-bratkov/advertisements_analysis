import pandas as pd
import numpy as np
import scipy.stats as stats
from pandasql import sqldf

from datetime import date

html_df_schema = {"brand": "brand", "model": "model", "car_year": "car_year", "count_owners": "count_owners",
                  "body_type": "body_type", "wheel_drive": "wheel_drive", "steering_wheel": "steering_wheel",
                  "power": "en_power", "gearbox": "gearbox_type", "color": "color", "is_climate": "is_climate"}

class ServerDataFrame:
    def __init__(self, df):
        if type(df) != pd.DataFrame:
            raise TypeError("ServerDataFrame can get only pandas.DataFrame")
        self.df = df


    def extract_values_to_html(self):
        self.form = dict()
        self.form["brand"] = np.append("Не имеет значения", self.df.brand.unique()).tolist()
        self.form["owners"] = ["Не имеет значения"] + sorted(self.df.count_owners.unique().tolist())
        self.form["wheel_drive"] = np.append("Не имеет значения", self.df.wheel_drive.unique()).tolist()
        self.form["steering"] = np.append("Не имеет значения", self.df.steering_wheel.unique()).tolist()
        self.form["gearbox"] = np.append("Не имеет значения", self.df.gearbox_type.unique()).tolist()
        self.form["color"] = np.append("Не имеет значения", self.df.color.unique()).tolist()
        self.form["model"] = {brand: np.append("Не имеет значения", self.df[self.df.brand == brand].model.unique()).tolist()
                         for brand in self.df.brand.unique()}
        self.df["brand_model"] = self.df.brand + "|" + self.df.model
        self.form["body_type"] = {model: np.append("Не имеет значения", self.df[self.df.model == model].body_type.unique()).tolist()
                             for model in self.df.model.unique()}
        return self.form

    def transform_input_values_for_sql(self, values):
        """
        Get a dictionary including values of features chosen by user.
        Returns the dictionary of values for applying in sql query
        :param values: a dictionary including values of features chosen by user
        :return: a dictionary of values for applying in sql query
        """
        cat_features = (
        "brand", "count_owners", "model", "body_type", "gearbox", "steering_wheel", "wheel_drive", "color")
        quant_features = ("power", "mileage", "car_year")
        self.features_for_sql = {}
        for key in cat_features:
            if values[key] != 'Не имеет значения':
                self.features_for_sql[html_df_schema[key]] = f"= '{values[key]}'"
        if values["is_climate"] == "true":
            self.features_for_sql["is_climate"] = f"= True"
        for key in quant_features:
            if not key in values.keys():
                continue
            if key == "car_year" and values["year_sign"] == "younger":
                self.features_for_sql[html_df_schema[key]] = f">= {int(values[key])}"
            elif key == "power" and values["power_sign"] == "more":
                self.features_for_sql[html_df_schema[key]] = f">= {int(values[key])}"
            else:
                self.features_for_sql[html_df_schema[key]] = f"<= {int(values[key])}"
        return self.features_for_sql

    def apply_settings(self, features):
        """

        :param df: a DataFrame for filtering
        :param features: a dictionary where keys are columns
        :return: a DataFrame cut for machine learning
        """
        ind = ["region", ]
        ind.extend(features.keys())
        df_cut = self.df.copy()
        cur_year = date.today().year
        df_cut["age"] = cur_year - df_cut["car_year"]
        for fea, val in features.items():
            query = f"SELECT * " \
                    f"FROM df_cut " \
                    f"WHERE {fea} {val}"
            print(query)
            df_cut = sqldf(query)
        return df_cut

    def check_enough_number(self, df):
        """
        Find out which regions have enough number of notes in data
        :param df:
        :return:
        """
        reg_enough = df["region"].value_counts()
        reg_enough = reg_enough[reg_enough > 4]  # need to find out enough number
        self.df_enough = df[df["region"].isin(reg_enough.index)]
        return self.df_enough

    def find_the_cheapest(self, df):
        prices = df.groupby("region")["price"].agg(("mean", "count")).sort_values("mean")
        mean_price = df.price.mean()
        prices["dif"] = mean_price - prices["mean"]
        self.cheap_regions = prices[prices.dif >= 0]
        return self.cheap_regions

    def make_the_output(self):
        pass








class ServerDataFrame:
    def __init__(self, df):
        if type(df) != pd.DataFrame:
            raise TypeError("ServerDataFrame can get only pandas.DataFrame")
        self.df = df


    def extract_values_to_html(self):
        self.form = dict()
        self.form["brand"] = np.append("Не имеет значения", self.df.brand.unique()).tolist()
        self.form["owners"] = ["Не имеет значения"] + sorted(self.df.count_owners.unique().tolist())
        self.form["wheel_drive"] = np.append("Не имеет значения", self.df.wheel_drive.unique()).tolist()
        self.form["steering"] = np.append("Не имеет значения", self.df.steering_wheel.unique()).tolist()
        self.form["gearbox"] = np.append("Не имеет значения", self.df.gearbox_type.unique()).tolist()
        self.form["color"] = np.append("Не имеет значения", self.df.color.unique()).tolist()
        self.form["model"] = {brand: np.append("Не имеет значения", self.df[self.df.brand == brand].model.unique()).tolist()
                         for brand in self.df.brand.unique()}
        self.df["brand_model"] = self.df.brand + "|" + self.df.model
        self.form["body_type"] = {model: np.append("Не имеет значения", self.df[self.df.model == model].body_type.unique()).tolist()
                             for model in self.df.model.unique()}
        return self.form

    def transform_input_values_for_sql(self, values):
        """
        Get a dictionary including values of features chosen by user.
        Returns the dictionary of values for applying in sql query
        :param values: a dictionary including values of features chosen by user
        :return: a dictionary of values for applying in sql query
        """
        cat_features = (
        "brand", "count_owners", "model", "body_type", "gearbox", "steering_wheel", "wheel_drive", "color")
        quant_features = ("power", "mileage", "car_year")
        self.features_for_sql = {}
        for key in cat_features:
            if key in values and values[key] != 'Не имеет значения':
                self.features_for_sql[html_df_schema[key]] = f"= '{values[key]}'"
        if values["is_climate"] == "true":
            self.features_for_sql["is_climate"] = f"= True"
        for key in quant_features:
            if not key in values.keys():
                continue
            if key == "car_year" and values["year_sign"] == "younger":
                self.features_for_sql[html_df_schema[key]] = f">= {int(values[key])}"
            elif key == "power" and values["power_sign"] == "more":
                self.features_for_sql[html_df_schema[key]] = f">= {int(values[key])}"
            else:
                self.features_for_sql[html_df_schema[key]] = f"<= {int(values[key])}"

    def apply_settings(self):
        """

        :param df: a DataFrame for filtering
        :param features: a dictionary where keys are columns
        :return: a DataFrame cut for machine learning
        """
        ind = ["region", ]
        ind.extend(self.features_for_sql.keys())
        df_cut = self.df.copy()
        cur_year = date.today().year
        df_cut["age"] = cur_year - df_cut["car_year"]
        for fea, val in self.features_for_sql.items():
            query = f"SELECT * " \
                    f"FROM df_cut " \
                    f"WHERE {fea} {val}"
            print(query)
            df_cut = sqldf(query)
        return df_cut

    def check_enough_number(self, min_cars=5):
        """
        Find out which regions have enough number of notes in data
        :param self.df_cut:
        :return:
        """
        reg_enough = self.df_cut["region"].value_counts()
        reg_enough = reg_enough[reg_enough >= min_cars]  # need to find out enough number
        self.df_cut = self.df_cut[self.df_cut["region"].isin(reg_enough.index)]


    def find_the_cheapest(self):
        prices = self.df_cut.groupby("region")["price"].agg(("mean", "count")).sort_values("mean")
        mean_price = self.df.price.mean()
        prices["dif"] = mean_price - prices["mean"]
        self.cheap_regions = prices[prices.dif >= 0].sort_values("mean")
        return self.cheap_regions

    def make_the_output(self, values):
        self.transform_input_values_for_sql(values)
        self.df_cut = self.apply_settings()
        self.check_enough_number()
        self.find_the_cheapest()
        if self.df_cut.shape[0] == 0:
            return False
        else:
            return self.cheap_regions[:3]




#features = {"brand": "= 'ВАЗ (LADA)'", "model": "= 'Granta'", "age": , "mileage": , "count_owners": , "body_type": , "gearbox_type": , "en_power":,
#"gearbox_type": , "wheel_drive": , "steering_wheel": , "en_type": , "air_condition": , "color": }
# training_cols = ["brand", "model", "car_year", "mileage", "count_owners", "body_type", "gearbox_type", "en_power", "gearbox_type", "wheel_drive", "steering_wheel", "en_type", "is_climate", "color", "price"]