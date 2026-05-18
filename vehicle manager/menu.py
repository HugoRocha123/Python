from json_manager import GestorEstruturaJSON
from re import fullmatch
from utils import ImprimirCor


def obter_entrada_veiculo():
    marca = input("Marca: ").strip()
    modelo = input("Modelo: ").strip()
    cor = input("Cor: ").strip()
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
    return {"marca" : marca, "modelo" : modelo, "ano" : ano, "cor": cor}

def executar_menu():
    gestor = GestorEstruturaJSON(r"C:\Users\trukz\Desktop\Programação\Aula2\Trabalho veículos\frota.json")
    while True:
        ImprimirCor("="*30,1)
        ImprimirCor("1 - Adicionar veículo.",1)
        ImprimirCor("2 - Recuperar veículo.",1)
        ImprimirCor("3 - Atualizar veículo.",1)
        ImprimirCor("4 - Apagar um veículo",1)
        ImprimirCor("0 - Sair do programa.",1)
        ImprimirCor("="*30,1)
        try:
            i = int(input('\033[96m Introduza uma opcao: \033[00m'))
            match i:
                    case 1:
                        while True:
                            chave = input("Digite a matrícula: ").strip().upper()
                            if not fullmatch(r"[A-Z0-9]{2}-[A-Z0-9]{2}-[A-Z0-9]{2}", chave):
                                ImprimirCor("Matrícula inválida - Ex: \"AA-BB-11\"", 3)
                                continue
                            if gestor.existe(chave):
                                ImprimirCor("Essa matrícula já existe.", 3)
                                continue
                            break
                        info = obter_entrada_veiculo()
                        if gestor.adicionar(chave, info):
                            ImprimirCor("Veículo criado com sucesso",2)
                        else:
                            ImprimirCor("Um erro aconteceu.",3)
                    case 2:
                        chave = input("Digite a matrícula: ").strip().upper()
                        veiculo = gestor.recuperar(chave)
                        if veiculo:
                            ImprimirCor("Veículo encontrado:", 2)
                            for campo, valor in veiculo.items():
                                print(f"{campo}: {valor}")
                        else:
                            ImprimirCor("Veículo não encontrado.", 3)

                    case 3:
                        chave = input("Digite a matrícula: ").strip().upper()
                        if gestor.recuperar(chave):
                            novo_valor = obter_entrada_veiculo()
                            if gestor.atualizar(chave, novo_valor):
                                ImprimirCor("Veículo atualizado com sucesso.", 2)
                            else:
                                ImprimirCor("Erro ao atualizar o veículo.", 3)
                        else:
                            ImprimirCor("Veículo não encontrado.", 3)

                    case 4:
                        chave = input("Digite a matrícula do veículo que deseja remover: ").upper()
                        if gestor.deletar(chave):
                           ImprimirCor("Veículo removido com sucesso",2)
                        else:
                           ImprimirCor("A matrícula não foi encontrada",3)
                    case 0:
                        ImprimirCor('\nSair do programa.',1)
                        ImprimirCor("="*30,1)
                        break
                    case _:
                        print("Opção inválida.")

        except ValueError:
            ImprimirCor("Valor inserido deveria ter sido um numero",3)
        except Exception as erro:
            ImprimirCor(f"Um erro ocorreu no programa \n \"{erro}\"",3)