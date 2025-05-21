from math import gcd
import base64

M = 256
A = 5
B = 8

def mod_inverse(a, m):
    for i in range(1, m):
        if (a * i) % m == 1:
            return i
    raise ValueError(f"Модульна обернена не існує для a={a} mod {m}")

def affine_encrypt(text, a=A, b=B):
    if gcd(a, M) != 1:
        raise ValueError(f"Ключ 'a' = {a} має бути взаємно простим з M = {M}")

    byte_data = text.encode('utf-8')  # кодуємо в байти
    encrypted_bytes = bytearray()
    for byte in byte_data:
        enc = (a * byte + b) % M
        encrypted_bytes.append(enc)
    # Для зручності повертаємо base64 рядок
    return base64.b64encode(encrypted_bytes).decode('ascii')

def affine_decrypt(encoded_cipher, a=A, b=B):
    if gcd(a, M) != 1:
        raise ValueError(f"Ключ 'a' = {a} має бути взаємно простим з M = {M}")

    a_inv = mod_inverse(a, M)
    encrypted_bytes = base64.b64decode(encoded_cipher.encode('ascii'))
    decrypted_bytes = bytearray()
    for byte in encrypted_bytes:
        dec = (a_inv * (byte - b)) % M
        decrypted_bytes.append(dec)
    return decrypted_bytes.decode('utf-8')

def encrypt_from_file_affine(file_path, output_path, a=A, b=B):
    with open(file_path, 'r', encoding='utf-8') as f:
        text = f.read()
    encrypted = affine_encrypt(text, a, b)
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(encrypted)

def decrypt_from_file_affine(file_path, output_path, a=A, b=B):
    with open(file_path, 'r', encoding='utf-8') as f:
        encoded_cipher = f.read()
    decrypted = affine_decrypt(encoded_cipher, a, b)
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(decrypted)
