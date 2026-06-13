from GestorURL import GestorURL 

class GestorContratos:
    def __init__(self, municipality):
        parametros = {}
        parametros["municipality"] = municipality
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
                "procedure_type" : contrato.get("procedure_type"),
                "contract_price": contrato.get("contract_price"),
                "publication_date": contrato.get("publication_date"),
                "district_code": contrato.get("district_code"),
                "municipality_code": contrato.get("municipality_code")
            })

        return lista
