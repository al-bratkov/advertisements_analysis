from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import urlparse, parse_qs
from html import escape
import numpy as np
import pandas as pd

from compute_module import ServerDataFrame


brands = ['Не имеет значения', 'a', 'b']
brands = np.append("Не имеет значения", ['ВАЗ (LADA)', 'ЗАЗ', 'ГАЗ', 'УАЗ', 'ТагАЗ', 'РАФ', 'Москвич', 'ИЖ', 'Vortex', 'ВИС', 'Derways', 'ЗИЛ', 'Doninvest'])
models = {'does not matter': ["does not matter"], 'a': ['does not matter', "model_1", "model_11"], 'b': ['does not matter', "model2", "model22"]}
body_types = {'does not matter': ['-'], "model_1": ['does not matter', 'hach', 'sed'],
              "model_11": ['does not matter', 'mini', 'pick'], "model2": ['does not matter', 'hach', 'sed'],
              "model22": ['does not matter', 'mini', 'pick']}

colors = ["blue", "green", "red"]

result = []
test_df = pd.DataFrame

models = {'Не имеет значения': ['Не имеет значения'],
         'ВАЗ (LADA)': ["does not matter", 'Kalina', 'Granta', '4x4 (Нива)', '1111 Ока', 'Vesta', '2112', '2115 Samara',
         'Priora', 'Vesta Cross', 'Largus Cross', '2114 Samara', '2109', '2107', '2110', '21099', 'XRAY', 'Largus',
         '2113 Samara', 'Granta Cross', '2108', '2121 (4x4) Urban', 'Kalina Cross', '2106', '2121 (4x4) Bronto',
         '2111', '2104', '2105', '2101', 'Niva Legend Bronto', 'Niva Travel', 'Niva Off-road', 'Niva Legend',
         '2120 Надежда', 'Niva', '2102', '2103', '2329', 'XRAY Cross', '2131 (4x4) Urban', '2131 (4x4) Рысь',
         '2121 (4x4) Фора', '2123'], 'ЗАЗ': ["doen't matter", '968 Запорожец'],
         'ГАЗ': ["doen't matter", 'Соболь 2217', 'ГАЗель 2705', 'ГАЗель Next', 'ГАЗель 3302', 'Соболь 2752',
         '3102 Волга', '24 Волга', 'ГАЗель 2747', '31105 Волга', 'ГАЗель 33023', 'ГАЗель 3221', '3110 Волга',
         '21 Волга', 'ГАЗель NN', 'Соболь 2310', '31029 Волга', '69', 'Volga Siber', '310221 Волга', 'А', 'M1', 'М-72'],
         'УАЗ': ["doen't matter", 'Patriot', 'Hunter', '31519', '31514', '3962', 'Профи', '31512', '3159', '3909', '3303',
         'Карго', '39094', '3153', 'Pickup', '2206', '3160', '3741', '3151', '39095', 'Симбир', '469', '452 Буханка'],
         'ТагАЗ': ["doen't matter", 'Tager', 'C190', 'Vega', 'Road Partner'],
         'РАФ': ["doen't matter", '2203'],
         'Москвич': ["doen't matter", '410', '412', '407', '2141', '401', 'Князь Владимир', 'Святогор'],
         'ИЖ': ["doen't matter", '2126', '2717', '2125', 'Москвич-412', '21261', '2715'],
         'Vortex': ["doen't matter", 'Tingo', 'Estina', 'Corda'], 'ВИС': ["doen't matter", '2347', '2349', '2346'],
         'Derways': ["doen't matter", 'Plutus', 'Land Crown', 'Shuttle'],
         'ЗИЛ': ["doen't matter", '4104'],
         'Doninvest': ["doen't matter", 'Assol']}

bodies = {'Не имеет значения': ['Не имеет значения'], 'ВАЗ (LADA)|Kalina': ["doesn't matter", 'Универсал', 'Хетчбэк', 'Седан'], 'ЗАЗ|968 Запорожец': ["doesn't matter", 'Седан'], 'ГАЗ|Соболь 2217': ["doesn't matter", 'Микроавтобус', 'Минивэн'], 'ВАЗ (LADA)|Granta': ["doesn't matter", 'Седан', 'Лифтбек', 'Хетчбэк', 'Универсал'], 'ВАЗ (LADA)|4x4 (Нива)': ["doesn't matter", 'Внедорожник'], 'ВАЗ (LADA)|1111 Ока': ["doesn't matter", 'Хетчбэк'], 'ГАЗ|ГАЗель 2705': ["doesn't matter", 'Фургон'], 'ГАЗ|ГАЗель Next': ["doesn't matter", 'Фургон', 'Микроавтобус', 'Пикап'], 'ВАЗ (LADA)|Vesta': ["doesn't matter", 'Седан', 'Универсал'], 'ВАЗ (LADA)|2112': ["doesn't matter", 'Хетчбэк'], 'ВАЗ (LADA)|2115 Samara': ["doesn't matter", 'Седан'], 'ВАЗ (LADA)|Priora': ["doesn't matter", 'Седан', 'Хетчбэк', 'Универсал'], 'УАЗ|Patriot': ["doesn't matter", 'Внедорожник'], 'ВАЗ (LADA)|Vesta Cross': ["doesn't matter", 'Универсал', 'Седан'], 'ВАЗ (LADA)|Largus Cross': ["doesn't matter", 'Универсал'], 'ВАЗ (LADA)|2114 Samara': ["doesn't matter", 'Хетчбэк'], 'ВАЗ (LADA)|2109': ["doesn't matter", 'Хетчбэк', 'Внедорожник'], 'ВАЗ (LADA)|2107': ["doesn't matter", 'Седан'], 'ТагАЗ|Tager': ["doesn't matter", 'Внедорожник'], 'ГАЗ|ГАЗель 3302': ["doesn't matter", 'Фургон', 'Пикап'], 'ВАЗ (LADA)|2110': ["doesn't matter", 'Седан'], 'ВАЗ (LADA)|21099': ["doesn't matter", 'Седан'], 'ВАЗ (LADA)|XRAY': ["doesn't matter", 'Хетчбэк'], 'ГАЗ|Соболь 2752': ["doesn't matter", 'Фургон', 'Минивэн', 'Микроавтобус'], 'ВАЗ (LADA)|Largus': ["doesn't matter", 'Фургон', 'Универсал'], 'ВАЗ (LADA)|2113 Samara': ["doesn't matter", 'Хетчбэк'], 'ГАЗ|3102 Волга': ["doesn't matter", 'Седан'], 'РАФ|2203': ["doesn't matter", 'Микроавтобус'], 'ВАЗ (LADA)|Granta Cross': ["doesn't matter", 'Универсал'], 'ВАЗ (LADA)|2108': ["doesn't matter", 'Хетчбэк'], 'Москвич|410': ["doesn't matter", 'Седан'], 'УАЗ|Hunter': ["doesn't matter", 'Внедорожник'], 'УАЗ|31519': ["doesn't matter", 'Внедорожник'], 'ГАЗ|24 Волга': ["doesn't matter", 'Седан', 'Универсал'], 'ИЖ|2126': ["doesn't matter", 'Хетчбэк'], 'ВАЗ (LADA)|2121 (4x4) Urban': ["doesn't matter", 'Внедорожник'], 'ВАЗ (LADA)|Kalina Cross': ["doesn't matter", 'Универсал'], 'ВАЗ (LADA)|2106': ["doesn't matter", 'Седан'], 'ГАЗ|ГАЗель 2747': ["doesn't matter", 'Фургон'], 'Vortex|Tingo': ["doesn't matter", 'Внедорожник'], 'ГАЗ|31105 Волга': ["doesn't matter", 'Седан'], 'ГАЗ|ГАЗель 33023': ["doesn't matter", 'Фургон', 'Пикап'], 'ВАЗ (LADA)|2121 (4x4) Bronto': ["doesn't matter", 'Внедорожник'], 'ВАЗ (LADA)|2111': ["doesn't matter", 'Универсал'], 'ВАЗ (LADA)|2104': ["doesn't matter", 'Универсал'], 'УАЗ|31514': ["doesn't matter", 'Внедорожник'], 'ВАЗ (LADA)|2105': ["doesn't matter", 'Седан'], 'ГАЗ|ГАЗель 3221': ["doesn't matter", 'Микроавтобус', 'Фургон'], 'ВАЗ (LADA)|2101': ["doesn't matter", 'Седан'], 'Vortex|Estina': ["doesn't matter", 'Седан'], 'Москвич|412': ["doesn't matter", 'Седан'], 'УАЗ|3962': ["doesn't matter", 'Микроавтобус'], 'ВАЗ (LADA)|Niva Legend Bronto': ["doesn't matter", 'Внедорожник'], 'ВАЗ (LADA)|Niva Travel': ["doesn't matter", 'Внедорожник'], 'ИЖ|2717': ["doesn't matter", 'Фургон', 'Пикап'], 'УАЗ|Профи': ["doesn't matter", 'Пикап', 'Фургон'], 'УАЗ|31512': ["doesn't matter", 'Внедорожник'], 'ГАЗ|3110 Волга': ["doesn't matter", 'Седан'], 'Москвич|407': ["doesn't matter", 'Седан'], 'УАЗ|3159': ["doesn't matter", 'Внедорожник'], 'ВАЗ (LADA)|Niva Off-road': ["doesn't matter", 'Внедорожник'], 'ГАЗ|21 Волга': ["doesn't matter", 'Седан'], 'ВАЗ (LADA)|Niva Legend': ["doesn't matter", 'Внедорожник'], 'ВАЗ (LADA)|2120 Надежда': ["doesn't matter", 'Минивэн'], 'УАЗ|3909': ["doesn't matter", 'Микроавтобус', 'Пикап'], 'ГАЗ|ГАЗель NN': ["doesn't matter", 'Фургон'], 'ВАЗ (LADA)|Niva': ["doesn't matter", 'Внедорожник'], 'УАЗ|3303': ["doesn't matter", 'Пикап'], 'УАЗ|Карго': ["doesn't matter", 'Пикап'], 'УАЗ|39094': ["doesn't matter", 'Пикап'], 'ГАЗ|Соболь 2310': ["doesn't matter", 'Пикап', 'Фургон'], 'ГАЗ|31029 Волга': ["doesn't matter", 'Седан'], 'ИЖ|2125': ["doesn't matter", 'Лифтбек'], 'УАЗ|3153': ["doesn't matter", 'Внедорожник'], 'ВАЗ (LADA)|2102': ["doesn't matter", 'Универсал'], 'ВАЗ (LADA)|2103': ["doesn't matter", 'Седан'], 'ГАЗ|69': ["doesn't matter", 'Внедорожник'], 'ВИС|2347': ["doesn't matter", 'Фургон'], 'ВИС|2349': ["doesn't matter", 'Фургон'], 'ВАЗ (LADA)|2329': ["doesn't matter", 'Пикап'], 'УАЗ|Pickup': ["doesn't matter", 'Пикап'], 'УАЗ|2206': ["doesn't matter", 'Микроавтобус'], 'ГАЗ|Volga Siber': ["doesn't matter", 'Седан'], 'ТагАЗ|C190': ["doesn't matter", 'Внедорожник'], 'ТагАЗ|Vega': ["doesn't matter", 'Седан'], 'ВИС|2346': ["doesn't matter", 'Фургон'], 'ВАЗ (LADA)|XRAY Cross': ["doesn't matter", 'Хетчбэк'], 'ВАЗ (LADA)|2131 (4x4) Urban': ["doesn't matter", 'Внедорожник'], 'Москвич|2141': ["doesn't matter", 'Хетчбэк'], 'ВАЗ (LADA)|2131 (4x4) Рысь': ["doesn't matter", 'Внедорожник'], 'УАЗ|3160': ["doesn't matter", 'Внедорожник'], 'ГАЗ|310221 Волга': ["doesn't matter", 'Универсал'], 'Derways|Plutus': ["doesn't matter", 'Пикап'], 'УАЗ|3741': ["doesn't matter", 'Фургон'], 'ВАЗ (LADA)|2121 (4x4) Фора': ["doesn't matter", 'Внедорожник'], 'ИЖ|Москвич-412': ["doesn't matter", 'Седан'], 'Vortex|Corda': ["doesn't matter", 'Лифтбек'], 'ТагАЗ|Road Partner': ["doesn't matter", 'Внедорожник'], 'УАЗ|3151': ["doesn't matter", 'Внедорожник'], 'Derways|Land Crown': ["doesn't matter", 'Внедорожник'], 'ВАЗ (LADA)|2123': ["doesn't matter", 'Внедорожник'], 'ИЖ|21261': ["doesn't matter", 'Универсал'], 'ЗИЛ|4104': ["doesn't matter", 'Седан'], 'Москвич|401': ["doesn't matter", 'Седан'], 'УАЗ|39095': ["doesn't matter", 'Пикап'], 'УАЗ|Симбир': ["doesn't matter", 'Внедорожник'], 'Derways|Shuttle': ["doesn't matter", 'Внедорожник'], 'Москвич|Князь Владимир': ["doesn't matter", 'Седан'], 'ГАЗ|А': ["doesn't matter", 'Кабриолет'], 'УАЗ|469': ["doesn't matter", 'Внедорожник'], 'ГАЗ|M1': ["doesn't matter", 'Седан'], 'ИЖ|2715': ["doesn't matter", 'Фургон'], 'УАЗ|452 Буханка': ["doesn't matter", 'Фургон'], 'Москвич|Святогор': ["doesn't matter", 'Хетчбэк'], 'Doninvest|Assol': ["doesn't matter", 'Хетчбэк'], 'ГАЗ|М-72': ["doesn't matter", 'Седан']}
bodies = {'Не имеет значения': ['Не имеет значения'], 'Kalina': ["doesn't matter", 'Универсал', 'Хетчбэк', 'Седан'], '968 Запорожец': ["doesn't matter", 'Седан'], 'Соболь 2217': ["doesn't matter", 'Микроавтобус', 'Минивэн'], 'Granta': ["doesn't matter", 'Седан', 'Лифтбек', 'Хетчбэк', 'Универсал'], '4x4 (Нива)': ["doesn't matter", 'Внедорожник'], '1111 Ока': ["doesn't matter", 'Хетчбэк'], 'ГАЗель 2705': ["doesn't matter", 'Фургон'], 'ГАЗель Next': ["doesn't matter", 'Фургон', 'Микроавтобус', 'Пикап'], 'Vesta': ["doesn't matter", 'Седан', 'Универсал'], '2112': ["doesn't matter", 'Хетчбэк'], '2115 Samara': ["doesn't matter", 'Седан'], 'Priora': ["doesn't matter", 'Седан', 'Хетчбэк', 'Универсал'], 'Patriot': ["doesn't matter", 'Внедорожник'], 'Vesta Cross': ["doesn't matter", 'Универсал', 'Седан'], 'Largus Cross': ["doesn't matter", 'Универсал'], '2114 Samara': ["doesn't matter", 'Хетчбэк'], '2109': ["doesn't matter", 'Хетчбэк', 'Внедорожник'], '2107': ["doesn't matter", 'Седан'], 'Tager': ["doesn't matter", 'Внедорожник'], 'ГАЗель 3302': ["doesn't matter", 'Фургон', 'Пикап'], '2110': ["doesn't matter", 'Седан'], '21099': ["doesn't matter", 'Седан'], 'XRAY': ["doesn't matter", 'Хетчбэк'], 'Соболь 2752': ["doesn't matter", 'Фургон', 'Минивэн', 'Микроавтобус'], 'Largus': ["doesn't matter", 'Фургон', 'Универсал'], '2113 Samara': ["doesn't matter", 'Хетчбэк'], '3102 Волга': ["doesn't matter", 'Седан'], '2203': ["doesn't matter", 'Микроавтобус'], 'Granta Cross': ["doesn't matter", 'Универсал'], '2108': ["doesn't matter", 'Хетчбэк'], '410': ["doesn't matter", 'Седан'], 'Hunter': ["doesn't matter", 'Внедорожник'], '31519': ["doesn't matter", 'Внедорожник'], '24 Волга': ["doesn't matter", 'Седан', 'Универсал'], '2126': ["doesn't matter", 'Хетчбэк'], '2121 (4x4) Urban': ["doesn't matter", 'Внедорожник'], 'Kalina Cross': ["doesn't matter", 'Универсал'], '2106': ["doesn't matter", 'Седан'], 'ГАЗель 2747': ["doesn't matter", 'Фургон'], 'Tingo': ["doesn't matter", 'Внедорожник'], '31105 Волга': ["doesn't matter", 'Седан'], 'ГАЗель 33023': ["doesn't matter", 'Фургон', 'Пикап'], '2121 (4x4) Bronto': ["doesn't matter", 'Внедорожник'], '2111': ["doesn't matter", 'Универсал'], '2104': ["doesn't matter", 'Универсал'], '31514': ["doesn't matter", 'Внедорожник'], '2105': ["doesn't matter", 'Седан'], 'ГАЗель 3221': ["doesn't matter", 'Микроавтобус', 'Фургон'], '2101': ["doesn't matter", 'Седан'], 'Estina': ["doesn't matter", 'Седан'], '412': ["doesn't matter", 'Седан'], '3962': ["doesn't matter", 'Микроавтобус'], 'Niva Legend Bronto': ["doesn't matter", 'Внедорожник'], 'Niva Travel': ["doesn't matter", 'Внедорожник'], '2717': ["doesn't matter", 'Фургон', 'Пикап'], 'Профи': ["doesn't matter", 'Пикап', 'Фургон'], '31512': ["doesn't matter", 'Внедорожник'], '3110 Волга': ["doesn't matter", 'Седан'], '407': ["doesn't matter", 'Седан'], '3159': ["doesn't matter", 'Внедорожник'], 'Niva Off-road': ["doesn't matter", 'Внедорожник'], '21 Волга': ["doesn't matter", 'Седан'], 'Niva Legend': ["doesn't matter", 'Внедорожник'], '2120 Надежда': ["doesn't matter", 'Минивэн'], '3909': ["doesn't matter", 'Микроавтобус', 'Пикап'], 'ГАЗель NN': ["doesn't matter", 'Фургон'], 'Niva': ["doesn't matter", 'Внедорожник'], '3303': ["doesn't matter", 'Пикап'], 'Карго': ["doesn't matter", 'Пикап'], '39094': ["doesn't matter", 'Пикап'], 'Соболь 2310': ["doesn't matter", 'Пикап', 'Фургон'], '31029 Волга': ["doesn't matter", 'Седан'], '2125': ["doesn't matter", 'Лифтбек'], '3153': ["doesn't matter", 'Внедорожник'], '2102': ["doesn't matter", 'Универсал'], '2103': ["doesn't matter", 'Седан'], '69': ["doesn't matter", 'Внедорожник'], '2347': ["doesn't matter", 'Фургон'], '2349': ["doesn't matter", 'Фургон'], '2329': ["doesn't matter", 'Пикап'], 'Pickup': ["doesn't matter", 'Пикап'], '2206': ["doesn't matter", 'Микроавтобус'], 'Volga Siber': ["doesn't matter", 'Седан'], 'C190': ["doesn't matter", 'Внедорожник'], 'Vega': ["doesn't matter", 'Седан'], '2346': ["doesn't matter", 'Фургон'], 'XRAY Cross': ["doesn't matter", 'Хетчбэк'], '2131 (4x4) Urban': ["doesn't matter", 'Внедорожник'], '2141': ["doesn't matter", 'Хетчбэк'], '2131 (4x4) Рысь': ["doesn't matter", 'Внедорожник'], '3160': ["doesn't matter", 'Внедорожник'], '310221 Волга': ["doesn't matter", 'Универсал'], 'Plutus': ["doesn't matter", 'Пикап'], '3741': ["doesn't matter", 'Фургон'], '2121 (4x4) Фора': ["doesn't matter", 'Внедорожник'], 'Москвич-412': ["doesn't matter", 'Седан'], 'Corda': ["doesn't matter", 'Лифтбек'], 'Road Partner': ["doesn't matter", 'Внедорожник'], '3151': ["doesn't matter", 'Внедорожник'], 'Land Crown': ["doesn't matter", 'Внедорожник'], '2123': ["doesn't matter", 'Внедорожник'], '21261': ["doesn't matter", 'Универсал'], '4104': ["doesn't matter", 'Седан'], '401': ["doesn't matter", 'Седан'], '39095': ["doesn't matter", 'Пикап'], 'Симбир': ["doesn't matter", 'Внедорожник'], 'Shuttle': ["doesn't matter", 'Внедорожник'], 'Князь Владимир': ["doesn't matter", 'Седан'], 'А': ["doesn't matter", 'Кабриолет'], '469': ["doesn't matter", 'Внедорожник'], 'M1': ["doesn't matter", 'Седан'], '2715': ["doesn't matter", 'Фургон'], '452 Буханка': ["doesn't matter", 'Фургон'], 'Святогор': ["doesn't matter", 'Хетчбэк'], 'Assol': ["doesn't matter", 'Хетчбэк'], 'М-72': ["doesn't matter", 'Седан']}
owners = ["Не имеет значения", '1', '2', '3', '4+']
wheel_drive = ["Не имеет значения", 'Передний', 'Полный', 'Задний']
steering = ["Не имеет значения", 'Левый', 'Правый']
gearbox = ["Не имеет значения", 'Механика', 'Робот', 'Вариатор', 'Автомат']
color = ["Не имеет значения", 'Белый', 'Красный', 'Серебряный', 'Чёрный', 'Фиолетовый', 'Синий', 'Зелёный', 'Серый', 'Бежевый', 'Голубой', 'Бордовый', 'Жёлтый', 'Коричневый', 'Оранжевый', 'Пурпурный', 'Золотой', 'Розовый']


def convert_to_html_values(df):
    form = dict()
    form["brand"] = np.append("Не имеет значения", df.brand.unique()).tolist()
    form["owners"] = ["Не имеет значения"] + sorted(df.count_owners.unique().tolist())
    form["wheel_drive"] = np.append("Не имеет значения", df.wheel_drive.unique()).tolist()
    form["steering"] = np.append("Не имеет значения", df.steering_wheel.unique()).tolist()
    form["gearbox"] = np.append("Не имеет значения", df.gearbox_type.unique()).tolist()
    form["color"] = np.append("Не имеет значения", df.color.unique()).tolist()
    form["model"] = {brand: np.append("Не имеет значения", df[df.brand==brand].model.unique()).tolist() for brand in df.brand.unique()}
    df["brand_model"] = df.brand + "|" + df.model
    form["body_type"] = {model: np.append("Не имеет значения", df[df.model == model].body_type.unique()).tolist() for model in df.model.unique()}
    return form


class PetServer(BaseHTTPRequestHandler):

    @classmethod
    def add_df(clf, server_df):
        clf.server_df = server_df

    def do_GET(self):
        # Отправляем заголовки ответа
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()

        form = self.server_df.extract_values_to_html()
        fill_form = lambda seq: {"".join([f"<option value='{item}'>{item}</option>" for item in seq])}
        with open("Front/main.html", encoding="utf-8") as page:
            # html = page.read().format(fill_form(brands), ['does not matter'], fill_form(owners), ['does not matter'], fill_form(wheel_drive), fill_form(steering), fill_form(gearbox), fill_form(color), models, bodies)
            html = page.read().format(fill_form(form["brand"]), ['does not matter'], fill_form(form["owners"]), ['does not matter'], fill_form(form["wheel_drive"]), fill_form(form["steering"]), fill_form(form["gearbox"]), fill_form(form["color"]), form["model"], form["body_type"])

        self.wfile.write(html.encode('utf-8'))

    def do_POST(self):
        # Считываем данные из тела запроса
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length).decode('utf-8')
        chosen_values = {key: value[0] for key, value in parse_qs(post_data).items()}
        print(chosen_values)
        observe_results = self.server_df.make_the_output(chosen_values)
        if observe_results is False:
            result_text = "Извините, по указанным данным характеристикам недостаточно автомобилей, чтобы сделать выводы"
        else:
            rows = "".join([f"<li>{reg}. Средняя цена: {round(observe_results.loc[reg, 'mean'])} рублей</li>" for reg in observe_results.index])
            result_text = f"""<ol>
                                {rows}
                             </ol>"""

        # Отправляем заголовки ответа
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()

        # Отправляем html страницу с сообщением об успешной отправке данных
        with open("Front/result.html", encoding="utf-8") as page:
            html_res = page.read().format(result_text)
        self.wfile.write(html_res.encode('utf-8'))


if __name__ == '__main__':
    server_address = ('', 8000)
    my_server = PetServer
    # my_server.add_df()
    httpd = HTTPServer(server_address, my_server)
    print('Server running at http://localhost:8000')
    httpd.serve_forever()

