import requests

class GestorURL:
    def __init__(self, url : str, parametros={}):
        self.__parametros = parametros
        self.__url_base = 'https://api.ptdata.org'
        self.__url = self.__url_base + url

    def get_api(self):
        api = requests.get(self.__url, params=self.__parametros)
        return api