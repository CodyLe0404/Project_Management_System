from app.config import get_key_config

config = get_key_config()
KEY = config["key"]

def encrypt_password(password: str) -> str:
    key = KEY
    print(key)
    encrypted = []
    for i, ch in enumerate(password):
        xor_value = ord(ch) ^ ord(key[i % len(key)])
        encrypted.append(f"{xor_value:02X}")
    return "".join(encrypted)


# def decrypt_password(encrypted_hex: str) -> str:
#     key = KEY
#     result = []
#     for i in range(0, len(encrypted_hex), 2):
#         value = int(encrypted_hex[i:i+2], 16)
#         original = value ^ ord(key[(i // 2) % len(key)])
#         result.append(chr(original))
#     return "".join(result)
