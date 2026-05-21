from json_manager import GestorEstruturaJSON
from re import fullmatch
from utils import ImprimirCor

def normalizar_matricula(chave):
    chave = chave.strip().upper().replace("-", "")
    if not fullmatch(r"[A-Z0-9]{6}", chave):
        return None
    return f"{chave[:2]}-{chave[2:4]}-{chave[4:6]}"

def input_chave(gestor=None):
    while True:
        chave = normalizar_matricula(input("Digite a matrícula: "))
        if chave is None:
            ImprimirCor('Matrícula inválida - Ex: "AA-BB-11" ou "AABB11"', 3)
            continue
        if gestor is not None and gestor.existe(chave):
            ImprimirCor("Essa matrícula já existe.", 3)
            continue
        return chave

def obter_entrada_veiculo():
    while True:
        tipo = input("Tipo de veículo: ").strip()
        if tipo:
            break
        ImprimirCor("Erro: este campo não pode estar vazio.",3)
    while True:
        marca = input("Marca: ").strip()
        if marca:
            break
        ImprimirCor("Erro: este campo não pode estar vazio.",3)
    while True:
        cor = input("Cor: ").strip()
        if cor:
            break
        ImprimirCor("Erro: este campo não pode estar vazio.",3)
    while True:
        try:
            ano = int(input("Ano: "))
            if ano<1769 or ano>2026:
                ImprimirCor("Ano inválido",3)
                continue
            break
        except ValueError:
            ImprimirCor("Input inválido.",3)
        except Exception as erro:
            ImprimirCor(f"Um erro ocorreu no programa \n \"{erro}\"", 3)
    return {"Marca" : marca, "Tipo de veículo" : tipo, "Ano" : ano, "Cor": cor}

def executar_menu():
    gestor = GestorEstruturaJSON("Trabalho veículos\frota.json")
    while True:
        ImprimirCor("=" * 40, 1)
        ImprimirCor("MENU PRINCIPAL".center(40), 1)
        ImprimirCor("=" * 40, 1)
        ImprimirCor("  1 - Adicionar veículo", 1)
        ImprimirCor("  2 - Recuperar veículo", 1)
        ImprimirCor("  3 - Atualizar veículo", 1)
        ImprimirCor("  4 - Apagar um veículo", 1)
        ImprimirCor("  0 - Sair do programa", 1)
        ImprimirCor("=" * 40, 1)

        try:
            i = int(input('\033[96m Introduza uma opcao: \033[00m'))
            match i:
                case 1:
                    chave = input_chave(gestor)
                    info = obter_entrada_veiculo()
                    if gestor.adicionar(chave, info):
                        ImprimirCor("Veículo criado com sucesso.", 2)
                    else:
                        ImprimirCor("Um erro aconteceu ao criar o veículo.", 3)
                case 2:
                    chave = input_chave()
                    veiculo = gestor.recuperar(chave)
                    if veiculo is not None:
                        ImprimirCor("Veículo encontrado:", 2)
                        for campo, valor in veiculo.items():
                            print(f"{campo}: {valor}")
                    else:
                        ImprimirCor("Veículo não encontrado.", 3)

                case 3:
                    chave = input_chave()
                    if gestor.existe(chave):
                        novo_valor = obter_entrada_veiculo()
                        if gestor.atualizar(chave, novo_valor):
                            ImprimirCor("Veículo atualizado com sucesso.", 2)
                        else:
                            ImprimirCor("Erro ao atualizar o veículo.", 3)
                    else:
                        ImprimirCor("Veículo não encontrado.", 3)
                case 4:
                    chave = input_chave()
                    if gestor.deletar(chave):
                        ImprimirCor("Veículo removido com sucesso.", 2)
                    else:
                        ImprimirCor("A matrícula não foi encontrada.", 3)
                case 0:
                    ImprimirCor("=" * 40, 1)
                    ImprimirCor("A FECHAR O PROGRAMA".center(40), 1)
                    ImprimirCor("=" * 40, 1)
                    break
                case _:
                    ImprimirCor("Opção inválida.", 3)
        except ValueError:
            ImprimirCor("Valor inserido deveria ter sido um numero",3)
        except Exception as erro:
            ImprimirCor(f"Um erro ocorreu no programa \n \"{erro}\"",3)
