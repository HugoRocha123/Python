from GestorArquivos import GestorArquivo 
from GestorURL import GestorURL 
class GestorMunicipios:
    def __init__(self, parametros=None):
        if parametros is None:
            parametros = {}

        self.__parametros = parametros
        self.__arquivo = GestorArquivo("municipios")
        self.guardar_codigos()

    def guardar_codigos(self):
        data = self.__arquivo.ler_arquivo()
        if data:
            return
        offset = 0
        limit = 100
        while True:
            params = {
                **self.__parametros,
                "limit": limit,
                "offset": offset
            }
            api = GestorURL("/v1/geo/municipalities", params)
            resposta = api.get_api().json()
            municipios = resposta["data"]["municipalities"]
            if not municipios:
                break
            for municipio in municipios:
                data.append({
                    "name": municipio["name"],
                    "code": municipio["code"],
                    "district_code": municipio["district_code"]
                })
            if len(municipios) < limit:
                break
            offset += limit
        self.__arquivo.salvar_arquivo(data)

    def get_listamunicipios(self,id_distri):
        data = self.__arquivo.ler_arquivo()
        l_m = []
        for municipios in data:
            if municipios["district_code"] == id_distri:
                municipio = municipios["name"]
                l_m.append(municipio)
        return l_m