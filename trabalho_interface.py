# https://api.ptdata.org/docs#tag/Weather
# https://requests.readthedocs.io/en/latest/

from GestorContratos import GestorContratos
from GestorDistritos import GestorDistritos
from GestorMunicipios import GestorMunicipios


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