import json
import os
from pprint import pprint
import requests
from dotenv import load_dotenv

load_dotenv()


class Server:
    API_TOKEN = os.getenv("API_TOKEN")
    SERVER_ID = os.getenv("SERVER_ID")
    BASE_API_URL = f"https://api.hetzner.cloud/v1/servers/{SERVER_ID}/"
    HEADERS = {"Authorization": f"Bearer {API_TOKEN}"}

    def __init__(self):
        self.session = requests.session()
        self.session.headers = self.HEADERS

    def get_all_actions(self):
        return self.session.get(Server.BASE_API_URL + "actions/").content

    def get_server(self):
        res = self.session.get(Server.BASE_API_URL)
        res_dict = json.loads(res.content)
        return res_dict

    def print_server_status(self):
        print(self.get_server()["server"]["status"])

    def poweron(self):
        res = self.session.post(Server.BASE_API_URL + "actions/poweron")
        res_dict = json.loads(res.content)
        if res.status_code >= 200 and res.status_code < 300:
            print("\n Сервер запускается...\n")
            while True:
                if self.get_server()["server"]["status"] == "running":
                    print("\n Сервер успешно запущен\n")
                    return False
        else:
            print("Ошибка")
            print(res_dict)

    def shutdown(self):
        res = self.session.post(Server.BASE_API_URL + "actions/shutdown")
        res_dict = json.loads(res.content)
        if res.status_code >= 200 and res.status_code < 300:
            print("\n Сервер выключается...\n")
            while True:
                if self.get_server()["server"]["status"] == "off":
                    print("\n Сервер успешно выключен\n")
                    return False
        else:
            print("Ошибка")
            pprint(res_dict)


server = Server()
