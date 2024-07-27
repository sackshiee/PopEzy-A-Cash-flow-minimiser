import tkinter as tk
from tkinter import ttk, messagebox

class CashFlowMinimizerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("PopEzy🍿")

        self.friends = []
        self.transactions = []

        # Friend section
        self.friend_frame = ttk.LabelFrame(self.root, text="Friends")
        self.friend_frame.pack(padx=10, pady=10, fill="x")

        self.friend_name_label = ttk.Label(self.friend_frame, text="Name:")
        self.friend_name_label.pack(side="left", padx=5)

        self.friend_name_entry = ttk.Entry(self.friend_frame)
        self.friend_name_entry.pack(side="left", padx=5)

        self.friend_add_button = ttk.Button(self.friend_frame, text="Add Friend", command=self.add_friend)
        self.friend_add_button.pack(side="left", padx=5)

        self.friend_listbox = tk.Listbox(self.friend_frame, height=5)
        self.friend_listbox.pack(padx=5, pady=5, fill="x")

        # Transaction section
        self.transaction_frame = ttk.LabelFrame(self.root, text="Transactions")
        self.transaction_frame.pack(padx=10, pady=10, fill="x")

        self.payer_label = ttk.Label(self.transaction_frame, text="Payer:")
        self.payer_label.grid(row=0, column=0, padx=5, pady=5)

        self.payer_combobox = ttk.Combobox(self.transaction_frame, state="readonly")
        self.payer_combobox.grid(row=0, column=1, padx=5, pady=5)

        self.payee_label = ttk.Label(self.transaction_frame, text="Payee:")
        self.payee_label.grid(row=1, column=0, padx=5, pady=5)

        self.payee_combobox = ttk.Combobox(self.transaction_frame, state="readonly")
        self.payee_combobox.grid(row=1, column=1, padx=5, pady=5)

        self.amount_label = ttk.Label(self.transaction_frame, text="Amount:")
        self.amount_label.grid(row=2, column=0, padx=5, pady=5)

        self.amount_entry = ttk.Entry(self.transaction_frame)
        self.amount_entry.grid(row=2, column=1, padx=5, pady=5)

        self.add_transaction_button = ttk.Button(self.transaction_frame, text="Add Transaction", command=self.add_transaction)
        self.add_transaction_button.grid(row=3, column=0, columnspan=2, pady=5)

        self.transaction_listbox = tk.Listbox(self.transaction_frame, height=5)
        self.transaction_listbox.grid(row=4, column=0, columnspan=2, padx=5, pady=5, sticky="ew")

        # Calculate button
        self.calculate_button = ttk.Button(self.root, text="Calculate Minimal Transactions", command=self.calculate_minimal_transactions)
        self.calculate_button.pack(padx=10, pady=10)

    def add_friend(self):
        name = self.friend_name_entry.get().strip()
        if name and name not in self.friends:
            self.friends.append(name)
            self.friend_listbox.insert(tk.END, name)
            self.payer_combobox['values'] = self.friends
            self.payee_combobox['values'] = self.friends
            self.friend_name_entry.delete(0, tk.END)
        else:
            messagebox.showerror("Error", "Invalid or duplicate friend name")

    def add_transaction(self):
        payer = self.payer_combobox.get()
        payee = self.payee_combobox.get()
        try:
            amount = float(self.amount_entry.get())
            if payer and payee and amount > 0 and payer != payee:
                self.transactions.append((payer, payee, amount))
                self.transaction_listbox.insert(tk.END, f"{payer} paid {payee} INR{amount}")
                self.amount_entry.delete(0, tk.END)
            else:
                raise ValueError
        except ValueError:
            messagebox.showerror("Error", "Invalid transaction details")

    def calculate_minimal_transactions(self):
        balances = {friend: 0 for friend in self.friends}
        for payer, payee, amount in self.transactions:
            balances[payer] -= amount
            balances[payee] += amount

        debtors = sorted((f for f in balances if balances[f] < 0), key=lambda f: balances[f])
        creditors = sorted((f for f in balances if balances[f] > 0), key=lambda f: -balances[f])

        transactions = []
        while debtors and creditors:
            debtor = debtors[0]
            creditor = creditors[0]
            amount = min(-balances[debtor], balances[creditor])
            balances[debtor] += amount
            balances[creditor] -= amount
            transactions.append(f"{debtor} pays {creditor} INR{amount:.2f}")

            if balances[debtor] == 0:
                debtors.pop(0)
            if balances[creditor] == 0:
                creditors.pop(0)

        result_window = tk.Toplevel(self.root)
        result_window.title("Minimal Transactions")
        result_text = "\n".join(transactions) if transactions else "No transactions needed"
        result_label = tk.Label(result_window, text=result_text)
        result_label.pack(padx=10, pady=10)

if __name__ == "__main__":
    root = tk.Tk()
    app = CashFlowMinimizerApp(root)
    root.mainloop()
