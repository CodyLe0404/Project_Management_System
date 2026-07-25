def encrypt_password(password: str, key: str = "LSE") -> str:
    encrypted = []
    for i, ch in enumerate(password):
        xor_value = ord(ch) ^ ord(key[i % len(key)])
        encrypted.append(f"{xor_value:02X}")
    return "".join(encrypted)


def decrypt_password(encrypted_hex: str, key: str = "LSE") -> str:
    result = []
    for i in range(0, len(encrypted_hex), 2):
        value = int(encrypted_hex[i:i+2], 16)
        original = value ^ ord(key[(i // 2) % len(key)])
        result.append(chr(original))
    return "".join(result)
