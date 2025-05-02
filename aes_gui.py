import tkinter as tk
from tkinter import messagebox, filedialog
from aes128 import encrypt_block, decrypt_block, pad_message, unpad_message, derive_key_from_password, key_expansion

def encrypt():
    plaintext = input_text.get("1.0", tk.END).strip()
    password = key_entry.get().strip()
    if not plaintext or not password:
        messagebox.showerror("Error", "Please enter both text and password.")
        return

    key = derive_key_from_password(password)
    schedule = key_expansion(key)
    padded = pad_message(plaintext)
    ciphertext = []

    for i in range(0, len(padded), 16):
        block = list(map(ord, padded[i:i+16]))
        encrypted_block = encrypt_block(block, schedule)
        ciphertext.extend(encrypted_block)

    output_text.delete("1.0", tk.END)
    output_text.insert(tk.END, ''.join(f'{b:02x}' for b in ciphertext))

def decrypt():
    ciphertext_hex = input_text.get("1.0", tk.END).strip()
    password = key_entry.get().strip()
    if not ciphertext_hex or not password:
        messagebox.showerror("Error", "Please enter both ciphertext and password.")
        return

    try:
        ciphertext = [int(ciphertext_hex[i:i+2], 16) for i in range(0, len(ciphertext_hex), 2)]
    except ValueError:
        messagebox.showerror("Error", "Invalid ciphertext format.")
        return

    if len(ciphertext) % 16 != 0:
        messagebox.showerror("Error", "Ciphertext length is not a multiple of 16.")
        return

    key = derive_key_from_password(password)
    schedule = key_expansion(key)
    decrypted = []

    for i in range(0, len(ciphertext), 16):
        block = ciphertext[i:i+16]
        decrypted_block = decrypt_block(block, schedule)
        decrypted.extend(decrypted_block)

    try:
        plain_text = ''.join(chr(b) for b in decrypted)
        plain_text = unpad_message(plain_text)
    except Exception as e:
        messagebox.showerror("Error", f"Decryption failed: {str(e)}")
        return

    output_text.delete("1.0", tk.END)
    output_text.insert(tk.END, plain_text)
def load_from_file():
    filepath = filedialog.askopenfilename(title="Select message file", filetypes=[("Text Files", "*.txt")])
    print("Selected file:", filepath)  # <-- ADD THIS
    if filepath:
        with open(filepath, "r") as f:
            contents = f.read()
        input_text.delete("1.0", tk.END)
        input_text.insert(tk.END, contents)

# GUI setup
root = tk.Tk()
root.title("AES-128 Encryptor/Decryptor")

tk.Label(root, text="Enter Text or Cipher (hex):").pack()
input_text = tk.Text(root, height=6, width=60)
input_text.pack()

tk.Button(root, text="Load from File", command=load_from_file).pack(pady=2)

tk.Label(root, text="Enter Password:").pack()
key_entry = tk.Entry(root, show="*", width=40)
key_entry.pack()

tk.Button(root, text="Encrypt", command=encrypt).pack(pady=2)
tk.Button(root, text="Decrypt", command=decrypt).pack(pady=2)

tk.Label(root, text="Output:").pack()
output_text = tk.Text(root, height=6, width=60)
output_text.pack()

root.mainloop()
