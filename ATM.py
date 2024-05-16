class User:
    def __init__(self, user_id, pin, balance=0):
        self.user_id = user_id
        self.pin = pin
        self.balance = balance
        self.transaction_history = []

    def add_transaction(self, transaction):
        self.transaction_history.append(transaction)

    def display_transaction_history(self):
        if not self.transaction_history:
            print("No transactions found.")
        else:
            for transaction in self.transaction_history:
                print(transaction)

    def display_balance(self):
        print(f"Current balance: ${self.balance}")

    def withdraw(self, amount):
        if amount > self.balance:
            print("Insufficient funds.")
            return False
        else:
            self.balance -= amount
            self.add_transaction(f"Withdraw: ${amount}")
            print(f"${amount} withdrawn successfully.")
            return True

    def deposit(self, amount):
        self.balance += amount
        self.add_transaction(f"Deposit: ${amount}")
        print(f"${amount} deposited successfully.")

    def transfer(self, recipient, amount):
        if amount > self.balance:
            print("Insufficient funds.")
            return False
        else:
            self.balance -= amount
            recipient.balance += amount
            self.add_transaction(f"Transfer: ${amount} to User {recipient.user_id}")
            recipient.add_transaction(f"Transfer: ${amount} from User {self.user_id}")
            print(f"${amount} transferred successfully to User {recipient.user_id}.")
            return True


class Bank:
    def __init__(self):
        self.users = {}

    def add_user(self, user_id, pin, balance=0):
        self.users[user_id] = User(user_id, pin, balance)

    def authenticate_user(self, user_id, pin):
        user = self.users.get(user_id)
        if user and user.pin == pin:
            return user
        return None


class ATM:
    def __init__(self, bank):
        self.bank = bank
        self.current_user = None

    def start(self):
        print("---------Welcome to the ATM!-------------")
        user_id = input("Enter your user ID: ")
        pin = input("Enter your PIN: ")

        user = self.bank.authenticate_user(user_id, pin)
        if user:
            self.current_user = user
            self.show_menu()
        else:
            print("Authentication failed. Please check your user ID and PIN.")

    def show_menu(self):
        while True:
            print("\nATM Menu:")
            print("1. Transaction History")
            print("2. Display Balance")
            print("3. Withdraw")
            print("4. Deposit")
            print("5. Transfer")
            print("6. Quit")
            choice = input("Enter your choice: ")

            if choice == '1':
                self.current_user.display_transaction_history()
            elif choice == '2':
                self.current_user.display_balance()
            elif choice == '3':
                amount = float(input("Enter the amount to withdraw: "))
                self.current_user.withdraw(amount)
            elif choice == '4':
                amount = float(input("Enter the amount to deposit: "))
                self.current_user.deposit(amount)
            elif choice == '5':
                recipient_id = input("Enter the recipient user ID: ")
                recipient = self.bank.users.get(recipient_id)
                if not recipient:
                    print("Recipient user ID not found.")
                else:
                    amount = float(input("Enter the amount to transfer: "))
                    self.current_user.transfer(recipient, amount)
            elif choice == '6':
                print("Thank you for using the ATM. Goodbye!")
                break
            else:
                print("Invalid choice. Please try again.")

if __name__ == "__main__":
    bank = Bank()
    bank.add_user("user1", "1234", 1000)
    bank.add_user("user2", "5678", 500)
    bank.add_user("user3", "5831", 4500)

    atm = ATM(bank)
    atm.start()