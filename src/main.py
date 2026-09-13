import os
import shutil


def copy_static_to_public(source, destination):
    if os.path.exists(destination):
        shutil.rmtree(destination)
    shutil.copytree(source, destination)


def main():
    copy_static_to_public("static", "public")


main()