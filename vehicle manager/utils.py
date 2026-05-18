def ImprimirCor(texto, opcao):
    if opcao == 1:
        print(f"\033[94m{texto}\033[00m")
    elif opcao == 2:
        print(f"\033[92m{texto}\033[00m")
    elif opcao == 3:
        print(f"\033[31m{texto}\033[00m")
    else:
        print(texto)
