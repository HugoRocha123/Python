import json
import datetime
from pathlib import Path


class GestorArquivo:
    def __init__(self, documento: str):
        data = datetime.datetime.now()
        hoje = f"{data.day}-{data.month}-{data.year}"
        self.__file = f"Dados Guardados/{documento}-{hoje}.json"

        path = Path(self.__file)
        path.parent.mkdir(parents=True, exist_ok=True)

        if not path.exists():
            self.abrir_arquivo()

        self.garantir_arquivo_valido()

    def ler_arquivo(self):
        try:
            with open(self.__file, "r", encoding="utf-8") as f:
                conteudo = json.load(f)

                # Garante que o conteúdo seja uma lista
                if isinstance(conteudo, list):
                    return conteudo
                return []

        except (json.JSONDecodeError, FileNotFoundError):
            self.abrir_arquivo()
            return []
        except Exception as erro:
            print(f"Um erro ocorreu no programa\n\"{erro}\"")
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
