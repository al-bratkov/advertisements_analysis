from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import urlparse, parse_qs


class PetServer(BaseHTTPRequestHandler):
    """
    The simplest server. It was recommended by ChatGPT. It must contain functions do_GET and do_POST.
    You have to assign an instance of the class, perform add_df method and then use the instance
    """
    @classmethod
    def add_df(clf, server_df):
        cols = []
        if not True: #type(server_df) is pd.DataFrame:
            raise TypeError("You need a pandas dataframe")

        clf.server_df = server_df

    def do_GET(self):
        # Отправляем заголовки ответа
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()

        form = self.server_df.extract_values_to_html()
        fill_form = lambda seq: {"".join([f"<option value='{item}'>{item}</option>" for item in seq])}
        with open("Front/main.html", encoding="utf-8") as page:
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

