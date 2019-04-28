import os
import sys


def get_res(path):
    try:
        base_path = os.path.dirname(sys.argv[0])
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, path)
