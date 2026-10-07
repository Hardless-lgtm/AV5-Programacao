import functions as fn
1

def menu_conexao():
    print("\n=== ESCOLHA A BASE DE DADOS ===")
    print("1: SQLite (Local)")
    print("2: MySQL (Remoto via .env)")
    try:
        op = int(input("Opção: "))
        fn.conectar_banco(op)
    except ValueError:
        print("Entrada inválida.")

def menu_inserir():
    while True:
        print("\n--- MENU INSERIR ---")
        print("1: Inserir Dublador")
        print("2: Inserir Personagem")
        print("3: Criar Contrato (Relacionar)")
        print("4: Voltar")
        op = input("Opção: ")
        if op == '1': fn.adicionar_dublador()
        elif op == '2': fn.adicionar_personagem()
        elif op == '3': fn.relacionar_dublador_personagem()
        elif op == '4': break

def menu_listar():
    while True:
        print("\n--- MENU LISTAR ---")
        print("1: Listar Dubladores")
        print("2: Listar Personagens")
        print("3: Listar Contratos")
        print("4: Voltar")
        op = input("Opção: ")
        if op == '1': fn.listar_dubladores()
        elif op == '2': fn.listar_personagens()
        elif op == '3': fn.listar_contratos()
        elif op == '4': break

def menu_excluir():
    while True:
        print("\n--- MENU EXCLUIR ---")
        print("1: Excluir Dublador")
        print("2: Excluir Personagem")
        print("3: Excluir Contrato")
        print("4: Voltar")
        op = input("Opção: ")
        if op == '1': fn.excluir_dublador()
        elif op == '2': fn.excluir_personagem()
        elif op == '3': fn.excluir_contrato()
        elif op == '4': break

def main():
    menu_conexao()
    
    while True:
        print(f"\n====================================")
        print(f" BASE CONECTADA: {fn.banco_atual}")
        print(f"====================================")
        print("1: Alternar Conexão com Banco")
        print("2: Inserir Dados")
        print("3: Listar Dados")
        print("4: Excluir Dados")
        print("0: Sair")
        
        opcao = input("Digite a opção desejada: ")
        
        if opcao == '1':
            menu_conexao()
        elif opcao == '2':
            menu_inserir()
        elif opcao == '3':
            menu_listar()
        elif opcao == '4':
            menu_excluir()
        elif opcao == '0':
            print("A encerrar o programa...")
            break
        else:
            print("Opção inválida!")

if __name__ == "__main__":
    main()