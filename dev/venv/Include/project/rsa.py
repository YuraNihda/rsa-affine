# Розширений алгоритм Евкліда
def egcd(a, b):
    if b == 0:
        return a, 1, 0
    d, x, y = egcd(b, a % b)
    return d, y, x - (a // b) * y

# Функція Ейлера
def eiler_fun(a, b):
    return (a - 1) * (b - 1)

# Перевірка на просте число
def is_prime(n):
    if n <= 1:
        return False
    for i in range(2, int(n**0.5) + 1):
        if n % i == 0:
            return False
    return True

# Модульна обернена
def modinv(a, m):
    gcd, x, _ = egcd(a, m)
    if gcd != 1:
        raise Exception("Оберненого не існує")
    return x % m

# Генерація ключів RSA
def generate_keys():
    p, q = 61, 53  # Простi числа
    n = p * q
    phi = eiler_fun(p, q)
    e = 17  # Вибрано взаємно просте до phi
    d = modinv(e, phi)
    return (e, n), (d, n)

# Шифрування
def encrypt(message, public_key):
    e, n = public_key
    return [pow(ord(char), e, n) for char in message]

# Розшифрування
def decrypt(ciphertext, private_key):
    d, n = private_key
    return ''.join([chr(pow(char, d, n)) for char in ciphertext])

# Створення ключів один раз
public_key, private_key = generate_keys()

def crypt_from_file(file):
    try:
        with open(file, 'r', encoding='utf-8') as f:
            plaintext = f.read()
        encrypted = encrypt(plaintext, public_key)
        return encrypted
    except FileNotFoundError:
        print(f"Файл '{file}' не знайдено.")
    except Exception as e:
        print(f"Сталася помилка: {e}")

def decrypt_from_file(file):
    try:
        with open(file, 'r', encoding='utf-8') as f:
            encrypted_data = f.read()
        
        # Перетворення рядка у список цілих чисел
        encrypted_numbers = list(map(int, encrypted_data.strip().split()))
        
        # Розшифрування
        decrypted_data = decrypt(encrypted_numbers, private_key)
        return decrypted_data
    except FileNotFoundError:
        print(f"Файл '{file}' не знайдено.")
    except Exception as e:
        print(f"Сталася помилка: {e}")


    