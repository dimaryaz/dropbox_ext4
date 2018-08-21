# Dropbox ext4 Hack

Gets around Dropbox dropping support for non-ext4 filesystems by wrapping the `statfs64` function and overwriting the filesystem type.

## Install the pre-built hack

Just run:

    sudo ./fix_dropbox.py
    dropbox stop
    dropbox start

It will install the hack into `/usr/local/`. You can modify `fix_dropbox.py` to customize that.

## Install from source

Make sure you have GCC installed and run the following:

    make
    sudo make install
