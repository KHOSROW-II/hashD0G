import hashlib
import base64
import tkinter as tk
from tkinter import messagebox


# ---------- Crypto Core ----------

def derive_key(password):
    return hashlib.sha256(password.encode()).digest()

def encrypt(text, password):
    key = derive_key(password)
    data = text.encode()

    encrypted = bytearray()
    for i, b in enumerate(data):
        x = b ^ key[i % len(key)]
        x = (x + key[(i + 3) % len(key)]) % 256
        encrypted.append(x)

    return base64.b64encode(encrypted).decode()

def decrypt(cipher, password):
    try:
        key = derive_key(password)
        data = base64.b64decode(cipher)

        decrypted = bytearray()
        for i, b in enumerate(data):
            x = (b - key[(i + 3) % len(key)]) % 256
            x = x ^ key[i % len(key)]
            decrypted.append(x)

        return decrypted.decode()
    except Exception:
        return None


# ---------- GUI Actions ----------

def do_encrypt():
    text = input_text.get("1.0", tk.END).strip()
    password = key_entry.get()

    if not text or not password:
        messagebox.showerror("Error", "Text and key are required")
        return

    result = encrypt(text, password)
    output_text.delete("1.0", tk.END)
    output_text.insert(tk.END, result)

def do_decrypt():
    cipher = input_text.get("1.0", tk.END).strip()
    password = key_entry.get()

    if not cipher or not password:
        messagebox.showerror("Error", "Text and key are required")
        return

    result = decrypt(cipher, password)
    if result is None:
        messagebox.showerror("Error", "The key is wrong or data is invalid")
    else:
        output_text.delete("1.0", tk.END)
        output_text.insert(tk.END, result)

def do_clear():
    input_text.delete("1.0", tk.END)
    output_text.delete("1.0", tk.END)
    key_entry.delete(0, tk.END)


# ---------- Window ----------

root = tk.Tk()
root.title("KHOSROW Crypto Tool")
root.geometry("600x500")
root.resizable(False, False)

# Colors
BG_COLOR = "#1e1e1e"
BTN_COLOR = "#c0c0c0"
BTN_TEXT = "#000000"
TEXT_BG = "#2b2b2b"
TEXT_FG = "#ffffff"

root.configure(bg=BG_COLOR)

# ---------- Widgets ----------

tk.Label(root, text="Input / Encrypted Text",
         bg=BG_COLOR, fg="white").pack()

input_text = tk.Text(root, height=8, bg=TEXT_BG, fg=TEXT_FG, insertbackground="white")
input_text.pack(fill="x", padx=10)

tk.Label(root, text="Key (Password)",
         bg=BG_COLOR, fg="white").pack()

key_entry = tk.Entry(root, show="*", bg=TEXT_BG, fg=TEXT_FG, insertbackground="white")
key_entry.pack(fill="x", padx=10)

frame = tk.Frame(root, bg=BG_COLOR)
frame.pack(pady=10)

tk.Button(frame, text="Encrypt", width=15,
          command=do_encrypt,
          bg=BTN_COLOR, fg=BTN_TEXT,
          activebackground="#a9a9a9").pack(side="left", padx=5)

tk.Button(frame, text="Decrypt", width=15,
          command=do_decrypt,
          bg=BTN_COLOR, fg=BTN_TEXT,
          activebackground="#a9a9a9").pack(side="left", padx=5)

tk.Button(frame, text="Clear", width=15,
          command=do_clear,
          bg=BTN_COLOR, fg=BTN_TEXT,
          activebackground="#a9a9a9").pack(side="left", padx=5)

tk.Label(root, text="Output",
         bg=BG_COLOR, fg="white").pack()

output_text = tk.Text(root, height=8, bg=TEXT_BG, fg=TEXT_FG, insertbackground="white")
output_text.pack(fill="x", padx=10)

root.mainloop()
