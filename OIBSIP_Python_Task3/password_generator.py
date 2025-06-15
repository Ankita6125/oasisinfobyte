import tkinter as tk
from tkinter import messagebox, ttk
import random
import string
import pyperclip


def check_password_strength(password):
    length = len(password)
    has_upper = any(c.isupper() for c in password)
    has_lower = any(c.islower() for c in password)
    has_digit = any(c.isdigit() for c in password)
    has_symbol = any(c in string.punctuation for c in password)

    score = sum([has_upper, has_lower, has_digit, has_symbol])

    if length >= 8 and score == 4:
        return "Strong", "green", 100
    elif length >= 6 and score >= 3:
        return "Medium", "orange", 66
    else:
        return "Weak", "red", 33
    

def generate_password():
    length = password_length.get()

    if not (use_upper.get() or use_lower.get() or use_digits.get() or use_symbols.get()):
        messagebox.showerror("Error", "Please select at least one character type.")
        return

    try:
        length = int(length)
        if length <= 0:
            raise ValueError
    except ValueError:
        messagebox.showerror("Error", "Enter a valid password length (positive number).")
        return

    characters = ""
    if use_upper.get():
        characters += string.ascii_uppercase
    if use_lower.get():
        characters += string.ascii_lowercase
    if use_digits.get():
        characters += string.digits
    if use_symbols.get():
        characters += string.punctuation

    excluded = exclude_chars.get()
    for ch in excluded:
        characters = characters.replace(ch, "")

    if not characters:
        messagebox.showerror("Error", "No characters left to generate password.")
        return

    password = ''.join(random.choice(characters) for _ in range(length))
    password_entry.delete(0, tk.END)
    password_entry.insert(0, password)

    
    strength, color, progress_val = check_password_strength(password)
    strength_label.config(text=f"Strength: {strength}", fg=color)
    strength_bar['value'] = progress_val

def copy_to_clipboard():
    pwd = password_entry.get()
    if pwd:
        pyperclip.copy(pwd)
        show_toast("Password copied to clipboard!")

def show_toast(msg):
    toast_label.config(text=msg)
    toast_label.place(relx=0.5, rely=0.95, anchor='center')
    
    root.after(2000, lambda: toast_label.place_forget())


root = tk.Tk()
root.title("🔐 Advanced Password Generator")
root.geometry("450x550")
root.config(bg="#e6f2ff", padx=20, pady=20)

title_label = tk.Label(root, text="Advanced Password Generator", font=("Helvetica", 14, "bold"), fg="#003366", bg="#e6f2ff")
title_label.pack(pady=8)

tk.Label(root, text="Password Length:", bg="#e6f2ff", font=("Arial", 12)).pack()
password_length = tk.Entry(root, font=("Arial", 12), width=10, bg="white")
password_length.pack(pady=5)


use_upper = tk.BooleanVar()
use_lower = tk.BooleanVar()
use_digits = tk.BooleanVar()
use_symbols = tk.BooleanVar()

tk.Checkbutton(root, text="Include Uppercase (A-Z)", variable=use_upper, font=("Arial", 11), bg="#e6f2ff").pack(anchor='w')
tk.Checkbutton(root, text="Include Lowercase (a-z)", variable=use_lower, font=("Arial", 11), bg="#e6f2ff").pack(anchor='w')
tk.Checkbutton(root, text="Include Digits (0-9)", variable=use_digits, font=("Arial", 11), bg="#e6f2ff").pack(anchor='w')
tk.Checkbutton(root, text="Include Symbols (!@#$)", variable=use_symbols, font=("Arial", 11), bg="#e6f2ff").pack(anchor='w')

tk.Label(root, text="Exclude Characters (optional):", bg="#e6f2ff", font=("Arial", 12)).pack(pady=(15, 5))
exclude_chars = tk.Entry(root, font=("Arial", 12), bg="white")
exclude_chars.pack(pady=5)

tk.Label(root, text="Generated Password:", bg="#e6f2ff", font=("Arial", 12)).pack(pady=(15, 5))
password_entry = tk.Entry(root, font=("Courier", 14), bg="white", fg="green", justify="center")
password_entry.pack(pady=5)

strength_label = tk.Label(root, text="", font=("Arial", 12, "bold"), bg="#e6f2ff")
strength_label.pack(pady=5)

strength_bar = ttk.Progressbar(root, length=300, mode='determinate', maximum=100)
strength_bar.pack(pady=5)


toast_label = tk.Label(root, text="", bg="#007acc", fg="white", font=("Arial", 10, "bold"), padx=10, pady=5)



tk.Button(root, text="Generate Password", command=generate_password, font=("Arial", 10, "bold"), bg="#007acc", fg="white", padx=8, pady=3).pack(pady=10)
tk.Button(root, text="Copy to Clipboard", command=copy_to_clipboard, font=("Arial", 10, "bold"), bg="#00b386", fg="white", padx=8, pady=5).pack(pady=5)

root.mainloop()
