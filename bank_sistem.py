menu = '''
  [1] Withdrawal
  [2] Deposit
  [3] Statement
  [0] Exit
'''

available_balance = 500
history = []
withdrawals_made = 0

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

while True:
    option = input(menu)

    if option == "1":
        withdrawal()
    elif option == "2":
        deposit()
    elif option == "3":
        show_statement()
    elif option == "0":
        print("Thank you for using Eduardo's bank")
        break
    else:
        print("Invalid operation, please select your desired operation again.")
