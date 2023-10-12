from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import urlparse, parse_qs
from html import escape

brands = ['1', '2', '3']
colors = ["blue", "green", "red"]

result = []


class SimpleHTTPRequestHandler(BaseHTTPRequestHandler):

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
                    <br>
                    <select id="brand" name="brand">
                        {"".join([f"<option value='{brand}'>{brand}</option>" for brand in brands])}
                    </select>
                    <br>
                    
                    <label for="model">Выберите модель:</label>
                    <br>
                    <select id="model" name="model" disabled>
                        {"".join([f"<option value='{model}'>{model}</option>" for model in brands])}
                    </select>
                    <br>
                    

                    <label for="year_sign">Выберите максимальный(минимальный)год производства:</label>
                    <br>
                    <input type="radio" id="younger" name="year_sign" value="yonger" checked="checked"/>
                        <label for="yonger">Моложе</label>
                    <input type="radio" id="older" name="year_sign" value="older" />
                        <label for="older">Старше</label>
                        <input id="car_year" name="car_year" type="number" min=1936 max=2023>
                    <br>   
                    
                    <label for="mileage">Выберите максимальный пробег:</label>
                    <br>
                        <input id="mileage" name="mileage" type="number" min=0 max=1000000>
                    <br>           
                                   
                    
                    <label for="owners">Выберите максимально возможное количество владельцев:</label>
                    <br>
                    <select id="owners" name="owners">
                        {"".join([f"<option value='{brand}'>{brand}</option>" for brand in brands])}
                    </select>
                    <br>
                    
                    <label for="body_type">Выберите тип кузова:</label>
                    <br>
                    <select id="body_type" name="body_type" disabled>
                        {"".join([f"<option value='{brand}'>{brand}</option>" for brand in brands])}
                    </select>
                    <br>
                    
                    <label for="wheel_drive">Выберите тип привода:</label>
                    <br>
                    <select id="wheel_drive" name="wheel_drive">
                        {"".join([f"<option value='{brand}'>{brand}</option>" for brand in brands])}
                    </select>
                    <br>     
                    
                    <label for="steering_wheel">Выберите модель:</label>
                    <br>
                    <select id="steering_wheel" name="steering_wheel">
                        {"".join([f"<option value='{brand}'>{brand}</option>" for brand in brands])}
                    </select>
                    <br>                         
                    
                    <label for="power">Укажите максимальное (минимальное) количество лошадиных сил:</label>
                    <br>
                    <input type="radio" id="less" name="power_sign" value="less" checked="checked"/>
                        <label for="less">Меньше</label>
                    <input type="radio" id="more" name="power_sign" value="more" />
                        <label for="more">Больше</label>                    
                        <input id="power" name="power" type="number" min=20 max=315>
                    <br>                       
                    
                    <label for="gearbox">Выберите тип коробки передач:</label>
                    <br>
                    <select id="gearbox" name="gearbox">
                        {"".join([f"<option value='{brand}'>{brand}</option>" for brand in brands])}
                    </select>
                    <br>                                    
                     
                                 
                    <label for="color">Выберите цвет:</label>
                    <br>
                    <select id="color" name="color">
                        {"".join([f"<option value='{color}'>{color}</option>" for color in colors])}
                    </select>
                    <br>
                    
                    <label for="power">Необходим ли кондиционер:</label>
                    <br>
                    <input type="radio" id="true" name="is_climate" value="true" />
                        <label for="True">Да</label>
                    <input type="radio" id="false" name="is_climate" value="false" checked="checked"/>
                        <label for="False">Нет</label> 
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
