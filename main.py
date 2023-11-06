from http.server import BaseHTTPRequestHandler, HTTPServer

from db_module import FromDB, schema
from backend_module import convert_to_html_values, PetServer
from compute_module import ServerDataFrame


db_schema = {"advertisement": "advertisement", "car": "car", "city": "city", "fed_count": "fed_count",
              "region": "region", "brand": "brand", "model": "model", "modification": "modification"}


training_cols = ["brand", "model", "car_year", "mileage", "count_owners", "body_type", "gearbox_type", "en_power", "gearbox_type", "wheel_drive", "en_type", "is_climate", "color", "price"]


if __name__ == '__main__':
    login = input("Enter the login")
    password = input("Enter the password")
    db = input("Enter the name of the database")

    source = FromDB(login, password, db)
    df = source.get_all_db(schema)
    server_df = ServerDataFrame(df)
    my_server = PetServer
    my_server.add_df(server_df)
    server_address = ('', 8000)
    httpd = HTTPServer(server_address, PetServer)
    print('Server running at http://localhost:8000')
    httpd.serve_forever()

