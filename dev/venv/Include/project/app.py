from flask import Flask, request, render_template, send_from_directory
from werkzeug.utils import secure_filename
import os
from rsa import generate_keys, encrypt, decrypt, crypt_from_file, decrypt_from_file
from affine import affine_encrypt, affine_decrypt, encrypt_from_file_affine, decrypt_from_file_affine

app = Flask(__name__)
UPLOAD_FOLDER = './uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Генерація ключів один раз
public_key, private_key = generate_keys()

@app.route('/download/<filename>')
def download_file(filename):
    return send_from_directory(UPLOAD_FOLDER, filename, as_attachment=True)

@app.route('/', methods=['GET', 'POST'])
def index():
    encrypted_text = ''
    decrypted_text = ''
    encrypted_text2 = ''
    decrypted_text2 = ''
    file_name = None
    file2 = None
    download_link = None
    error_message = ''
    encrypt_file = False
    decrypt_file = False

    if request.method == 'POST':
        action = request.form.get('action')
        text_data = request.form.get('text', '')
        text_data_2 = request.form.get('text2', '')
        file_data = request.files.get('file')
        file_data_2 = request.files.get('file2')

        if action == 'encrypt':
            if text_data:
                try:
                    encrypted = encrypt(text_data, public_key)
                    encrypted_text = ' '.join(map(str, encrypted))
                except Exception as e:
                    error_message = f"Помилка при шифруванні: {str(e)}"

            if file_data and file_data.filename:
                filename = secure_filename(file_data.filename)
                file_path = os.path.join(UPLOAD_FOLDER, filename)
                file_data.save(file_path)
                try:
                    encrypted_content = crypt_from_file(file_path)
                    output_path = os.path.join(UPLOAD_FOLDER, 'encrypted_output.txt')
                    with open(output_path, 'w', encoding='utf-8') as f:
                        f.write(' '.join(map(str, encrypted_content)))
                    file_name = filename
                    download_link = 'encrypted_output.txt'
                    encrypt_file = True
                    decrypt_file = False
                except Exception as e:
                    error_message = f"Помилка при шифруванні файлу: {str(e)}"

        elif action == 'decrypt':
            if text_data:
                try:
                    numbers = list(map(int, text_data.strip().split()))
                    decrypted = decrypt(numbers, private_key)
                    decrypted_text = decrypted
                except ValueError:
                    decrypted_text = "Помилка: введіть лише числа, розділені пробілами"
                except Exception:
                    decrypted_text = "Помилка при розшифруванні"

            if file_data and file_data.filename:
                filename = secure_filename(file_data.filename)
                file_path = os.path.join(UPLOAD_FOLDER, filename)
                file_data.save(file_path)
                try:
                    decrypted_content = decrypt_from_file(file_path)
                    output_path = os.path.join(UPLOAD_FOLDER, 'decrypted_output.txt')
                    with open(output_path, 'w', encoding='utf-8') as f:
                        f.write(decrypted_content)
                    file_name = filename
                    download_link = 'decrypted_output.txt'
                    encrypt_file = False
                    decrypt_file = True
                except Exception as e:
                    error_message = f"Помилка при розшифруванні файлу: {str(e)}"

        elif action == 'encrypt2':
            if text_data_2:
                try:
                    encrypted_text2 = affine_encrypt(text_data_2, 5, 8)
                except Exception as e:
                    error_message = f"Помилка шифрування (Affine): {str(e)}"

            if file_data_2 and file_data_2.filename:
                filename = secure_filename(file_data_2.filename)
                file_path = os.path.join(UPLOAD_FOLDER, filename)
                file_data_2.save(file_path)
                try:
                    output_path = os.path.join(UPLOAD_FOLDER, 'affine_encrypted.txt')
                    encrypt_from_file_affine(file_path, output_path)
                    file2 = filename
                    download_link = 'affine_encrypted.txt'
                    encrypt_file = True
                    decrypt_file = False
                except Exception as e:
                    error_message = f"Помилка шифрування файлу (Affine): {str(e)}"

        elif action == 'decrypt2':
            if text_data_2:
                try:
                    decrypted_text2 = affine_decrypt(text_data_2, 5, 8)
                except Exception as e:
                    error_message = f"Помилка розшифрування (Affine): {str(e)}"

            if file_data_2 and file_data_2.filename:
                filename = secure_filename(file_data_2.filename)
                file_path = os.path.join(UPLOAD_FOLDER, filename)
                file_data_2.save(file_path)
                try:
                    output_path = os.path.join(UPLOAD_FOLDER, 'affine_decrypted.txt')
                    decrypt_from_file_affine(file_path, output_path)
                    file2 = filename
                    download_link = 'affine_decrypted.txt'
                    encrypt_file = False
                    decrypt_file = True
                except Exception as e:
                    error_message = f"Помилка розшифрування файлу (Affine): {str(e)}"

    return render_template('index.html',
                           encrypted=encrypted_text,
                           decrypted=decrypted_text,
                           encrypted2=encrypted_text2,
                           decrypted2=decrypted_text2,
                           file=file_name,
                           file2=file2,
                           encrypt_file=encrypt_file,
                           decrypt_file=decrypt_file,
                           download_link=download_link,
                           error=error_message)

if __name__ == '__main__':
    app.run(debug=True)
