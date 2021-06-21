import os
import hashlib
from re import template
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
    current_hash = sha1(filename)
    if previous_hash is None:
        previous_hash = sha1(filename)
    while True:
        # sleep(0.01)  # to slow it down
        if current_hash != previous_hash:
            return current_hash
        current_hash = sha1(filename)


class Server(Manager):
    def __init__(self, working_on=None, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        if working_on == None:
            self._working_on = self._template
        else:
            self._working_on = working_on

    def run_dev_server(self):
        self.save_to_html("output.html")
        previous_hash = None
        browser_sync_process = subprocess.Popen(
            'browser-sync start --server --files "*.html" --index "output.html',
            shell=True,
        )
        print("BrowserSync PID: ", browser_sync_process.pid)
        while True:
            # subprocess.Popen
            new_hash = check_for_updates(
                filename=self._working_on, previous_hash=previous_hash
            )

            self.save_to_html("output.html")
            previous_hash = new_hash


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--template",
        "-s",
        required=True,
        # default=os.getcwd(),
        # help="Specify alternative directory " "[default:current directory]",
    )
    args = parser.parse_args()
    s = Server(template=args.template)
    s.run_dev_server()
