from Python.districts.GestorURL import GestorURL
from Python.districts.GestorArquivos import GestorArquivo


class GestorDistritos:
    def __init__(self, parametros={}):
        self.__api = GestorURL("/v1/geo/districts", parametros)
        self.__arquivo = GestorArquivo("distritos")
        self.__distritos = self.__api.get_api()
        self.guardar_codigos()

    def guardar_codigos(self):
        data = self.__arquivo.ler_arquivo()

        # Se o ficheiro já tiver dados, não adiciona novamente
        if data:
            return

        for distrito in self.__distritos.json()["data"]["districts"]:
            data.append({
                "name": distrito["name"],
                "code": distrito["code"]
            })

        self.__arquivo.salvar_arquivo(data)

    def get_listadistritos(self):
        data = self.__arquivo.ler_arquivo()
        l_d = []
        for distritos in data:
            distrito = distritos["name"]
            l_d.append(distrito)
        return l_d
    
    def get_iddistrito(self, nome):
        data = self.__arquivo.ler_arquivo()
        for distritos in data:
            if distritos["name"] == nome:
                return distritos["code"]