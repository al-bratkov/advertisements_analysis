import pandas as pd
import sqlalchemy as sql


table_advertisement = ["avito_id", "fk_car_id", "is_owner", "is_promo", "fk_region_code", "fk_city_id", "link", "ad_date"]
table_region = ["region_code", "region"]
table_city = ["city_id", "city", "fk_region_code"]
table_car = ["car_id", "fk_model_id", "fk_modification_id", "vin", "year", "mileage", "count_owners",
               "air_condition", "color", "price",]
table_model = ["model_id", "brand", "model"]
table_modification = ["modification_id", "fk_model_id", "model_uid", "en_capacity", "en_type", "en_power",
               "num_cylinders", "fuel_waste_mix", "body_type", "modification", "num_doors", "gearbox_type",
               "wheel_drive", "steering_wheel"]

def to_database(auto_db):
    pass

