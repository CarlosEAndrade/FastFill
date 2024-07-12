from base64 import b64encode, b64decode
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
from Crypto.Random import get_random_bytes

SKey_hex = "8bd0c5cf9db7b9b6d115feb91097d5f3ae1a8cfbe5f38b0e7d19ebacd0cf9087"
key = bytes.fromhex(SKey_hex)

def encrypt(data):
    iv = get_random_bytes(AES.block_size)  # Gerar o IV dentro da função
    cipher = AES.new(key, AES.MODE_CBC, iv)
    encrypted_data = cipher.encrypt(pad(data.encode(), AES.block_size))
    return b64encode(iv + encrypted_data).decode('utf-8')

def decrypt(encrypted_data):
    try:
        encrypted_data = b64decode(encrypted_data)
        iv = encrypted_data[:AES.block_size]
        encrypted_data = encrypted_data[AES.block_size:]
        cipher = AES.new(key, AES.MODE_CBC, iv)
        decrypted_data = unpad(cipher.decrypt(encrypted_data), AES.block_size)
        return decrypted_data.decode('utf-8')
    except (ValueError, KeyError) as e:
        # Adicionar manuseio de exceções para erros de descriptografia
        print(f"Erro na descriptografia: {e}")
        return None

