import pandas as pd
import numpy as np
import transliterate as trsl
import re


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


def check_regions(df):
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

    # find and fix rows with shifted location: region is city, city is street
    reg_is_city = wrong_reg[wrong_reg["region"].isin(right_reg["city"].unique())]
    df.loc[reg_is_city.index, "city"] = df.loc[reg_is_city.index, "region"]
    for i in reg_is_city.index:
        correct_reg = right_reg[right_reg["city"] == reg_is_city.loc[i, "region"]]["region"].unique()
        if len(correct_reg) == 1:
            df.loc[i, "region"] = correct_reg[0]
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
            df.loc[i, "city"] = correct_cities[i_city[0]]
            correct_reg = right_reg[right_reg["city"] == df.loc[i, "city"]]["region"].unique()
            if len(correct_reg) == 1:
                df.loc[i, "region"] = correct_reg[0]
        else:
            slice = pd.merge(df.loc[i-3:i-1, "region"], df.loc[i+1:i+3, "region"]).iloc[:, 0]
            if len(slice.unique()) == 1:
                df.loc[i, "region"] = slice.unique()[0]
                df.loc[i, "city"] = wrong_reg.loc[i, "new"].capitalize()


def check_regions_manual(df):
    reg_names = regions.values()
    wrong_reg = df[~df["region"].isin(reg_names)]
    right_reg = df[df["region"].isin(reg_names)]
    wrong_reg.loc[:, "new"] = wrong_reg["link"].str.split("/").str[3].map(lambda x: trsl.translit(x, "ru"))
    for i in wrong_reg.index:
        city = input(
            f"Enter the right city. Enter 0 to drop the row. The city name from url is: \n{wrong_reg.loc[i, 'new'].capitalize()}")
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
                    df.loc[i, "region"] = regions[int(region)]
            else:
                region = input(f"Enter the code of the right region")
                df.loc[i, "region"] = regions[region]


def clean_na(df):
    df.drop(df[df.isna().all(1)].index, inplace=True)  # delete rows with all NaN
    print("Removed empty rows")

    # feel NaN values if all the other modifications of model have only one value
    for col in ["num_cylinders", "wheel_drive"]:
        rows_na_models = df[df[col].isna()][["brand", "model"]].drop_duplicates()
        for i in rows_na_models.index:
            vals = df[(df["brand"] == rows_na_models.loc[i, "brand"]) & (df["model"] == rows_na_models.loc[i, "model"])][col]
            if len(vals.unique()) == 2:
                df.loc[vals[vals.isna()].index, col] = vals.unique()[~pd.isnull(vals.unique())][0]

