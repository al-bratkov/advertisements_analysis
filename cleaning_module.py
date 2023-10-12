import pandas as pd
import numpy as np
import requests
import json
import transliterate as trsl
import re
from sklearn.linear_model import LinearRegression, SGDClassifier

from db_module import cities_from_db


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


def translate(text, IAM_TOKEN, folder_id):
    """
    Translates text from url with Yandex translate API.
    More information how to use it: https://cloud.yandex.ru/docs/translate/api-ref/authentication
    :param text: string for translating
    :param IAM_TOKEN: Token getting on Yandex Cloud. Need to enter 'yc iam create-token' in cmd to get IAM token
    :param folder_id: id of a folder on Yandex Cloud
    :return: Translated text
    """
    target_language = 'ru'
    body = {"targetLanguageCode": target_language,
            "texts": text,
            "folderId": folder_id,}
    headers = {"Content-Type": "application/json",
               "Authorization": "Bearer {0}".format(IAM_TOKEN)}
    response = requests.post('https://translate.api.cloud.yandex.net/translate/v2/translate',
                             json=body,
                             headers=headers)
    res = json.loads(response.text)
    return res["translations"][0]["text"].title()


class DfMess:
    pass


def check_regions(df, db=None, login=None, password=None, IAM_TOKEN= None, folder_id=None):
    """
    Fix errors in values about a city and a region. Right values are important for a future analysis
    :param df: a dataframe with all information
    :return: no return. Change the input dataframe
    """
    reg_names = regions.values()
    wrong_reg = df[~df["region"].isin(reg_names)]

    # find and fix rows with wrong named regions: in "region - count" format
    wrong_reg["new"] = wrong_reg["region"].str.split(" — ").str[0]
    for reg in regions.values():
        for name in wrong_reg.new.unique():
            if reg.startswith(name):
                i_short = wrong_reg[wrong_reg["new"] == name].index
                df.loc[i_short, "region"] = reg
    wrong_reg = df[~df["region"].isin(reg_names)]
    right_reg = df[df["region"].isin(reg_names)]
    correct_cities = right_reg["city"].unique()
    if db is not None:
        inf_db_city = cities_from_db(db, login, password)
        correct_cities_db = inf_db_city["city"].values
        correct_cities = np.unique(np.concatenate((correct_cities, correct_cities_db)))

    # find and fix rows with shifted location: region is city, city is street
    reg_is_city = wrong_reg[wrong_reg["region"].isin(correct_cities)]
    df.loc[reg_is_city.index, "city"] = df.loc[reg_is_city.index, "region"]
    for i in reg_is_city.index:
        correct_reg = right_reg[right_reg["city"] == reg_is_city.loc[i, "region"]]["region"].unique()
        if len(correct_reg) == 1:
            df.loc[i, "region"] = correct_reg[0]
        elif len(correct_reg) == 0 and db is not None:
            correct_reg = inf_db_city[inf_db_city["city"] == reg_is_city.loc[i, "region"]]["region_code"].values
            if len(correct_reg) == 1:
                df.loc[i, "region"] = regions[str(correct_reg[0])]
    wrong_reg = df[~df["region"].isin(reg_names)]
    right_reg = df[df["region"].isin(reg_names)]

    # find and fix rows with a correct city and a wrong region
    for i in wrong_reg.index:
        i_city = np.where(correct_cities.astype(str) == wrong_reg.loc[i, "city"])[0]
        if len(i_city) == 1:
            df.loc[i, "city"] = correct_cities[i_city[0]]
            correct_reg = right_reg[right_reg["city"] == df.loc[i, "city"]]["region"].unique()
            if len(correct_reg) == 1:
                df.loc[i, "region"] = correct_reg[0]
            elif len(correct_reg) == 0 and db is not None:
                correct_reg = inf_db_city[inf_db_city["city"] == wrong_reg.loc[i, "city"]]["region_code"].values
                if len(correct_reg) == 1:
                    df.loc[i, "region"] = regions[str(correct_reg[0])]
    wrong_reg = df[~df["region"].isin(reg_names)]
    right_reg = df[df["region"].isin(reg_names)]

    # find and fix all the other rows using city in url
    wrong_reg.loc[:, "new"] = wrong_reg["link"].str.split("/").str[3].map(lambda x: trsl.translit(x, "ru"))
    wrong_reg.loc[:, "new"] = wrong_reg.new.map(lambda word: word[:-1] + "й" if word[-2:] == "ыы" else word)
    wrong_reg.loc[:, "new"] = wrong_reg.new.map(lambda word: word[:-1] + "й" if word[-2:] == "иы" else word)
    wrong_reg.loc[:, "new"] = wrong_reg.new.map(lambda word: re.sub(r"ыа", "я", word))
    for i in wrong_reg.index:
        if wrong_reg.loc[i, "new"] == "москва":
            df.loc[i, "city"] = df.loc[i, "region"]
            df.loc[i, "region"] = "Москва"
        i_city = np.where(np.char.lower(correct_cities.astype(str)) == wrong_reg.loc[i, "new"])[0]
        if len(i_city) == 1:
            print(f"{i}: {df.loc[i, 'city']} --> {correct_cities[i_city[0]]} \#transliterated")
            df.loc[i, "city"] = correct_cities[i_city[0]]
            correct_reg = right_reg[right_reg["city"] == df.loc[i, "city"]]["region"].unique()
            if len(correct_reg) == 1:
                df.loc[i, "region"] = correct_reg[0]
            elif len(correct_reg) == 0 and db is not None:
                correct_reg = inf_db_city[inf_db_city["city"].str.lower() == wrong_reg.loc[i, "new"]]["region_code"].values
                if len(correct_reg) == 1:
                    df.loc[i, "region"] = regions[str(correct_reg[0])]
        else:
            real_city = translate("city " + wrong_reg.loc[i, "link"].split("/")[3], IAM_TOKEN, folder_id)[6:]
            if real_city != wrong_reg.loc[i, "new"]:
                print(f"{i}: {df.loc[i, 'city']} --> {real_city} \#translated")
                df.loc[i, "city"] = real_city
#            else:
#                slice = pd.merge(df.loc[i-3:i-1, "region"], df.loc[i+1:i+3, "region"]).iloc[:, 0]
#                if len(slice.unique()) == 1:
#                    df.loc[i, "region"] = slice.unique()[0]
#                    df.loc[i, "city"] = wrong_reg.lowc[i, "new"].capitalize()


def check_regions_manual(df):
    """
    Manually fill values about a city and a region haven't been fixed with the check_regions function
    :param df: a dataframe with all information
    :return: no return. Change the input dataframe
    """
    reg_names = regions.values()
    wrong_reg = df[~df["region"].isin(reg_names)]
    right_reg = df[df["region"].isin(reg_names)]
    wrong_reg.loc[:, "new"] = wrong_reg["link"].str.split("/").str[3].map(lambda x: trsl.translit(x, "ru"))
    for i in wrong_reg.index:
        city = input(
            f"Enter the right city. Enter 0 to drop the row. The city name from url is: \n{wrong_reg.loc[i, 'city'].capitalize()}")
        if city == "0":
            df.drop(labels=i, inplace=True)
        else:
            df.loc[i, "city"] = city
            correct_reg = right_reg[right_reg["city"] == df.loc[i, "city"]]["region"].unique()
            if len(correct_reg) == 1:
                region = input(
                    f"Enter the right region. Enter 1 if the region is {correct_reg[0]}. Otherwise enter code of the region")
                if region == "1":
                    df.loc[i, "region"] = correct_reg[0]
                else:
                    df.loc[i, "region"] = regions[region]
            else:
                region = input(f"Enter the code of the right region")
                df.loc[i, "region"] = regions[region]


def clean_na(df, db=None, login=None, password=None, IAM_TOKEN=None, folder_id=None):
    """
    Clean a dataframe. Delete duplicated and empty rows. Fill NaN values in some important columns
    :param df: a dataframe with all information
    :return: no return. Change the input dataframe
    """
    df.drop(df[df.isna().all(1)].index, inplace=True)  # delete rows with all NaN
    print("Empty rows are removed")
    df.drop_duplicates(inplace=True)
    df.drop_duplicates("avito_id", inplace=True)
    print("Duplicated rows are removed")

    # feel NaN values if all the other modifications of a model have only one value
    for col in ["num_cylinders", "wheel_drive"]:
        rows_na_models = df[df[col].isna()][["brand", "model"]].drop_duplicates()
        for i in rows_na_models.index:
            vals = df[(df["brand"] == rows_na_models.loc[i, "brand"]) & (df["model"] == rows_na_models.loc[i, "model"])][col]
            if len(vals.unique()) == 2:
                df.loc[vals[vals.isna()].index, col] = vals.unique()[~pd.isnull(vals.unique())][0]
    # use K nearest neighbors for all other NaN values
    classifier = SGDClassifier()
    cyl_na = df[df.num_cylinders.isna()]
    cyl_filled = df[~df.num_cylinders.isna()]
    model = classifier.fit(cyl_filled.en_capacity.values.reshape(-1, 1), y=cyl_filled.num_cylinders.values)
    cyl_na.loc[:, "num_cylinders"] = model.predict(cyl_na.en_capacity.values.reshape(-1, 1))
    for i in cyl_na.index:
        df.loc[i, "num_cylinders"] = cyl_na.loc[i, "num_cylinders"]

    # feel NaN values in the city column
    empty_city = df[df["city"].isna()]
    empty_city.loc[:, "new"] = empty_city["link"].str.split("/").str[3].map(lambda x: trsl.translit(x, "ru"))
    empty_city.loc[:, "new"] = empty_city.new.map(lambda word: word[:-1] + "й" if word[-2:] == "ыы" else word)
    empty_city.loc[:, "new"] = empty_city.new.map(lambda word: word[:-1] + "й" if word[-2:] == "иы" else word)
    empty_city.loc[:, "new"] = empty_city.new.map(lambda word: re.sub(r"ыа", "я", word))
    cities_db = cities_from_db(db, login, password)["city"].values
    for i in empty_city.index:
        if empty_city.loc[i, "new"].title() in cities_db:
            print(f"{i}: {df.loc[i, 'city']} --> {empty_city.loc[i, 'new'].title()} \#transliterated")
            df.loc[i, "city"] = empty_city.loc[i, "new"].title()
        else:
            real_city = translate(f'city "{empty_city.loc[i, "link"].split("/")[3].title()}"', IAM_TOKEN, folder_id)[6:].strip('"')
            print(f"{i}: {df.loc[i, 'city']} --> {real_city} \#translated")
            df.loc[i, "city"] = real_city


def fix_wrong(df):
    # fix wrong year. There is an error with a year. Instead of real value df get current year. The right year is in the link
    df["new"] = df["link"].str.split("/").str[-1].str.split("_")
    wrong_year_i = df[df["year"] >= 2023]
    for i in wrong_year_i.index:
        year_url = int(list(filter(lambda txt: len(txt) == 4 and txt.isdigit(), df.loc[i, "new"]))[-1])
        df.loc[i, "year"] = year_url

    # fix wrong fuel waste. Some models have wrong value 1.0. Try to fix it using mean value of other modifications of the model
    engine = df[['brand', 'model', 'en_capacity', 'en_type', 'en_power', 'num_cylinders', 'fuel_waste_mix']]
    wrong_waste = df[df.fuel_waste_mix < 2.5]
    right_waste = df[df.fuel_waste_mix > 2.5]
    for i in wrong_waste.index:
        brand = wrong_waste.loc[i, "brand"]
        model = wrong_waste.loc[i, "model"]
        df.loc[i, "fuel_waste_mix"] = round(right_waste[(right_waste.brand == brand) &
              (right_waste.model == model)].fuel_waste_mix.mean(), 2)
        print(f"{brand} {model} {wrong_waste.loc[i, 'fuel_waste_mix']} ==> {df.loc[i, 'fuel_waste_mix']}")
    # then fill NaN values using linear regression with engine capacity as a predictor
    waste_na = df[df.fuel_waste_mix.isna()]
    waste_filled = df[~df.fuel_waste_mix.isna()]
    waste_na = waste_na[waste_na.en_capacity <= waste_filled.en_capacity.max()]
    linereg = LinearRegression()
    model = linereg.fit(waste_filled.en_capacity.values.reshape(-1, 1), waste_filled.fuel_waste_mix.values)
    waste_na.loc[:, "fuel_waste_mix"] = model.predict(waste_na.en_capacity.values.reshape(-1, 1))
    for i in waste_na.index:
        df.loc[i, "fuel_waste_mix"] = round(waste_na.loc[i, "fuel_waste_mix"])

