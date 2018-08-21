#!/usr/bin/env python3

"""
Encodes the shared library so it can be stored inline in `fix_installer.py`.
"""

import base64
import gzip
import textwrap


INPUT_FILE = 'libdropbox_ext4.so'


def main():
    with open(INPUT_FILE, 'rb') as fd:
        contents = fd.read()

    encoded_contents = base64.b85encode(gzip.compress(contents)).decode()

    print("ENCODED_LIB_CONTENTS = (")
    for line in textwrap.wrap(encoded_contents, 128):
        print("    '%s'" % line)
    print(")")


if __name__ == '__main__':
    main()
