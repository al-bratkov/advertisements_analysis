import pandas as pd
import sqlalchemy as sql
import psycopg2


fed_counts = {0: 'Центральный', 1: 'Северо-Западный', 2: 'Южный', 3: 'Северо-Кавказский', 4: 'Приволжский', 5: 'Уральский', 6: 'Сибирский', 7: 'Дальневосточный'}
regions = {'01': 'Республика Адыгея', '02': 'Республика Башкортостан', '03': 'Республика Бурятия',
           '04': 'Республика Алтай (Горный Алтай)', '05': 'Республика Дагестан', '06': 'Республика Ингушетия',
           '07': 'Кабардино-Балкарская Республика', '08': 'Республика Калмыкия', '09': 'Карачаево-Черкесская Республика',
           '10': 'Республика Карелия', '11': 'Республика Коми', '12': 'Республика Марий Эл', '13': 'Республика Мордовия',
           '14': 'Республика Саха (Якутия)', '15': 'Республика Северная Осетия — Алания', '16': 'Республика Татарстан',
           '17': 'Республика Тыва', '18': 'Удмуртская Республика', '19': 'Республика Хакасия', '21': 'Чувашская Республика',
           '22': 'Алтайский край', '23': 'Краснодарский край', '24': 'Красноярский край', '25': 'Приморский край',
           '26': 'Ставропольский край', '27': 'Хабаровский край', '28': 'Амурская область', '29': 'Архангельская область',
           '30': 'Астраханская область', '31': 'Белгородская область', '32': 'Брянская область', '33': 'Владимирская область',
           '34': 'Волгоградская область', '35': 'Вологодская область', '36': 'Воронежская область', '37': 'Ивановская область',
           '38': 'Иркутская область', '39': 'Калининградская область', '40': 'Калужская область', '41': 'Камчатский край',
           '42': 'Кемеровская область', '43': 'Кировская область', '44': 'Костромская область', '45': 'Курганская область',
           '46': 'Курская область', '47': 'Ленинградская область', '48': 'Липецкая область', '49': 'Магаданская область',
           '50': 'Московская область', '51': 'Мурманская область', '52': 'Нижегородская область', '53': 'Новгородская область',
           '54': 'Новосибирская область', '55': 'Омская область', '56': 'Оренбургская область', '57': 'Орловская область',
           '58': 'Пензенская область', '59': 'Пермский край', '60': 'Псковская область', '61': 'Ростовская область',
           '62': 'Рязанская область', '63': 'Самарская область', '64': 'Саратовская область', '65': 'Сахалинская область',
           '66': 'Свердловская область', '67': 'Смоленская область', '68': 'Тамбовская область', '69': 'Тверская область',
           '70': 'Томская область', '71': 'Тульская область', '72': 'Тюменская область', '73': 'Ульяновская область',
           '74': 'Челябинская область', '75': 'Забайкальский край', '76': 'Ярославская область', '77': 'Москва',
           '78': 'Санкт-Петербург', '79': 'Еврейская автономная область', '82': 'Республика Крым',
           '83': 'Ненецкий автономный округ', '86': 'Ханты-Мансийский автономный округ — Югра',
           '87': 'Чукотский автономный округ', '89': 'Ямало-Ненецкий автономный округ', '92': 'Севастополь',
           '94': 'Территории за пределами РФ, обслуживаемые Департаментом режимных объектов МВД России',
           '95': 'Чеченская Республика'}



def to_model_db(df, con, schema):
    """
    Add information to table 'model'
    :param df: a dataframe with all information
    :param con: connection to a database. An object is created with create_engine function of sqlalchemy module
    :param schema: a dict with names of tables in database
    :return: no return. Change the input dataframe
    """
    df_model = df[["brand", "model"]].drop_duplicates()
    db_model = pd.read_sql(f"SELECT brand, model FROM {schema['model']}", con)
    db_model["join"] = db_model["brand"].str[:] + "_" + db_model["model"].str[:]
    df_model["join"] = df_model["brand"].str[:] + "_" + df_model["model"].str[:]
    new_models = df_model[~df_model["join"].isin(db_model["join"])][["brand", "model"]]
    new_models.to_sql(schema['model'], con, index=False, if_exists="append")
    print(f"{new_models.shape[0]} rows are added to the table {schema['model']}")


def to_modification_db(df, con, schema):
    """
    Add information to table 'modification'
    :param df: a dataframe with all information
    :param con: connection to a database. An object is created with create_engine function of sqlalchemy module
    :param schema: a dict with names of tables in database
    :return: no return. Change the input dataframe
    """
    df_mod = df[["brand", "model", "model_uid", "en_capacity", "en_type", "en_power",
                 "num_cylinders", "fuel_waste_mix", "body_type", "modification", "num_doors", "gearbox_type",
                 "wheel_drive"]].drop_duplicates()
    df_mod["fk_model_id"] = df_mod["brand"].str[:] + "_" + df_mod["model"].str[:]
    db_model = pd.read_sql(f"SELECT * FROM {schema['model']}", con)
    db_model["join"] = db_model["brand"].str[:] + "_" + db_model["model"].str[:]
    model_i = {d_m: i for i, d_m in db_model[["model_id", "join"]].set_index("model_id")["join"].to_dict().items()}
    df_mod["fk_model_id"].replace(model_i, inplace=True)
    df_mod.drop(["brand", "model"], axis=1, inplace=True)
    db_mod = pd.read_sql(f"SELECT model_uid FROM {schema['modification']}", con)
    new_mods = df_mod[~df_mod["model_uid"].isin(db_mod["model_uid"])]
    new_mods.to_sql(schema['modification'], con, index=False, if_exists="append")
    print(f"{new_mods.shape[0]} rows are added to the table {schema['modification']}")


def to_car_db(df, con, schema):
    """
    Add information to table 'car'
    :param df: a dataframe with all information
    :param con: connection to a database. An object is created with create_engine function of sqlalchemy module
    :param schema: a dict with names of tables in database
    :return: no return. Change the input dataframe
    """
    last_car_i = pd.read_sql(f"SELECT MAX(car_id) FROM {schema['car']}", con)["max"][0]
    df["car_id"] = range(last_car_i+1, last_car_i+1+df.shape[0])
    df_car = df[["brand", "model", "model_uid", "vin", "year", "mileage", "count_owners",
                 "air_condition", "steering_wheel", "color", "price", "car_id"]]
    df_car["model_id"] = df_car["brand"].str[:] + "_" + df_car["model"].str[:]
    db_model = pd.read_sql(f"SELECT * FROM {schema['model']}", con)
    db_model["join"] = db_model["brand"].str[:] + "_" + db_model["model"].str[:]
    model_i = {d_m: i for i, d_m in db_model[["model_id", "join"]].set_index("model_id")["join"].to_dict().items()}
    df_car["model_id"].replace(model_i, inplace=True)
    df_car.drop(["brand", "model"], axis=1, inplace=True)
    df_car.columns = ['model_uid', 'vin', 'car_year', 'mileage', 'count_owners', 'is_climate',
                      'steering_wheel', 'color', 'price', 'car_id', 'model_id']
    # need to fix double prices
    df_car.to_sql("car", con, index=False, if_exists="append")
    print(f"{df_car.shape[0]} rows are added to the table {schema['car']}")


def to_city_db(df, con, schema):
    """
    Add information to table 'city'
    :param df: a dataframe with all information
    :param con: connection to a database. An object is created with create_engine function of sqlalchemy module
    :param schema: a dict with names of tables in database
    :return: no return. Change the input dataframe
    """
    df_city = df[["city", "region"]].drop_duplicates()
    db_region = pd.read_sql(f"SELECT region_code, region FROM {schema['region']}", con)
    region_i = {name: i for i, name in
                db_region[["region_code", "region"]].set_index("region_code")["region"].to_dict().items()}
    df_city["region"].replace(region_i, inplace=True)
    df_city.columns = ['city', 'region_code']
    db_city = pd.read_sql(f"SELECT city FROM {schema['city']}", con)
    new_cities = df_city[~df_city["city"].isin(db_city["city"])]
    new_cities.to_sql(schema['city'], con, index=False, if_exists="append")
    print(f"{new_cities.shape[0]} rows are added to the table {schema['city']}")


def to_advertisement_db(df, con, schema):
    """
    Add information to table 'advertisement'
    :param df: a dataframe with all information
    :param con: connection to a database. An object is created with create_engine function of sqlalchemy module
    :param schema: a dict with names of tables in database
    :return: no return. Change the input dataframe
    """
    # need to fix double avito_id
    df_ad = df[["avito_id", "is_owner", "is_promo", "city", "link", "ad_date", "car_id"]]
    db_city = pd.read_sql(f"SELECT city, city_id FROM {schema['city']}", con)
    city_i = {d_m: i for i, d_m in db_city[["city_id", "city"]].set_index("city_id")["city"].to_dict().items()}
    df_ad["city"].replace(city_i, inplace=True)
    df_ad.columns = ["avito_id", "is_owner", "is_promo", "city_id", "link", "ad_date", "car_id"]
    df_ad.to_sql("advertisement", con, index=False, if_exists="append")
    print(f"{df_ad.shape[0]} rows are added to the table {schema['advertisement']}")


def to_database(df, auto_db, login, password):
    schema = {"advertisement": "advertisement", "car": "car", "city": "city", "fed_count": "fed_count",
              "region": "region",
              "model": "model", "modification": "modification"}
    con = sql.create_engine(f"postgresql+psycopg2://{login}:{password}@localhost/{auto_db}")
    to_model_db(df, con, schema)
    to_modification_db(df, con, schema)
    to_city_db(df, con, schema)
    to_car_db(df, con, schema)
    to_advertisement_db(df, con, schema)
    print("The dataframe is imported to the database")


def id_from_db(con, schema):
    # con = sql.create_engine(f"postgresql+psycopg2://{login}:{password}@localhost/{auto_db}")
    avito_id = pd.read_sql(f"SELECT avito_id FROM {schema['advertisement']}", con)
    uid = pd.read_sql(f"SELECT * FROM {schema['modification']}", con)
    return {"avito_id": avito_id, "model_uid": uid}


def get_all_db(con, schema):
    query = f"WITH sub_city AS (\
        SELECT city_id, city, region \
	    FROM {schema['city']} \
	    INNER JOIN {schema['region']} \
	    USING(region_code)), \
    sub_model AS (SELECT brand, model, model_uid, en_capacity, en_type, en_power, num_cylinders, fuel_waste_mix, \
        body_type, modification, num_doors, gearbox_type, wheel_drive \
	    FROM {schema['model']} \
	    INNER JOIN {schema['modification']} \
	    ON fk_model_id = model_id) \
	SELECT avito_id, vin, brand, model, car_year, mileage, count_owners, is_climate, color, price, steering_wheel, \
	    is_owner, is_promo, city, region, link, ad_date \
    FROM {schema['advertisement']} AS ad\
    INNER JOIN (\
	SELECT car_id, vin, brand, model, mileage, count_owners, is_climate, color, price, steering_wheel, car_year, \
	    en_capacity, en_type, en_power, num_cylinders, fuel_waste_mix, body_type, modification, num_doors, gearbox_type, \
	    wheel_drive\
    FROM {schema['car']} \
	INNER JOIN sub_model\
    USING(model_uid)) as car_model\
    USING(car_id)\
    INNER JOIN sub_city\
    USING(city_id)"
    df = pd.read_sql(query, con)
    return df


right_uids = {1: "2888849526", 63: "2727509782", 164: "2446427534", 167: "2635611458"}  # for NaN and wrong uids
right_price = {511: 289000.00, 874: 195000.00, 1057: 87000.00, 1172: 125000.00, 1233: 165000.00, 1254: 129000.00,
                   1591: 295000.00}
double_id = [43, 42, 38, 31, 33, 36, 45, 44, 39, 1, 32]
schema = {"advertisement": "advertisement", "car": "car", "city": "city", "fed_count": "fed_count",
              "region": "region",
              "model": "model", "modification": "modification"}

