# https://api.ptdata.org/docs#tag/Weather
# https://requests.readthedocs.io/en/latest/

from Python.districts.GestorContratos import GestorContratos
from Python.districts.GestorDistritos import GestorDistritos
from Python.districts.GestorMunicipios import GestorMunicipios


if __name__ == '__main__':
    districts = GestorDistritos()
    districts.guardar_codigos()

    municipios = GestorMunicipios()
    municipios.guardar_codigos()

    contratos = GestorContratos(1106)
    lista_contratos = contratos.obter_contratos()
    for l in lista_contratos:
        print(l)
    #contratos.guardar_contratos()

    
    #print(json.dumps(resposta.json(), indent=4))
    #for distrito in resposta.json()["data"]["districts"]:
        #print(distrito)