import tkinter as tk
from tkinter import messagebox, simpledialog
import os
from voting_cli import (
    register_user, authenticate_user,
    generate_token, cast_vote, get_results,
    CANDIDATES  # import the candidate list
)

current_user = None

def register():
    username = simpledialog.askstring("Register", "Enter username:")
    password = simpledialog.askstring("Register", "Enter password:", show='*')
    success, msg = register_user(username, password)
    messagebox.showinfo("Register", msg)

def login():
    global current_user
    username = simpledialog.askstring("Login", "Enter username:")
    password = simpledialog.askstring("Login", "Enter password:", show='*')

    if not username or not password:
        messagebox.showwarning("Login", "Username or password cannot be empty.")
        return

    success, msg = authenticate_user(username, password)
    if success:
        current_user = username
        messagebox.showinfo("Login", f"Welcome, {username}!")
        if username == "admin":
            admin_panel()
    else:
        messagebox.showerror("Login Failed", msg)

def admin_panel():
    while True:
        choice = simpledialog.askstring("Admin Panel", "Choose action:\n1. Show Results\n2. Exit")
        if choice == "1":
            show_results()
        elif choice == "2" or choice is None:
            break
        else:
            messagebox.showwarning("Invalid", "Choose 1 or 2.")

def get_token():
    if not current_user:
        messagebox.showwarning("Not logged in", "Please login first.")
        return
    token = generate_token(current_user)
    # Use a dialog with selectable text to allow copy:
    token_win = tk.Toplevel()
    token_win.title("Voting Token")
    tk.Label(token_win, text="Your voting token (copy this):").pack(pady=5)
    token_text = tk.Text(token_win, height=2, width=50)
    token_text.pack()
    token_text.insert(tk.END, token)
    token_text.config(state=tk.DISABLED)
    token_text.bind("<Button-1>", lambda e: token_text.config(state=tk.NORMAL))
    token_text.bind("<FocusOut>", lambda e: token_text.config(state=tk.DISABLED))
    tk.Button(token_win, text="Close", command=token_win.destroy).pack(pady=5)

def vote():
    if not current_user:
        messagebox.showwarning("Not logged in", "Please login first.")
        return
    token = simpledialog.askstring("Token", "Enter your voting token:")
    if not token:
        messagebox.showwarning("Input Error", "Token is required.")
        return
    candidate = simpledialog.askstring("Vote", f"Enter group name:\nOptions: {', '.join(CANDIDATES)}")
    if not candidate:
        messagebox.showwarning("Input Error", "Candidate is required.")
        return
    candidate = candidate.strip()
    if candidate not in CANDIDATES:
        messagebox.showerror("Invalid Candidate", f"Please choose from: {', '.join(CANDIDATES)}")
        return
    success, msg = cast_vote(current_user, token, candidate)
    if success:
        messagebox.showinfo("Success", msg)
    else:
        messagebox.showerror("Vote Failed", msg)

def show_results():
    if current_user != "admin":
        messagebox.showerror("Access Denied", "Only admin can view results.")
        return
    results = get_results()
    if not results:
        messagebox.showinfo("Results", "No votes yet.")
        return
    result_str = "\n".join([f"{k}: {v} votes" for k, v in results.items()])
    winner = max(results, key=results.get)
    result_str += f"\n\n🏆 Lucky Group: {winner} with {results[winner]} votes!"
    messagebox.showinfo("Voting Results", result_str)

# ==== MAIN WINDOW ====

root = tk.Tk()
root.title("✈️ Free Australia Trip Voting System")

tk.Label(root, text="Vote for the Group to Win a Free Trip to Australia!", font=("Arial", 14)).pack(pady=10)

tk.Button(root, text="Register", command=register, width=30).pack(pady=5)
tk.Button(root, text="Login", command=login, width=30).pack(pady=5)
tk.Button(root, text="Generate Voting Token", command=get_token, width=30).pack(pady=5)
tk.Button(root, text="Cast Vote", command=vote, width=30).pack(pady=5)
tk.Button(root, text="Show Results (Admin Only)", command=show_results, width=30).pack(pady=5)
tk.Button(root, text="Exit", command=root.destroy, width=30).pack(pady=10)

root.mainloop()
