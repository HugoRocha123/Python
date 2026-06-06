# https://api.ptdata.org/docs#tag/Weather
# https://requests.readthedocs.io/en/latest/

import requests
import json
from pathlib import Path
import datetime

class GestorArquivo:
    def __init__(self, documento: str):
        data = datetime.datetime.now()
        hoje = f"{data.day}-{data.month}-{data.year}"
        self.__file = f"Trabalho distritos/{documento}{hoje}.json"

        path = Path(self.__file)
        path.parent.mkdir(parents=True, exist_ok=True)

        if not path.exists():
            self.abrir_arquivo()

        self.garantir_arquivo_valido()

    def ler_arquivo(self):
        try:
            with open(self.__file, "r", encoding="utf-8") as f:
                return json.load(f)
        except (json.JSONDecodeError, FileNotFoundError):
            self.abrir_arquivo()
            return []
        except Exception as erro:
            print(f"Um erro ocorreu no programa \n \"{erro}\"", 3)
            return []

    def abrir_arquivo(self):
        path = Path(self.__file)
        path.parent.mkdir(parents=True, exist_ok=True)

        if not path.exists():
            with open(self.__file, "w", encoding="utf-8") as file:
                json.dump([], file, indent=4, ensure_ascii=False)

    def salvar_arquivo(self, data):
        path = Path(self.__file)
        path.parent.mkdir(parents=True, exist_ok=True)

        with open(self.__file, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4, ensure_ascii=False)

    def garantir_arquivo_valido(self):
        path = Path(self.__file)
        if not path.exists() or path.stat().st_size == 0:
            self.abrir_arquivo()
            return

        try:
            with open(self.__file, "r", encoding="utf-8") as f:
                conteudo = f.read().strip()
                if not conteudo:
                    self.abrir_arquivo()
                    return
                json.loads(conteudo)
        except (json.JSONDecodeError, Exception):
            self.abrir_arquivo()

class GestorURL:
    def __init__(self, url : str, parametros={}):
        self.__parametros = parametros
        self.__url_base = 'https://api.ptdata.org'
        self.__url = self.__url_base + url

    def get_api(self):
        api = requests.get(self.__url, params=self.__parametros)
        return api

class GestorMunicipios:
    def __init__(self, parametros=None):
        if parametros is None:
            parametros = {}

        self.__parametros = parametros
        self.__arquivo = GestorArquivo("municipios")

    def guardar_codigos(self):
        data = self.__arquivo.ler_arquivo()
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

class GestorContratos:
    def __init__(self, district, municipality):
        parametros = {}
        parametros["municipality"] = municipality
        parametros["disctrict"] = district
        self.__api = GestorURL("/v1/contracts", parametros)

    def obter_contratos(self):
        resposta = self.__api.get_api()
        if resposta.status_code != 200:
            return []

        try:
            dados = resposta.json()
        except Exception as erro:
            print("Erro ao converter JSON:", erro)
            return []
        contratos = dados.get("data", {}).get("contracts") or []

        lista = []
        for contrato in contratos:
            lista.append({
                "id": contrato.get("id"),
                "object": contrato.get("object"),
                "contract_price": contrato.get("contract_price"),
                "publication_date": contrato.get("publication_date"),
                "district_code": contrato.get("district_code"),
                "municipality_code": contrato.get("municipality_code")
            })

        return lista

    #Recebe o parametro e vai returnar a lista dos municiopios do distrito inserido

class GestorDistritos:
    def __init__(self,parametros={}):
        self.__api = GestorURL("/v1/geo/districts",parametros)
        self.__arquivo = GestorArquivo(f"distritos")
        self.__distritos = self.__api.get_api()

    def guardar_codigos(self):
        data = self.__arquivo.ler_arquivo()
        for distrito in self.__distritos.json()["data"]["districts"]:
            data.append({
                "name": distrito["name"],
                "code": distrito["code"]
            })
        self.__arquivo.salvar_arquivo(data)


if __name__ == '__main__':
    districts = GestorDistritos()
    districts.guardar_codigos()

    municipios = GestorMunicipios()
    municipios.guardar_codigos()

    contratos = GestorContratos(13,1106)
    lista_contratos = contratos.obter_contratos()
    for l in lista_contratos:
        print(l)
    #contratos.guardar_contratos()

    
    #print(json.dumps(resposta.json(), indent=4))
    #for distrito in resposta.json()["data"]["districts"]:
        #print(distrito)
