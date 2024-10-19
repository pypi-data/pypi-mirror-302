def create_account(cpf, users, accounts):
    for user in users:
        if cpf == user["cpf"]:
            accounts.append({
                "agency": "0001",
                "account_number": len(accounts)+1,
                "user": user,
                "balance": 0,
                "bank_statement": "",
                "withdraw_number": 0
            })
            print(f"Conta número {accounts[-1]["account_number"]} cadastrada com sucesso.")
            return accounts
    print("Este CPF não foi cadastrado. Efetue o cadastro de usuário antes de cadastrar sua conta.")
    return accounts

def register_user(cpf, name, birth_date, address, users):
    for user in users:
        if cpf == user["cpf"]:
            print("Este CPF já foi cadastrado. Tente novamente.")
            return users
    users.append({
                "cpf": cpf,
                "name": name,
                "birth_date": birth_date,
                "address": address
            })
    print(f"Cliente {users[-1]["name"]} cadastrado com sucesso.")
    return users