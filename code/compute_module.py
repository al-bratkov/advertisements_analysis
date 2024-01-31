import pandas as pd
import numpy as np
import scipy.stats as stats
from pandasql import sqldf
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, mean_absolute_error
from sklearn.model_selection import GridSearchCV, RandomizedSearchCV

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
        """
        Give valid values from a dataset for filling the forms on the html page
        :return: a dictionary where the values are lists of unique values
        """
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
        :param min_cars: count of cars in a region that is a threshold
        :return: a DataFrame including only regions having enough count of cars
        """
        reg_enough = self.df_cut["region"].value_counts()
        reg_enough = reg_enough[reg_enough >= min_cars]  # need to find out enough number
        self.df_cut = self.df_cut[self.df_cut["region"].isin(reg_enough.index)]


    def find_the_cheapest(self):
        """

        :return:
        """
        prices = self.df_cut.groupby("region")["price"].agg(("mean", "count")).sort_values("mean")
        mean_price = self.df.price.mean()
        prices["dif"] = mean_price - prices["mean"]
        self.cheap_regions = prices[prices.dif >= 0].sort_values("mean")
        return self.cheap_regions

    def make_the_output(self, values):
        """

        :param values:
        :return:
        """
        self.transform_input_values_for_sql(values)
        self.df_cut = self.apply_settings()
        self.check_enough_number()
        self.find_the_cheapest()
        if self.df_cut.shape[0] == 0:
            return False
        else:
            return self.cheap_regions[:3]

    def make_x_pred(self):
        x_predict = pd.get_dummies(self.df.region.unique(), prefix="region")


# the code below is for future updates
'''
def preprocess(df):
    df["brand_model"] = df.brand + "/" + df.model
    df["age"] = 2023 - df.car_year
    dummies = pd.get_dummies(df[['count_owners', 'is_climate','color', 'steering_wheel', 'is_owner', 'region',
                                 'en_type', 'body_type', 'gearbox_type', 'wheel_drive', 'brand', 'model']])
    X = pd.concat([df[['mileage', 'en_capacity', 'en_power', 'fuel_waste_mix',
                       'age']], dummies], axis=1)
    y = df.price
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    parameters = {"max_depth": list(range(10, 60, 5)), "min_samples_split": list(range(2, 10)), "min_samples_leaf": list(range(1, 10))}
    model = RandomForestRegressor(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)

    search = GridSearchCV(model, parameters, cv=5)
    search.fit(X_train, y_train)
    best_forest = search.best_estimator_
    {'max_depth': 15, 'min_samples_leaf': 2, 'min_samples_split': 9}

    x_predict = pd.get_dummies(df.region.unique(), prefix="region")
    X = pd.DataFrame({col: [False] * x_predict.shape[0] for col in model.feature_names_in_})
    for col in model.feature_names_in_:
        X.loc[:, col] = x_predict.loc[:col]
    y_pred = model.predict(X_test)
    comparison = pd.DataFrame({"ML": y_pred, "real": y_test})
    comparison["difference"] = comparison.ML - comparison.real
    mse = mean_squared_error(y_test, y_pred)
    mae = mean_absolute_error(y_test, y_pred)
    for key in features_for_sql.keys():
        if not key in ["brand", "model"]:
            x_predict[key] = True
    if "brand" in features_for_sql.keys() and "model" in features_for_sql.keys()
    x_predict[f'brand_model_{features_for_sql["brand"]}/{features_for_sql["model"]}'] = True


trees = model.estimators_
t = trees[0]
decisions = pd.DataFrame({"children_left": t.tree_.children_left, "children_right": t.tree_.children_right, "feature": t.tree_.feature, "impurity": t.tree_.impurity, "missing_go_to_left": t.tree_.missing_go_to_left, "n_node_samples": t.tree_.n_node_samples, "threshold": t.tree_.threshold, "value": t.tree_.value[:, 0, 0], "weighted_n_node_samples": t.tree_.weighted_n_node_samples})


X_fake = X_test.drop(X_test.index)
X_regions = pd.get_dummies(df.region.unique(), prefix="region")
X_fake[X_regions.columns.values] = X_regions
for col in X_fake.dtypes[~(X_fake.dtypes == "object")].index:
    X_fake[col] = X[col].median()
for col in X_fake.dtypes[X_fake.dtypes == "object"].index:
    X_fake[col] = X[col].mode()[0]
X_regions = pd.get_dummies(df.region.unique(), prefix="region")'''