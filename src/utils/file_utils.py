import os

FILE_NAME = "debug.txt"


def append(content:str):
    with open(FILE_NAME, "a") as f:
        f.write("\n")
        f.write(content)

if not os.path.exists(FILE_NAME):
    open(FILE_NAME, "w").close()