from .str_to_list import encrypt_bytes_to_list
from .str_to_list import encrypt_str_to_list
from .str_to_list import decrypt_list_to_bytes
from .str_to_list import decrypt_list_to_str
from getpass import getpass


def bytes_from_file(fin) -> bytes:
    with open(fin, "rb") as f:
        s = f.read()
    return s


def bytes_to_file(s: bytes, fout):
    with open(fout, "wb") as f:
        f.write(s)


def str_from_txtfile(fin) -> str:
    with open(fin, encoding="utf-8") as f:
        s = f.read()
    return s


def str_to_txtfile(s: str, fout):
    with open(fout, "w", encoding="utf-8") as f:
        f.write(s)


def bytes_to_file(s, fout):
    with open(fout, "wb") as f:
        f.write(s)


def encrypt_txt(s: str, prompt=None, accept_password=False):
    if not prompt:
        prompt = input("input prompt=")
    password = None
    if accept_password:
        password = getpass("input password=")
    if password:
        encrypted_list = encrypt_str_to_list(s, password)
        encrypted_list[0] = "-"
    else:
        encrypted_list = encrypt_str_to_list(s)
    s2 = "\n".join([prompt] + encrypted_list)
    return s2


def decrypt_txt(s: str):
    encrypted_list = s.split("\n")
    prompt = encrypted_list[0]
    if encrypted_list[1] == "-":
        print(prompt)
        password = getpass("input password=")
        s2 = decrypt_list_to_str(encrypted_list[1:], password)
    else:
        s2 = decrypt_list_to_str(encrypted_list[1:])

    return s2


def encrypt_txtfile(fin, fout, prompt=None, accept_password=False):
    s = str_from_txtfile(fin)
    s2 = encrypt_txt(s, prompt, accept_password)
    str_to_txtfile(s2, fout)


def decrypt_txtfile(fin, fout):
    s = str_from_txtfile(fin)
    s2 = decrypt_txt(s)
    str_to_txtfile(s2, fout)


def encrypt_bytes(s: bytes, prompt=None, accept_password=False):
    if not prompt:
        prompt = input("input prompt=")
    password = None
    if accept_password:
        password = getpass("input password=")
    if password:
        encrypted_list = encrypt_bytes_to_list(s, password)
        encrypted_list[0] = "-"
    else:
        encrypted_list = encrypt_bytes_to_list(s)
    s2 = "\n".join([prompt] + encrypted_list)
    return s2


def decrypt_bytes(s: str):
    encrypted_list = s.split("\n")
    prompt = encrypted_list[0]
    if encrypted_list[1] == "-":
        print(prompt)
        password = getpass("input password=")
        s2 = decrypt_list_to_bytes(encrypted_list[1:], password)
    else:
        s2 = decrypt_list_to_bytes(encrypted_list[1:])

    return s2


def encrypt_file(fin, fout, prompt=None, accept_password=False):
    s = bytes_from_file(fin)
    s2 = encrypt_bytes(s, prompt, accept_password)
    str_to_txtfile(s2, fout)


def decrypt_file(fin, fout):
    s = str_from_txtfile(fin)
    s2 = decrypt_bytes(s)
    bytes_to_file(s2, fout)
