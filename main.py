from http.server import BaseHTTPRequestHandler, HTTPServer

from db_module import get_all_db


schema = {"advertisement": "advertisement", "car": "car", "city": "city", "fed_count": "fed_count",
              "region": "region", "brand": "brand", "model": "model", "modification": "modification"}

def get_values_for_html_form(df, schema):
    form = {}
    form["brands"] = tuple(['Не имеет значения', ].extend(df[schema["brand"]].unique()))
    form["bodies"] = tuple(df[schema["body_type"]].unique())
    form["colors"] = tuple(df[schema["color"]].unique())
    form["miles"] = 1_000_000
    form["year"] = 1936
    form["owners"] = ('Не имеет значения', '1', '2', '3', '4+')
    form["gearboxes"] = ('Не имеет значения', 'Механика', 'Робот', 'Вариатор', 'Автомат')
    form["power"] = 26, 315
    form["wheel_drives"] = ('Не имеет значения', 'Передний', 'Полный', 'Задний')
    form["steering_wheels"] = ('Не имеет значения', 'Левый', 'Правый')
    form["engines"] = ('Не имеет значения', 'Бензин', 'Дизель', 'Газ')
    return form


def get_models_for_brand(df, brand, schema):
    pass


def get_features_for_model(df, brand, model, schema):
    pass

training_cols = ["brand", "model", "car_year", "mileage", "count_owners", "body_type", "gearbox_type", "en_power", "gearbox_type", "wheel_drive", "en_type", "is_climate", "color", "price"]


class SimpleHTTPRequestHandler(BaseHTTPRequestHandler):
    features = get_values_for_html_form(df, schema)
    def do_GET(self):
        # Отправляем заголовки ответа
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()

        # Отправляем html страницу с выпадающими списками и кнопкой отправки
        html = f"""
        <html>
            <head>
                <meta charset="UTF-8">
            </head>
            <body>
                <form action="/" method="post">
                    <label for="brand">Выберите бренд:</label>
                    <select id="brand" name="brand">
                        {"".join([f"<option value='{brand}'>{brand}</option>" for brand in features["brands"]])}
                    </select>
                    <br>

                    <label for="model">Выберите модель:</label>
                    <select id="model" name="model">
                        {"".join([f"<option value='{brand}'>{brand}</option>" for brand in brands])}
                    </select>
                    <br>


                    <label for="year_sign">Выберите максимальный(минимальный)год производства:</label>
                    <input type="radio" id="yonger" name="year_sign" value="yonger" />
                        <label for="yonger">Моложе</label>
                    <input type="radio" id="older" name="year_sign" value="older" />
                        <label for="older">Старше</label>
                        <input id="year" name="year" type="number" min=1936 max=2023>
                    <br>   

                     <label for="mileage">Выберите максимальный пробег:</label>
                        <input id="mileage" name="mileage" type="number" min=0 max=1000000>
                    <br>                          

                    <label for="owners">Выберите максимально возможное количество владельцев:</label>
                    <select id="owners" name="owners">
                        {"".join([f"<option value='{brand}'>{brand}</option>" for brand in brands])}
                    </select>
                    <br>

                    <label for="body_type">Выберите тип кузова:</label>
                    <select id="body_type" name="body_type">
                        {"".join([f"<option value='{brand}'>{brand}</option>" for brand in brands])}
                    </select>
                    <br>

                    <label for="wheel_drive">Выберите тип привода:</label>
                    <select id="wheel_drive" name="wheel_drive">
                        {"".join([f"<option value='{brand}'>{brand}</option>" for brand in brands])}
                    </select>
                    <br>     

                    <label for="steering_wheel">Выберите модель:</label>
                    <select id="steering_wheel" name="steering_wheel">
                        {"".join([f"<option value='{brand}'>{brand}</option>" for brand in brands])}
                    </select>
                    <br>                         

                    <label for="power">Укажите максимальное (минимальное) количество лошадиных сил:</label>
                    <input type="radio" id="less" name="power_sign" value="less" />
                        <label for="less">Меньше</label>
                    <input type="radio" id="more" name="power_sign" value="more" />
                        <label for="more">Больше</label>                    
                        <input id="power" name="power" type="number" min=20 max=315>
                    <br>                       

                    <label for="gearbox">Выберите тип коробки передач:</label>
                    <select id="gearbox" name="gearbox">
                        {"".join([f"<option value='{brand}'>{brand}</option>" for brand in brands])}
                    </select>
                    <br>                                    


                    <label for="color">Выберите цвет:</label>
                    <select id="color" name="color">
                        {"".join([f"<option value='{color}'>{color}</option>" for color in colors])}
                    </select>
                    <br>
                    <input type="submit" value="Отправить">
                </form>
            </body>
        </html>
        """
        self.wfile.write(html.encode('utf-8'))

    def do_POST(self):
        # Считываем данные из тела запроса
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length).decode('utf-8')
        print(post_data)

        # Парсим данные из строки запроса и сохраняем в переменную result
        result = {var.split("=")[0]: var.split("=")[1] for var in post_data.split("&")}

        # Отправляем заголовки ответа
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()

        # Отправляем html страницу с сообщением об успешной отправке данных
        html = """
        <html>
            <body>
                <h1>Данные успешно отправлены!</h1>
            </body>
        </html>
        """
        self.wfile.write(html.encode('utf-8'))


if __name__ == '__main__':
    server_address = ('', 8000)
    httpd = HTTPServer(server_address, SimpleHTTPRequestHandler)
    print('Server running at http://localhost:8000')
    httpd.serve_forever()

