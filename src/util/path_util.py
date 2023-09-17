import os


def mkdirs(dir):
    try:
        os.makedirs(dir)
    except FileExistsError:
        pass
