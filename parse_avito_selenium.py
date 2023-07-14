import numpy as np
import pandas as pd
import selenium
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait

from datetime import date, timedelta
import time
import random


user_way = "C:\\Users\Александр\AppData\Local\Google\Chrome\\User Data\Default"
proxy = "51.159.212.239:80"
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument("user-data-dir=C:\\Users\Александр\AppData\Local\Google\Chrome\\User Data\Default")
# chrome_options.add_argument("user-data-dir=C:\\Users\Александр\AppData\Local\Google\Chrome\\User Data\Profile 1")
chrome_options.add_experimental_option("useAutomationExtension", False)
chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
# chrome_options.add_argument("--proxy-server=%s" % proxy)
chrome_options.add_argument('--headless')

url = "https://www.avito.ru/stavropolskiy_kray/avtomobili?cd=1&f=ASgBAQICA0TyCrCKAYYUyOYB~vAP6Lv3AgJA4LYNFKaKNKbaDhQC&user=1"
file = "auto.csv"


def model_page(browser, url):  # url uses for particular tests
    """
    Get information about car model
    :param browser: Selenium webdriver object
    :param url: uses for particular tests
    :return: a list with gotten features
    """
    time.sleep(1)
    scrolls = random.choice([1, 4])  #
    time.sleep(5)
    for _ in range(scrolls):  # scroll page for imitation of human behavior
        browser.execute_script("window.scrollBy(0, 100);")
    # browser.get(url)
    time.sleep(random.randint(1,4))
    cur_url = browser.current_url
    main_table = browser.find_elements(By.CLASS_NAME, "styles-block-zWT9W")  # finds all
    main_titles = [el.text.split("\n")[0] for el in main_table]
    div_main = main_table[main_titles.index("Основные характеристики")].find_elements(By.CLASS_NAME, "desktop-1jb7eb2")
    divmain_titles = [el.text.split("\n")[0] for el in div_main]
    try:
        fuel_waste_mix = div_main[divmain_titles.index("Расход топлива смешанный")].find_element(By.CSS_SELECTOR, "span:nth-child(2)").text
        fuel_waste_mix = float(fuel_waste_mix[:fuel_waste_mix.find(",") + 2].replace(",", "."))
    except ValueError:
        fuel_waste_mix = np.NaN
    except NameError:
        fuel_waste_mix = np.NaN
    gearbox_type = div_main[3].find_element(By.CSS_SELECTOR, "span:nth-child(2)").text

    div_engine = main_table[main_titles.index("Двигатель")].find_elements(By.CLASS_NAME, "desktop-1jb7eb2")
    engine_titles = [el.text.split("\n")[0] for el in div_engine]
    en_capacity = int("".join(
        [l for l in [span for span in div_engine[engine_titles.index("Рабочий объём")].find_element(By.CSS_SELECTOR, "span:nth-child(2)").text][:-1] if
         l.isdigit()]))
    en_type = div_engine[engine_titles.index("Тип двигателя")].find_element(By.CSS_SELECTOR, "span:nth-child(2)").text
    en_power = int("".join(
        [l for l in [span for span in div_engine[engine_titles.index("Мощность, л.с.")].find_element(By.CSS_SELECTOR, "span:nth-child(2)").text] if
         l.isdigit()]))
    try:
        num_cylinders = int(div_engine[engine_titles.index("Количество цилиндров")].find_element(By.CSS_SELECTOR, "span:nth-child(2)").text)
    except ValueError:
        num_cylinders = np.NaN
    except NameError:
        num_cylinders = np.NaN

    div_rest = main_table[-1].find_elements(By.CLASS_NAME, "desktop-1jb7eb2")
    rest_titles = [el.text.split("\n")[0] for el in div_rest]
    body_type = div_rest[rest_titles.index("Кузов")].find_element(By.CSS_SELECTOR, "span:nth-child(2)").text
    modification = div_rest[rest_titles.index("Модификация")].find_element(By.CSS_SELECTOR, "span:nth-child(2)").text
    num_doors = int(div_rest[rest_titles.index("Количество дверей")].find_element(By.CSS_SELECTOR, "span:nth-child(2)").text)
    try:
        wheel_drive = div_main[divmain_titles.index("Привод")].find_element(By.CSS_SELECTOR, "span:nth-child(2)").text
    except ValueError:
        wheel_drive = np.NaN
    except NameError:
        wheel_drive = np.NaN

    out = [en_capacity, en_type, en_power, num_cylinders, fuel_waste_mix, body_type, modification, num_doors,
           gearbox_type, wheel_drive]
    return out


def car_page(browser, url, model_uids):
    """
    Get information about a car in an advertisement
    :param browser: Selenium webdriver object
    :param url: uses for particular tests, also one item in output
    :param model_uids: dictionary with model uids (part of url) as keys, values are model features
    :return: list with full information about car
    """
    way = random.choice([0, 1])
    scroll_len = 0
    if way == 0:
        time.sleep(random.randint(1, 4))
    else:
        time.sleep(1)
        scroll_len = random.randint(10, height_window)
        time.sleep(1)
        browser.execute_script(f"window.scrollBy(0, {scroll_len});")
    # browser.get(url)
    vin = np.NaN
    try:
        is_owner = "собственника" in browser.find_element(By.CLASS_NAME, "style-ts-card-badge-bar-FxDs0").text
    except selenium.common.exceptions.NoSuchElementException:
        is_owner = False
    is_promo = np.NaN
    _car_path = browser.find_elements(By.CLASS_NAME, "breadcrumbs-linkWrapper-jZP0j")
    brand = _car_path[4].text
    model = _car_path[5].text
    # year = int(browser.find_element(By.CSS_SELECTOR, ".title-info-title-text").text[-4:])
    _location = browser.find_element(By.CSS_SELECTOR, ".style-item-address-KooqC .style-item-address__string-wt61A")\
        .text.split(", ")
    try:
        region = _location[0]
    except IndexError:
        region = np.NaN
    try:
        city = _location[1]
    except IndexError:
        city = np.NaN
    _car_table = browser.find_element(By.CLASS_NAME, "params-paramsList-zLpAu").find_elements(By.TAG_NAME, "li")
    _car_dict = {feature.text.split(": ")[0]: feature.text.split(": ")[1] for feature in _car_table}
    if "Пробег" in _car_dict.keys():
        mileage = int("".join([l for l in _car_dict["Пробег"] if l.isdigit()]))
    else:
        mileage = np.NaN
    count_owners = _car_dict.get("Владельцев по ПТС", np.NaN)
    year = _car_dict.get("Год выпуска", np.NaN)
    price = int("".join([l for l in browser.find_element(By.CLASS_NAME, "style-item-price-PuQ0I")\
           .text if l.isdigit()]))
    browser.execute_script(f"window.scrollBy(0, {height_window*2+random.randint(1, 100)});")
    try:
        browser.find_element(By.CLASS_NAME, "style-advanced-params-show-more-gvtRP").click()
        time.sleep(2)
        scroll_len = 0
    except selenium.common.exceptions.NoSuchElementException:
        pass
    browser.execute_script("window.scrollBy(0, -5000);")
    options = browser.find_elements(By.CSS_SELECTOR, ".style-advanced-params-container-_BQMZ>ul>li")
    is_air_condition = False
    for block in options:
        if block.find_element(By.CLASS_NAME, "style-advanced-params-group-title-FsF_e").text == "Управление климатом":  # need to check
            for device in block.find_elements(By.CLASS_NAME, "style-advanced-params-group-list-item-YpEU6"):  # devices in climate system
                if device.text.lower().startswith("климат-контроль") or device.text.lower().startswith("кондиционер"):
                    is_air_condition = True
                    break
        if is_air_condition:
            break
    color = _car_dict.get("Цвет", np.NaN)
    steering_wheel = _car_dict.get("Руль", np.NaN)
    _ad_info = browser.find_elements(By.CSS_SELECTOR, ".style-item-footer-Ufxh_ p>span")
    avito_id = int(_ad_info[0].text.split()[1])
    ad_date_note = _ad_info[1].text.split()
    ad_date_note = ad_date_note[1:]  # need to check
    if ad_date_note[0] == "сегодня":
        ad_date = date.today()
    elif ad_date_note[0] == "вчера":
        ad_date = date.today() - timedelta(days=1)
    else:
        months = {"января": 1, "февраля": 2, "марта": 3, "апреля": 4, "мая": 5, "июня": 6, "июля": 7, "августа": 8,
                  "сентября": 9, "октября": 10, "ноября": 11, "декабря": 12}
        if ad_date_note[2] == "в":
            year = int(date.today().year)
        else:
            year = int(ad_date_note[2])
        month = months[ad_date_note[1]]
        ad_date = date(year, month, int(ad_date_note[0]))

    _features = browser.find_element(By.CSS_SELECTOR, ".params-specification-__5qD>a")
    features_url = _features.get_attribute("href")
    features_uid = features_url[features_url.find("uid=")+4:]
    if features_uid in model_uids.keys():
        modif = model_uids[features_uid]
    else:
        page_tab = browser.current_window_handle
        browser.execute_script(f"window.scrollBy(0, {height_window-scroll_len});")
        _features.click()
        browser.switch_to.window(browser.window_handles[2])
        time.sleep(3)
        modif = model_page(browser, features_url)
        model_uids[features_uid] = modif
        browser.close()
        browser.switch_to.window(page_tab)

    auto = [vin, is_owner, is_promo, region, city, brand, model, year, mileage, count_owners, is_air_condition, color,
            price]
    auto.extend(modif)
    auto.append(steering_wheel)
    auto.append(url)
    auto.append(ad_date)
    auto.append(avito_id)
    auto.append(features_uid)
    return auto


def search_page(browser, url, file, model_uids, ad_ids, num_cars=50):
    """
    Iter items in one list from all search results. Max value is 50
    :param browser: Selenium webdriver object
    :param url: uses for particular tests
    :param file: csv file for results. Add information from each advertisement one by one
    :param model_uids: dictionary with model uids (part of url) as keys, values are model features
    :param ad_ids: list of advertisement ids
    :return: list of lists with information about cars on page
    """
    # browser.get(url)
    cars = browser.find_elements(By.CSS_SELECTOR, ".iva-item-title-py3i_>a")[:num_cars]
    cars_href = [a.get_attribute("href") for a in cars]
    new_rows = []
    main_tab = browser.current_window_handle
    height_car = browser.find_element(By.CLASS_NAME, "index-content-_KxNP").size["height"] / len(cars) * 1.1
    for i, car in enumerate(cars):
        if cars_href[i].split("_")[-1] not in ad_ids:
            if random.random() > 0.90:
                time.sleep(60)
            cars[i].click()
            browser.switch_to.window(browser.window_handles[1])
            time.sleep(random.choice([4, 10]))
            row = car_page(browser, cars_href[i], model_uids)
            new_rows.append(row)
            row_df = pd.DataFrame([row, ])
            row_df.to_csv(file, mode="a", encoding="utf-8", header=False, index=False, sep=";")
            time.sleep(random.choice([2, 10]))
            browser.close()
            browser.switch_to.window(main_tab)
            time.sleep(random.choice([5, 15]))
            browser.execute_script(f"window.scrollBy(0, {height_car});")
            print(i + 1)
    return new_rows


def through_pages(browser, url, file, only_region=False, database=None):
    """
    Pagination
    :param browser: Selenium webdriver object
    :param url: url for webriver.get()
    :param file: csv file for results. Add information from each advertisement one by one
    :param database: FOR FUTURE
    :return: list of lists with information about cars from search results
    """
    browser.get(url)
    pagen = browser.find_element(By.CLASS_NAME, "pagination-pagination-_FSNE")
    df = pd.read_csv(file, encoding="utf-8", sep=";")
    ad_ids = df["avito_id"].astype("str").str[:-2].values
    model_uids = {df.loc[row, "model_uid"]: df.loc[row, ["en_capacity", "en_type", "en_power", "num_cylinders",
                                                           "fuel_waste_mix", "body_type", "modification", "num_doors",
                                                           "gearbox_type", "wheel_drive"]] for row in range(df.shape[0])}

    if only_region:
        num_cars = int(browser.find_element(By.CLASS_NAME, "page-title-count-wQ7pG").text)
        last_page = num_cars // 50
        if last_page == 0:
            cars = search_page(browser, url, file, model_uids, ad_ids, num_cars=num_cars)
        else:
            cars = search_page(browser, url, file, model_uids, ad_ids)
            print(cars)
            for i in range(int(last_page) - 2):
                pagen = browser.find_element(By.CLASS_NAME, "pagination-pagination-_FSNE")
                next_page = pagen.find_element(By.CSS_SELECTOR, "nav>ul>li:nth-last-child(1)")
                next_page.click()
                time.sleep(5)
                cur_url = browser.current_url
                cars.extend(search_page(browser, cur_url, file, model_uids, ad_ids))
            pagen = browser.find_element(By.CLASS_NAME, "pagination-pagination-_FSNE")
            next_page = pagen.find_element(By.CSS_SELECTOR, "nav>ul>li:nth-last-child(1)")
            next_page.click()
            time.sleep(5)
            cur_url = browser.current_url
            cars.extend(search_page(browser, cur_url, file, model_uids, ad_ids, num_cars=num_cars % 50))
    else:
        last_page = pagen.find_element(By.CSS_SELECTOR, "nav>ul>li:nth-last-child(2)").text
        cars = search_page(browser, url, file, model_uids, ad_ids)
        print(cars)
        for i in range(int(last_page)-1):
            pagen = browser.find_element(By.CLASS_NAME, "pagination-pagination-_FSNE")
            next_page = pagen.find_element(By.CSS_SELECTOR, "nav>ul>li:nth-last-child(1)")
            next_page.click()
            time.sleep(5)
            cur_url = browser.current_url
            cars.extend(search_page(browser, cur_url, file, model_uids, ad_ids))
    return cars


def new_df(data):
    columns = ["vin", "is_owner", "is_promo", "region", "city", "brand", "model", "year", "mileage", "count_owners",
               "air_condition", "color", "price", "en_capacity", "en_type", "en_power", "num_cylinders",
               "fuel_waste_mix", "body_type", "modification", "num_doors", "gearbox_type", "wheel_drive",
               "steering_wheel", "link", "ad_date", "avito_id", "model_uid"]  # add link and date
    table_cars = pd.DataFrame(data=data, columns=columns)
    table_cars.to_csv("result.csv", sep=";", index=False, encoding="utf-8")


with webdriver.Chrome(options=chrome_options) as browser:
    url73 = "https://www.avito.ru/ulyanovskaya_oblast/avtomobili/s_probegom-ASgBAgICAUSGFMjmAQ?cd=1&f=ASgBAQICA0TyCrCKAYYUyOYB~vAP6Lv3AgJAptoOFAKE0RIUssnaEQ&localPriority=1&user=1"
    few_urls = {13: 'https://www.avito.ru/mordoviya/avtomobili/s_probegom-ASgBAgICAUSGFMjmAQ?cd=1&f=ASgBAQICA0TyCrCKAYYUyOYB~vAP6Lv3AgJAptoOFAKE0RIUssnaEQ&user=1',
                73: 'https://www.avito.ru/ulyanovskaya_oblast/avtomobili/s_probegom-ASgBAgICAUSGFMjmAQ?cd=1&f=ASgBAQICA0TyCrCKAYYUyOYB~vAP6Lv3AgJAptoOFAKE0RIUssnaEQ&localPriority=1&user=1'}
    browser.maximize_window()
    height_window = browser.execute_script("return window.innerHeight")
    data = through_pages(browser, url73, file, only_region=False)

    new_df(data)
    print("Success!")
