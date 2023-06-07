import textwrap

def menu():
    menu = f'''\n
                                ============================
                                =      BANCO - PYTHON      =
                                ============================
                                = 1 - \tDEPÓSITO           =
                                = 2 - \tSAQUE              =
                                = 3 - \tEXTRATO            =
                                = 4 - \tNOVA CONTA         =
                                = 5 - \tLISTAR CONTAS      =
                                = 6 - \tNOVO USUÁRIO       =
                                = 0 - \tSAIR               =
                                ============================
    '''
    return input(textwrap.dedent(menu))

#(/) como argumento indica que todos os argumentos foram definidos como "positional only"
def depositar(saldo, valor, extrato, /):
    if valor > 0:
        saldo += valor
        extrato += f'\t+R${valor:.2f}\n'
        print('\n *** DEPÓSITO REALIZADO COM SUCESSO ***')

    else:
        print('\n *** ERRO! VALOR INFORMADO É INVÁLIDO. ***')

    return saldo, extrato

#(*) como argumento indica que todos os argumentos foram definidos como "keyword only"
def sacar(*, saldo, valor, extrato, limite, numero_saques, limite_saques):
    excedeu_saldo = valor > saldo
    excedeu_limite = valor > limite
    excedeu_saques = numero_saques > limite_saques

    if excedeu_saldo:
        print('\n *** ERRO! VOCÊ NÃO TEM SALDO SUFICIENTE! ***')

    elif excedeu_limite:
        print('\n *** ERRO! O VALOR DO SAQUE EXCEDE O LIMITE! ***')

    elif excedeu_saques:
        print('\n *** ERRO! VOCÊ ATINGIU O LIMITE DE SAQUES DIÁRIO! ***')

    elif valor > 0:
        saldo -= valor
        extrato += f'\t-R$ {valor:.2f}\n'
        numero_saques += 1
        print('\n *** SAQUE REALIZADO COM SUCESSO! ***')

    else:
        print('\n *** ERRO! VALOR INFORMADO É INVÁLIDO! ***')

    return saldo, extrato

#saldo antes da (/) indica argumento por posição e extrato depois do (*) indica argumento por chave
def exibir_extrato(saldo, /, *, extrato):
    print('===============================================')
    print('                    EXTRATO         ')
    print('Não foram realizadas movimentações.' if not extrato else extrato)
    print('===============================================')

def criar_usuario(usuarios):
    cpf = input('Informe o CPF (somente números): ')
    usuario = filtrar_usuario(cpf, usuarios)

    if usuario:
        print('\n *** ERRO! JÁ EXISTE USUÁRIO COM ESSE CPF! ***')
        return

    nome = input('Informe nome completo: ')
    data_nascimento = input('Informe a data de nascimento (dd/mm/aaaa): ')
    endereco = input('Informe o endereço (logradouro, n - bairro - cidade/sigla estado): ')

    usuarios.append({'nome': nome, 'data_nascimento': data_nascimento, 'cpf': cpf, 'endereco': endereco})

    print('*** USUÁRIO CRIADO COM SUCESSO! ***')

def filtrar_usuario(cpf, usuarios):
    usuarios_filtrados = [usuario for usuario in usuarios if usuario['cpf'] == cpf]
    return usuarios_filtrados[0] if usuarios_filtrados else None

def criar_conta(agencia, numero_conta, usuarios):
    cpf = input('Informe o CPF do usuário: ')
    usuario = filtrar_usuario(cpf, usuarios)

    if usuario:
        print('\n *** USUÁRIO CRIADO COM SUCESSO! *** ')
        return {'agencia': agencia, 'numero_conta': numero_conta, 'usuario': usuario}

    print('\n *** USUÁRIO NÃO ENCONTRADO! ***')

def listar_contas(contas):
    for conta in contas:
        linha = f'''\
            Agencia: \t{conta['agencia']}
            C/C: \t\t{conta['numero_conta']}
            Titular: \t{conta['usuario']['nome']}
        '''
        print('=' * 100)
        print(textwrap.dedent(linha))

def main():
    LIMITE_SAQUES = 3
    AGENCIA = '0001'

    saldo = 0
    limite = 500
    extrato = ''
    numero_saques = 0
    usuarios = []
    contas = []

    while True:
        opcao = menu()

        if opcao == '1':
            valor = float(input('Informe o valor do depósito: '))

            saldo, extrato = depositar(saldo, valor, extrato)

        elif opcao == '2':
            valor = float(input('Informe o valor do saque: '))

            saldo, extrato = sacar(
                saldo = saldo,
                valor = valor,
                extrato = extrato,
                limite = limite,
                numero_saques = numero_saques,
                limite_saques = LIMITE_SAQUES,
            )

        elif opcao == '3':
            exibir_extrato(saldo, extrato=extrato)

        elif opcao == '4':
            numero_conta = len(contas) + 1
            conta = criar_conta(AGENCIA, numero_conta, usuarios)

            if conta:
                contas.append(conta)

        elif opcao == '5':
            listar_contas(contas)

        elif opcao == '6':
            criar_usuario(usuarios)

        elif opcao == '7':
            break

        else:
            print('*** ERRO! FAVOR SELECIONE UMA OPERAÇÃO VÁLIDA *** ')

main()