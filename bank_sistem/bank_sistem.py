import textwrap
from abc import ABC, abstractclassmethod, abstractproperty
from datetime import datetime

class Client:
    def __init__(self, address):
        self.address = address
        self.accounts = []

    def perform_transaction(self, account, transaction):
        transaction.register(account)

    def add_account(self, account):
        self.accounts.append(account)


class IndividualPerson(Client):
    def __init__(self, name, birth_date, cpf, address):
        super().__init__(address)
        self.name = name
        self.birth_date = birth_date
        self.cpf = cpf


class Account:
    def __init__(self, number, client):
        self._balance = 0
        self._number = number
        self._branch = "0001"
        self._client = client
        self._history = History()

    @classmethod
    def new_account(cls, client, number):
        return cls(number, client)

    @property
    def balance(self):
        return self._balance

    @property
    def number(self):
        return self._number

    @property
    def branch(self):
        return self._branch

    @property
    def client(self):
        return self._client

    @property
    def history(self):
        return self._history

    def withdraw(self, amount):
        balance = self.balance

        if amount > balance:
            print(f"\nTransaction failed! Insufficient funds. Current balance: $ {balance:.2f}")
            return False

        elif amount > 0:
            self._balance -= amount
            print("\n=== Successful withdrawal! ===")
            return True

        else:
            print("\nTransaction failed! The provided amount is invalid.")
            return False

    def deposit(self, amount):
        if amount > 0:
            self._balance += amount
            print("\n=== Successful deposit! ===")
        else:
            print("\nTransaction failed! The provided amount is invalid.")
        self.history.add_transaction(Deposit(amount))


class CheckingAccount(Account):
    def __init__(self, number, client, limit=500, withdrawal_limit=3):
        super().__init__(number, client)
        self._limit = limit
        self._withdrawal_limit = withdrawal_limit

    def withdraw(self, amount):
        withdrawal_count = len(
            [transaction for transaction in self.history.transactions if transaction["type"] == Withdrawal.__name__]
        )

        exceeded_limit = amount > self._limit
        exceeded_withdrawals = withdrawal_count >= self._withdrawal_limit

        if exceeded_limit:
            print("\nTransaction failed! The withdrawal amount exceeds the limit.")

        elif exceeded_withdrawals:
            print("\nTransaction failed! Maximum number of withdrawals exceeded.")

        else:
            super().withdraw(amount)
            return True

        return False

    def __str__(self):
        return f"""
            Branch:\t\t{self.branch}
            Account:\t{self.number}
            Holder:\t\t{self.client.name}
        """

class History:
    def __init__(self):
        self._transactions = []

    @property
    def transactions(self):
        return self._transactions

    def add_transaction(self, transaction):
        self._transactions.append(
            {
                "type": transaction.__class__.__name__,
                "amount": transaction.amount,
                "date": datetime.now().strftime("%d-%m-%Y %H:%M:%S"),
            }
        )

class Transaction(ABC):
    @property
    @abstractproperty
    def amount(self):
        pass

    @abstractclassmethod
    def register(cls, account):
        pass


class Withdrawal(Transaction):
    def __init__(self, amount):
        self._amount = amount

    @property
    def amount(self):
        return self._amount

    def register(cls, account):
        success_transaction = account.withdraw(cls.amount)

        if success_transaction:
            account.history.add_transaction(cls)


class Deposit(Transaction):
    def __init__(self, amount):
        self._amount = amount

    @property
    def amount(self):
        return self._amount

    def register(cls, account):
        success_transaction = account.deposit(cls.amount)

        if success_transaction:
            account.history.add_transaction(cls)


def menu():
    menu_str = """\n
    ================ MENU ================
    [1]\tDeposit
    [2]\tWithdraw
    [3]\tStatement
    [4]\tNew account
    [5]\tList accounts
    [6]\tNew user
    [0]\tQuit
    => """
    return input(textwrap.dedent(menu_str))


def filter_client(cpf, clients):
    filtered_clients = [client for client in clients if client.cpf == cpf]
    return filtered_clients[0] if filtered_clients else None


def retrieve_client_account(client):
    if not client.accounts:
        print("\nClient does not have an account!")
        return

    return client.accounts[0]


def deposit(clients):
    cpf = input("Enter the client's CPF: ")
    client = filter_client(cpf, clients)

    if not client:
        print("\nClient not found!")
        return

    amount = float(input("Enter the deposit amount: "))
    transaction = Deposit(amount)

    account = retrieve_client_account(client)
    if not account:
        return

    client.perform_transaction(account, transaction)


def withdraw(clients):
    cpf = input("Enter the client's CPF: ")
    client = filter_client(cpf, clients)

    if not client:
        print("\nClient not found!")
        return

    amount = float(input("Enter the withdrawal amount: "))
    transaction = Withdrawal(amount)

    account = retrieve_client_account(client)
    if not account:
        return

    client.perform_transaction(account, transaction)


def display_statement(clients):
    cpf = input("Enter the client's CPF: ")
    client = filter_client(cpf, clients)

    if not client:
        print("\nClient not found!")
        return

    account = retrieve_client_account(client)
    if not account:
        return

    print("\n================ STATEMENT ================")
    transactions = account.history.transactions

    statement = ""
    if not transactions:
            statement = "No transactions have been made."
    else:
        for transaction in transactions:
            statement += f"\n{transaction['type']}:\n\t$ {transaction['amount']:.2f}"

    print(statement)
    print(f"\nBalance:\n\t$ {account.balance:.2f}")
    print("==========================================")

def create_client(clients):
    cpf = input("Enter the CPF (numbers only): ")
    client = filter_client(cpf, clients)

    if client:
        print("\nA client with this CPF already exists!")
        return

    name = input("Enter the full name: ")

    while True:
        birth_date_str = input("Enter the birth date (dd-mm-yyyy): ")
        try:
            birth_date = datetime.strptime(birth_date_str, "%d-%m-%Y")
            break
        except ValueError:
            print("Invalid date format. Please try again.")

    address = input("Enter the address (street, number - neighborhood - city/state): ")

    client = IndividualPerson(name=name, birth_date=birth_date, cpf=cpf, address=address)

    clients.append(client)

    print("\n=== Client created successfully! ===")


def create_account(account_number, clients, accounts):
    cpf = input("Enter the client's CPF: ")
    client = filter_client(cpf, clients)

    if not client:
        print("\nClient not found, account creation process aborted!")
        return

    account = CheckingAccount.new_account(client=client, number=account_number)
    accounts.append(account)
    client.accounts.append(account)

    print("\nAccount created successfully!")


def list_accounts(accounts):
    for account in accounts:
        print("=" * 100)
        print(textwrap.dedent(str(account)))


def main():
    clients = []
    accounts = []

    while True:
        option = menu()

        if option == "1":
            deposit(clients)

        elif option == "2":
            withdraw(clients)

        elif option == "3":
            display_statement(clients)

        elif option == "4":
            create_client(clients)

        elif option == "5":
            account_number = len(accounts) + 1
            create_account(account_number, clients, accounts)

        elif option == "6":
            list_accounts(accounts)

        elif option == "0":
            break

        else:
            print("\nInvalid operation, please select the desired operation again.")

if __name__ == "__main__":
    main()
