# SIMPLE BANK PACKAGE

Description. 
The package simple-bank-package is used to:
	- Simulate a simple bank system
	- There are bank operation functions and account register functions
Functions:
	- account.register_user(cpf = string, name = string, birth_date = string, address = string, users = list of dict) -> return users (adding a new user)
		- new user = {
                "cpf": cpf,
                "name": name,
                "birth_date": birth_date,
                "address": address
			}
	- account.create_account(cpf = string, users = list of dict, accounts = list of dict) -> return accounts (adding a new account)
		- new account = {
                "agency": "0001",
                "account_number": len(accounts)+1,
                "user": user,
                "balance": 0,
                "bank_statement": "",
                "withdraw_number": 0
            }
	- bank_operations.deposit(account = dict, value = float / positional only arguments) -> return account (with operation executed)
	- bank_operations.withdraw(account = dict, value = float, limit = float, withdraw_limit = interger / keyword only arguments) -> return account (with operation executed)
		- limit = maximum value for withdraw operation
		- withdraw_limit = maximum number of withdraws allowed
	- bank_operations.statement(account = dict / keyword only argument) -> print the account statement

## Installation

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install simple-bank-package

```bash
pip install simple-bank-package
```

## Usage

```python
from simple_bank import account, bank_operations
users=[]
accounts=[]
account.register_user('000.000.000-00', 'Client_name', 'DD/MM/YYYY', 'Client_address', users)
print(users[0]["name"])
account.create_account('000.000.000-00', users, accounts)
print(accounts[0]["account_number"])
bank_operations.deposit(accounts[0], 100.00)
bank_operations.withdraw(account = accounts[0], value = 50, limit = 500, withdraw_limit = 3)
bank_operations.statement(account = accounts[0])
```

## Author
Rafael Alves
