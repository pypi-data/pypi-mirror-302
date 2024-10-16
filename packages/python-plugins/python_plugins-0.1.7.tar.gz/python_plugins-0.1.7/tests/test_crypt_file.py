import os
import os.path as op
import filecmp
from python_plugins.random.random_str import rand_sentence
from python_plugins.crypto.file_to_file import encrypt_txtfile
from python_plugins.crypto.file_to_file import decrypt_txtfile
from python_plugins.crypto.file_to_file import encrypt_file
from python_plugins.crypto.file_to_file import decrypt_file


tmp_path = op.join(os.path.dirname(os.path.abspath(__file__)), "tmp")

path_1 = op.join(tmp_path, "test1.txt")
path_2 = op.join(tmp_path, "test2.txt")
path_3 = op.join(tmp_path, "test3.txt")
path_4 = op.join(tmp_path, "test4.txt")
path_5 = op.join(tmp_path, "test5.txt")


def _create_temp():
    if not op.exists(tmp_path):
        os.mkdir(tmp_path)
        return tmp_path


def safe_delete(path):
    try:
        if op.exists(path):
            os.remove(path)
    except:
        pass


def _remove_testfiles():
    safe_delete(path_1)
    safe_delete(path_2)
    safe_delete(path_3)
    safe_delete(path_4)
    safe_delete(path_5)


def test_crypto_file():
    create_tmp = _create_temp()
    if create_tmp:
        print(create_tmp)

    prompt = "test"

    with open(path_1, "w") as f:
        f.write(rand_sentence(30))
        f.write(rand_sentence(30))

    encrypt_txtfile(path_1, path_2, prompt=prompt)
    decrypt_txtfile(path_2, path_3)
    cmp_result = filecmp.cmp(path_1, path_3)
    assert cmp_result is True

    encrypt_file(path_1, path_4, prompt=prompt)
    decrypt_file(path_2, path_5)
    cmp_result = filecmp.cmp(path_1, path_5)
    assert cmp_result is True

    _remove_testfiles()

# pytest with `input()` must using `-s` 
# pytest tests\test_crypt_file.py::test_crypto_file_with_password -s
def _test_crypto_file_with_password():
    prompt = "test"

    with open(path_1, "w") as f:
        f.write(rand_sentence(30))
        f.write(rand_sentence(30))

    encrypt_txtfile(path_1, path_2, accept_password=True)
    decrypt_txtfile(path_2, path_3)
    cmp_result = filecmp.cmp(path_1, path_3)
    assert cmp_result is True

    encrypt_file(path_1, path_4, accept_password=True)
    decrypt_file(path_2, path_5)
    cmp_result = filecmp.cmp(path_1, path_5)
    assert cmp_result is True

    _remove_testfiles()
