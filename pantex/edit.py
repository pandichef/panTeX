import os
import hashlib
from re import template

from pandas.core import base
from pantex.publish import Manager
from time import sleep
from typing import Union
from typing_extensions import Literal
from string import Template
import pickle
import subprocess
import pandas as pd
import seaborn as sns
import matplotlib


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
    current_hash = sha1(filename[0]) + sha1(filename[1])
    if previous_hash is None:
        previous_hash = sha1(filename[0]) + sha1(filename[1])
    while True:
        # sleep(0.01)  # to slow it down
        if current_hash != previous_hash:
            return current_hash
        current_hash = sha1(filename[0]) + sha1(filename[1])


class Server(Manager):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self._file_being_watched_1 = self._template
        self._file_being_watched_2 = self._context

    def run_server(self):
        self.save_to_html()
        previous_hash = None
        browser_sync_process = subprocess.Popen(
            f'browser-sync start --server --files "*.html" --index {self._html_ouput_file_name}',
            shell=True,
        )
        print("BrowserSync PID: ", browser_sync_process.pid)
        while True:
            new_hash = check_for_updates(
                filename=[self._file_being_watched_1, self._file_being_watched_2],
                previous_hash=previous_hash,
            )
            passed = False
            while not passed:
                # This is a hack; reading context file too quickly is a problem
                try:
                    self.save_to_html()
                    passed = True
                except EOFError as e:
                    pass
            previous_hash = new_hash


if __name__ == "__main__":
    import os
    import argparse

    # see http.server in standard library
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "template", type=str, help="The template file path (md)",
    )
    args = parser.parse_args()
    splitname = args.template.split(".")
    basename = ".".join(splitname[:-1])
    extension = splitname[-1]
    if not os.path.isfile(basename + ".pkl"):
        print(f"{basename}.pkl not found.  Creating an empty context file...")
        with open(f"{basename}.pkl", "wb") as fn:
            fn.write(pickle.dumps({}))
    else:
        with open(f"{basename}.pkl", "rb") as fn:
            pickle_data = pickle.loads(fn.read())
        if len(pickle_data) == 0:
            print(
                f"[WARNING] {basename}.pkl contains no data.  Use pantex.Manager.save_context to create context."
            )
    s = Server(template=args.template)
    s.run_server()
