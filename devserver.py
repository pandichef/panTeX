import hashlib
from time import sleep


def sha1(filename):
    BUF_SIZE = 65536
    sha1 = hashlib.sha1()
    with open(filename, "rb") as f:
        while True:
            data = f.read(BUF_SIZE)
            if not data:
                break
            sha1.update(data)
    return sha1.digest()


def check_for_updates(filename, previous_hash):
    current_hash = sha1(filename)
    if previous_hash is None:
        previous_hash = sha1(filename)
    while True:
        sleep(0.25)
        print(1)
        if current_hash != previous_hash:
            return current_hash
        current_hash = sha1(filename)
