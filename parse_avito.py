import requests
from bs4 import BeautifulSoup
import lxml
from fake_useragent import UserAgent
import pandas as pd
from datetime import date, timedelta
import time


ua = UserAgent()


cookies = {"u": "2xupmssp.uchaj3.lvic740yhn00"," buyer_location_id": "655190", "uxs_uid": "9bf519e0-dee2-11ed-bd51-83bb4e1f5fbd", "_gcl_au": "1.1.1412193638.1681930038", "_ga_M29JC28873": "GS1.1.1683739604.15.1.1683739620.44.0.0", "_ga": "GA1.1.1482601418.1681930039", "_ym_uid": "1681930039599787610", "_ym_d": "1681930039", "tmr_lvid": "c160115b28f651b3a3988788bbf988b9", "tmr_lvidTS": "1681930040196", "adrcid": "ADMkmQ5NzlRZlffzvT3mEig", "_buzz_fpc": "JTdCJTIycGF0aCUyMiUzQSUyMiUyRiUyMiUyQyUyMmRvbWFpbiUyMiUzQSUyMi53d3cuYXZpdG8ucnUlMjIlMkMlMjJleHBpcmVzJTIyJTNBJTIyRnJpJTJDJTIwMTAlMjBNYXklMjAyMDI0JTIwMTclM0EyNyUzQTAxJTIwR01UJTIyJTJDJTIyU2FtZVNpdGUlMjIlM0ElMjJMYXglMjIlMkMlMjJ2YWx1ZSUyMiUzQSUyMiU3QiU1QyUyMnVmcCU1QyUyMiUzQSU1QyUyMjg1ZTg5MDY4NDNkNTcxNGY2NGVhODkwMjI1OTM2YzA3JTVDJTIyJTJDJTVDJTIyYnJvd3NlclZlcnNpb24lNUMlMjIlM0ElNUMlMjIxMTMuMCU1QyUyMiU3RCUyMiU3RA==", "cto_bundle": "wCgAkl9oZ0olMkJ1UmtBb0o4c0hLQ2pzbFYweDhlbWlvMFF6OG9tV0s0VGhnWW9sM2xDZkhVMHBJQ3olMkZKTmNCRkFVSW5VM0pjZmJ1ZnBZVjZOOGRyZ0l3SlM0MXVZVXJMd0ZDaUFnSzRIRUY0U0hvWE15bnU1dyUyRlVGcWVsT2k0WHR2TWx0bA", "_ga_WW6Q1STJ8M": "GS1.1.1682430620.3.1.1682431626.0.0.0", "_ga_ZJDLBTV49B": "GS1.1.1682430619.3.1.1682431626.0.0.0", "sx":"H4sIAAAAAAAC%2F6quBQQAAP%2F%2FQ7%2BmowIAAAA%3D", "v": "1683739621", "dfp_group": "61", "abp":"0", "gMltIuegZN2COuSe": "EOFGWsm50bhh17prLqaIgdir1V0kgrvN", "_ym_isad": "2", "tmr_detect": "0%7C1683739624581", "f": "5.0c4f4b6d233fb90636b4dd61b04726f147e1eada7172e06c47e1eada7172e06c47e1eada7172e06c47e1eada7172e06cb59320d6eb6303c1b59320d6eb6303c1b59320d6eb6303c147e1eada7172e06c8a38e2c5b3e08b898a38e2c5b3e08b890df103df0c26013a7b0d53c7afc06d0b2ebf3cb6fd35a0ac7b0d53c7afc06d0b8b1472fe2f9ba6b9ad42d01242e34c7968e2978c700f15b6831064c92d93c390fa5be3b03511ce6d04dbcad294c152cb8b1472fe2f9ba6b9ba0ac8037e2b74f97b0d53c7afc06d0b0df103df0c26013a8b1472fe2f9ba6b97b0d53c7afc06d0b71e7cb57bbcb8e0f03c77801b122405c03c77801b122405c03c77801b122405c2ebf3cb6fd35a0ac20f3d16ad0b1c546b892c6c84ad16848a9b4102d42ade879dcb5a55b9498f642cb1c56d8c25813448d503fe02743959ed60adb528b72609ea59d2712057302ac65019b20d24bbadb737502fa095869dc30e13c3c12ccf123fb0fb526bb39450a46b8ae4e81acb9fa46b8ae4e81acb9fadc0d86d9e44006d8ae585b491464264e8c83e7d34f72facb2da10fb74cac1eab2da10fb74cac1eabfa9f8f522451da10030cba0f65b590855802b7f7e805047f", "ft":"3vhgMSzF3jVcnVgRVaAtSJS6zknC8HCXvTBnIjHnn+RZl5OHGyEl3SSmCBh2AxB3P2G72i61KP9I4fV57SHfaDoAfHcf2Ol8IDEB26GKZhJMh1xryE1us2bRRMADeLXm1wEXMrHYIB5fADiTVS0iCD33WR0kMD+3JsLh2H74dPPpscqz7qWkP7fpl92MIFkJ"}
headers = {"user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/113.0",
           "x-requested-with": "XMLHttpRequest"}



def model_page(url):
    time.sleep(3)
    response = requests.get(url, headers=headers, cookies=cookies)
    response.encoding = "utf-8"
    soup = BeautifulSoup(response.text, "lxml")  # fix
    main_table = soup.find("div", {"data-marker": "modification-characteristics"}).find("div", {
                "class": "styles-narrowBlocks-FRFsk"}).find_all("div", {"class": "styles-block-zWT9W"})

    div_main = main_table[0].find_all("div", {"class": "desktop-1jb7eb2"})
    fuel_waste_mix = div_main[5].find_all("span")[1].text
    fuel_waste_mix = float(fuel_waste_mix[:fuel_waste_mix.find(",") + 2].replace(",", "."))
    gearbox_type = div_main[3].find_all("span")[1].text

    div_engine = main_table[3].find_all("div", {"class": "desktop-1jb7eb2"})
    en_capacity = int("".join([l for l in [span.text for span in div_engine[0].find_all("span")][1][:-1] if l.isdigit()]))
    en_type = div_engine[3].find_all("span")[1].text
    en_power = int("".join([l for l in [span.text for span in div_engine[4].find_all("span")][1] if l.isdigit()]))
    num_cylinders = int(div_engine[1].find_all("span")[1].text)

    div_rest = main_table[10].find_all("div", {"class": "desktop-1jb7eb2"})
    body_type = div_rest[0].find_all("span")[1].text
    modification = div_rest[1].find_all("span")[1].text
    num_doors = int(div_rest[5].find_all("span")[1].text)
    wheel_drive = div_main[4].find_all("span")[1].text

    out = [en_capacity, en_type, en_power, num_cylinders, fuel_waste_mix, body_type, modification, num_doors,
           gearbox_type, wheel_drive]
    return out


def car_page(url):
    time.sleep(5)
    response = requests.get(url, headers=headers, cookies=cookies)
    response.encoding = "utf-8"
    soup = BeautifulSoup(response.text, "lxml")
    vin = None
    is_owner = "собственника" in soup.find("div", {"class": "style-ts-card-badge-bar-FxDs0"}).text
    is_promo = None
    _car_path = soup.find("div", attrs={"class": "breadcrumbs-root-_GADZ"}).\
                find_all("span", {"class": "breadcrumbs-linkWrapper-jZP0j breadcrumbs-linkWrapper_AbRedesign-WcsIB"})
    region = _car_path[0].text
    brand = _car_path[4].text
    model = _car_path[5].text
    year = int(soup.find("span", attrs={"class": "title-info-title-text"}).text[-4:])
    city_start = url.find("avito.ru/") + 9
    city_end = url[city_start:].find("/")
    city = url[city_start:city_start + city_end]

    _car_table = soup.find("ul", attrs={"class": "params-paramsList-zLpAu"}).find_all("li")
    mileage = int("".join([l for l in _car_table[2].text if l.isdigit()]))
    count_owners = _car_table[5].text.split(': ')[1]
    price = int("".join([l for l in
            soup.find("div", attrs={"class": "style-price-value-mHi1T style-item-price-main-jpt3x item-price"})
            .text if l.isdigit()]))

    options = soup.find("div", attrs={"class": "style-advanced-params-container-_BQMZ"})\
              .find_all("li", attrs={"class": "style-advanced-params-group-zjm0_"})
    is_air_condition = False
    for block in options:
        if block.find("div", attrs={"class": "style-advanced-params-group-title-FsF_e"}).text == "Управление климатом":
            for device in block.find_all("li", attrs={"class": "style-advanced-params-group-list-item-YpEU6"}):  # devices in climate system
                if device.text.lower().startswith("климат-контроль") or device.text.lower().startswith("кондиционер"):
                    is_air_condition = True
                    break
        if is_air_condition:
            break

    color = _car_table[14].text[6:]
    steering_wheel = _car_table[15].text[6:]
    _ad_info = soup.find("div", attrs={"class": "style-item-footer-Ufxh_"})
    avito_id = int(_ad_info.find("span", attrs={"data-marker": "item-view/item-id"}).text.split()[1])
    ad_date_note = _ad_info.find("span", attrs={"data-marker": "item-view/item-date"}).text.split()
    ad_date_note = ad_date_note[1:]  # need to check
    print(ad_date_note)
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
        ad_date = (int(ad_date_note[0]), month, year)
    features_url = soup.find("div", attrs={"class": "params-specification-__5qD"}).find("a")["href"]
    auto = [vin, is_owner, is_promo, region, city, brand, model, year, mileage, count_owners, is_air_condition, color, price]
    time.sleep(5)
    auto.extend(model_page(features_url))
    auto.append(steering_wheel)
    auto.append(url)
    auto.append(ad_date)
    auto.append(avito_id)
    return auto


def search_page(url):
    time.sleep(3)
    response = requests.get(url, headers=headers, cookies=cookies)
    response.encoding = "utf-8"
    soup = BeautifulSoup(response.text, "lxml")
    cars = soup.find("div", attrs={"class": "index-root-KVurS"}).find_all("div", attrs={"class": "iva-item-content-rejJg"})
    cars_href = [a.find("a")["href"] for a in cars]
    new_rows = []
    for car in cars_href:
        new_rows.append(car_page(car))
    return new_rows


def through_pages(url):
    response = requests.get(url, headers=headers, cookies=cookies)
    response.encoding = "utf-8"
    soup = BeautifulSoup(response.text, "lxml")
    pagen = soup.find("div", attrs={"class": "js-pages pagination-pagination-_FSNE"})
    last_page = pagen.find("li", attrs={"class": "styles-module-listItem-_dG7y styles-module-listItem_size_s-oO9W6 styles-module-listItem_last-_ZfSe styles-module-listItem_notFirst-Z383V"}).text
    cars = search_page(url)
    for i in range(int(last_page)-1):
        next_page = pagen.find("li", attrs={"class": " styles-module-listItem-_dG7y styles-module-listItem_arrow-x_snQ styles-module-listItem_arrow_next-GnEQw"})\
        .find("a")["href"]
        cars.extend(search_page(next_page))
    return cars


def new_df(url):
    data = through_pages(url)
    columns = ["vin", "is_owner", "is_promo", "region", "city", "brand", "model", "year", "mileage", "count_owners",
               "air condition", "color", "price", "en_capacity", "en_type", "en_power", "num_cylinders",
               "fuel_waste_mix", "body_type", "modification", "num_doors", "gearbox_type", "wheel_drive",
               "steering_wheel", "link", "ad_date", "avito_id"]  # add link and date
    table_cars = pd.DataFrame(data=data, columns=columns)
    table_cars.to_csv("auto.csv", sep=";")



