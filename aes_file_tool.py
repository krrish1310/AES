from aes128 import key_expansion, encrypt_block, decrypt_block, pad, unpad

def encrypt_file(input_path, output_path, key):
    with open(input_path, 'r', encoding='utf-8') as f:
        plain_text = f.read()

    key_schedule = key_expansion(key)
    padded = pad(plain_text)

    cipher_text = ''
    for i in range(0, len(padded), 16):
        block = padded[i:i+16]
        cipher_text += encrypt_block(block, key_schedule)

    with open(output_path, 'wb') as f:
        f.write(cipher_text.encode('latin1'))

    print(f"✅ Encrypted file saved as {output_path}")

def decrypt_file(input_path, output_path, key):
    with open(input_path, 'rb') as f:
        cipher_text = f.read().decode('latin1')

    key_schedule = key_expansion(key)

    decrypted = ''
    for i in range(0, len(cipher_text), 16):
        block = cipher_text[i:i+16]
        decrypted += decrypt_block(block, key_schedule)

    plain_text = unpad(decrypted)
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(plain_text)

    print(f"✅ Decrypted file saved as {output_path}")

# Example usage
if __name__ == "__main__":
    key = "Thats my Kung Fu"  # 16-byte key

    encrypt_file("message.txt", "message.enc", key)
    decrypt_file("message.enc", "message_dec.txt", key)
