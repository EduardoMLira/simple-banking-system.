menu = '''
  [1] Withdrawal
  [2] Deposit
  [3] Statement
  [4] Register User
  [5] Create Bank Account
  [6] List Bank Accounts
  [0] Exit
'''

available_balance = 500
history = []
withdrawals_made = 0
users = []
accounts = []

def show_statement():
    print(f'''
=====================================
         Bank Statement
=====================================
   Branch: xxxx    Account: xxxxxxx-x
   Client: Charles Andrade
=====================================
   Total Balance: R$ {available_balance:.2f}
=====================================
            History
{"".join(history)}=====================================
''')

def withdrawal():
    global available_balance
    global withdrawals_made
    if withdrawals_made < 3:
        withdrawal_amount = float(input("Enter the amount you want to withdraw: "))
        if withdrawal_amount <= available_balance and withdrawal_amount > 0 and withdrawal_amount <= 500.00:
            if available_balance - withdrawal_amount >= 0:
                available_balance -= withdrawal_amount
                history.append(f"Withdrawal of R$ {withdrawal_amount:.2f} completed.\n")
                withdrawals_made += 1
                print(f"You withdrew R$ {withdrawal_amount:.2f}")
            else:
                print("Unable to withdraw due to insufficient balance.")
        else:
            print("Invalid withdrawal amount. Please enter a valid amount within the limit of R$ 500.00.")
    else:
        print("You've reached the maximum limit of 3 daily withdrawals.")

def deposit():
    global available_balance
    deposit_amount = float(input("Enter the deposit amount: "))
    if deposit_amount > 0:
        available_balance += deposit_amount
        history.append(f"Deposit of R$ {deposit_amount:.2f} completed.\n")
        print(f"Deposit of R$ {deposit_amount:.2f} successful!")

def register_user():
    name = input("Enter your full name: ")
    birth_date = input("Enter your birth date (YYYY/MM/DD): ")
    ssn = input("Enter your ssn (only numbers): ")
    address = input("Enter your address (format: street, number - neighborhood - city/state): ")

    if any(user['ssn'] ==  ssn for user in users):
        print("Error: User with this SSN alredy exists.")
        return
    
    users.append({'name': name, 'birth_date': birth_date, 'ssn': ssn, 'address': address})
    print("User registered successfully!")

def create_bank_account():
    global accounts
    global users

    user_ssn = input("Enter the user's CPF to create a bank account: ")

    user_exists = next((user for user in users if user['ssn'] == user_ssn), None)

    if not user_exists:
        print("Error: User does not exist. Please register the user first.")
        return

    if any(account['user']['ssn'] == user_ssn for account in accounts):
        print("Error: User already has a bank account.")
        return

    account_number = len(accounts) + 1
    account = {'agency': '0001', 'account_number': account_number, 'user': user_exists}
    accounts.append(account)

    print(f"Bank account created successfully. Account number: {account_number}")

def list_bank_accounts():
    print("\nList of Bank Accounts:")
    for account in accounts:
        user_info = account['user']
        print(f"Account Number: {account['account_number']} | User: {user_info['name']} | SSN: {user_info['ssn']}")
    print("\n")

while True:
    option = input(menu)

    if option == "1":
        withdrawal()
    elif option == "2":
        deposit()
    elif option == "3":
        show_statement()
    elif option == "4":
        register_user() 
    elif option == "5":
        create_bank_account()
    elif option == "6":
        list_bank_accounts()
    elif option == "0":
        print("Thank you for using Eduardo's bank")
        break
    else:
        print("Invalid operation, please select your desired operation again.")
