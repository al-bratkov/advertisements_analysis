import pandas as pd


table_advertisement = ["fk_car_id", "is_owner", "is_promo", "region", "city", "link", "ad_date", "avito_id"]
table_car = ["fk_car_id", "fk_model_id", "fk_modification_id", "vin", "year", "mileage", "count_owners",
               "air condition", "color", "price",]
table_model = ["fk_model_id", "brand", "model"]
table_modification = ["fk_modification_id", "fk_model_id", "model_uid", "en_capacity", "en_type", "en_power",
               "num_cylinders", "fuel_waste_mix", "body_type", "modification", "num_doors", "gearbox_type",
               "wheel_drive", "steering_wheel"]

