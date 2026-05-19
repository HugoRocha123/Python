from utils import ImprimirCor
from pathlib import Path
import json


class GestorEstruturaJSON:
    def __init__(self, nome_arquivo):
        self.__file = nome_arquivo
        self._garantir_arquivo_valido()

    def adicionar(self, chave, valor):
        data = self._ler_arquivo()
        data.append({chave: valor})
        self._salvar_arquivo(data)
        return True

    def recuperar(self, chave):
        data = self._ler_arquivo()
        for veiculo in data:
            if chave in veiculo:
                return veiculo[chave]
        return None
    
    def atualizar(self, chave, novo_valor):
        data = self._ler_arquivo()
        for veiculo in data:
            if chave in veiculo:
                veiculo[chave] = novo_valor
                self._salvar_arquivo(data)
                return True
        return False

    def deletar(self, chave):
        data = self._ler_arquivo()
        for veiculo in data:
            if chave in veiculo:
                data.remove(veiculo)
                self._salvar_arquivo(data)
                return True
        return False
    
    def existe(self,chave):
        return self.recuperar(chave) is not None
    
    def _ler_arquivo(self):
        try:
            with open(self.__file, "r", encoding="utf-8") as f:
                return json.load(f)
        except (json.JSONDecodeError, FileNotFoundError):
            self._abrir_arquivo()
            return []
        except Exception as erro:
            ImprimirCor(f"Um erro ocorreu no programa \n \"{erro}\"", 3)
            return []

    def _salvar_arquivo(self, data):
        with open(self.__file, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4, ensure_ascii=False)

    def _abrir_arquivo(self):
        with open(self.__file, "w", encoding="utf-8") as file:
            json.dump([], file, indent=4, ensure_ascii=False)
            
    def _garantir_arquivo_valido(self):
        path = Path(self.__file)

        if not path.exists() or path.stat().st_size == 0:
            self._abrir_arquivo()
            return

        try:
            with open(self.__file, "r", encoding="utf-8") as f:
                conteudo = f.read().strip()
                if not conteudo:
                    self._abrir_arquivo()
                    return
                json.loads(conteudo)
        except (json.JSONDecodeError, Exception):
            self._abrir_arquivo()
