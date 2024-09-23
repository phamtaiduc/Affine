import tkinter as tk
from tkinter import messagebox

# Hàm tính nghịch đảo modulo 26 của a
def mod_inverse(a, m):
    for i in range(1, m):
        if (a * i) % m == 1:
            return i
    return None

# Hàm mã hóa Affine
def affine_encrypt(text, a, b):
    result = ""
    for char in text:
        if char.isalpha():
            char = char.upper()
            result += chr(((a * (ord(char) - 65) + b) % 26) + 65)
        else:
            result += char
    return result

# Hàm giải mã Affine
def affine_decrypt(cipher, a, b):
    result = ""
    a_inv = mod_inverse(a, 26)
    if a_inv is None:
        messagebox.showerror("Lỗi", "Không tìm được nghịch đảo của a")
        return None

    for char in cipher:
        if char.isalpha():
            char = char.upper()
            result += chr(((a_inv * ((ord(char) - 65) - b)) % 26) + 65)
        else:
            result += char
    return result

# Hàm xử lý mã hóa
def encrypt_message():
    text = input_text.get()
    try:
        a = int(key_a.get())
        b = int(key_b.get())
        encrypted = affine_encrypt(text, a, b)
        output_text.set(encrypted)
    except ValueError:
        messagebox.showerror("Lỗi", "Khóa a và b phải là số nguyên")

# Hàm xử lý giải mã
def decrypt_message():
    cipher = input_text.get()
    try:
        a = int(key_a.get())
        b = int(key_b.get())
        decrypted = affine_decrypt(cipher, a, b)
        if decrypted:
            output_text.set(decrypted)
    except ValueError:
        messagebox.showerror("Lỗi", "Khóa a và b phải là số nguyên")

# Tạo giao diện người dùng với Tkinter
root = tk.Tk()
root.title("Dịch vụ bảo mật tin nhắn - Affine Cipher")
root.geometry("400x300")

# Nhãn và ô nhập liệu cho văn bản
tk.Label(root, text="Nhập tin nhắn:").pack(pady=5)
input_text = tk.StringVar()
tk.Entry(root, textvariable=input_text, width=50).pack()

# Nhãn và ô nhập liệu cho khóa a
tk.Label(root, text="Khóa a:").pack(pady=5)
key_a = tk.StringVar()
tk.Entry(root, textvariable=key_a, width=10).pack()

# Nhãn và ô nhập liệu cho khóa b
tk.Label(root, text="Khóa b:").pack(pady=5)
key_b = tk.StringVar()
tk.Entry(root, textvariable=key_b, width=10).pack()

# Nút mã hóa và giải mã
tk.Button(root, text="Mã hóa", command=encrypt_message).pack(pady=10)
tk.Button(root, text="Giải mã", command=decrypt_message).pack(pady=10)

# Kết quả
output_text = tk.StringVar()
tk.Label(root, text="Kết quả:").pack(pady=5)
tk.Entry(root, textvariable=output_text, width=50).pack()

# Chạy ứng dụng
root.mainloop()
