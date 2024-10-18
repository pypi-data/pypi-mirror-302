def deposit(account, value, /):
    if value > 0:
        account["balance"] += value
        account["bank_statement"] += f"Depósito de R$ {value:.2f}\n"
        print(f"Depósito de R$ {value:.2f} realizado com sucesso à conta {account["account_number"]}")
    else:
        print("Erro. O valor a ser depositado deve ser um número maior que zero.")
    return account

def withdraw(*, account, value, limit, withdraw_limit):
    if account["withdraw_number"] < withdraw_limit:
        if value >0:
            if value <= limit:
                if value <= account["balance"]:
                    account["balance"] -= value
                    account["bank_statement"] += f"Saque de R$ {value:.2f}\n"
                    print(f"Saque de R$ {value:.2f} realizado com sucesso à conta {account["account_number"]}.")
                    account["withdraw_number"] += 1
                else:
                    print(f"Lamentamos, mas o valor de saque desejado é maior que o seu saldo de R$ {account["balance"]:.2f}.")
            else:
                print(f"Lamentamos, mas você excedeu o limite de R$ {limit:.2f} por saque.")
        else:
            print("Erro. O valor a ser sacado deve ser um número maior que zero.")
    else:
        print("Lamentamos, mas você excedeu o número de saques diários")
    
    return account

def statement(*, account):
    print("\nEXTRATO DE CONTA")
    print(f"Conta de número: {account["account_number"]}")
    if account["bank_statement"] == "":
        print("Não foram realizadas movimentações")
    else:
        print(account["bank_statement"])
        print(f"\nSaldo de conta: R$ {account["balance"]:.2f}")