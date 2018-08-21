#!/usr/bin/env python3

import base64
import gzip
import os
import subprocess

# Install a wrapper script as /usr/local/bin/dropbox.
# It *should* be in $PATH before /usr/bin/dropbox, and therefore take precedence.
INSTALL_PATH = '/usr/local/'

# Replace with ~/.local/ if you like - but make sure it's in the $PATH before /usr/bin/!
# INSTALL_PATH = os.path.expanduser('~/.local/')

# Base85-encoded gzipped libdropbox_ext4.so, generated by `encode_lib.py`,
ENCODED_LIB_CONTENTS = (
    'ABzY8O?7))0{`t;-D}fO6u(K<wR2q-#j&~xMwzh98QRXyq0D`6QRc@s21AjMu9+$HV>apBe3>v5`ylL3@UQTB;Db-1e}VWS=#zra8gJ5bYIC<*Me!*=$UXOb-Fxo2hrq'
    'czvkP-P#}R};t`L{o=d1h#$lppe6Dk`eAv#K=)3Xhc#@G`4ln~h)UB6a$T@lt7Wgoo-A+2(LKfZ}y9PE)sz<cq7ooOY%4?OM?^=tWq{kU2lt8unKet2g6db?jCO21?D6'
    'nG!AAV1^9*g<4T_StuN_6O1H*+&o9E3i&KBPY3RI+IhZqLL(*t=sF?$OV$gS=)J{85!NyiKeA3OQX7yO+|$anP0d%HLWF;q>`$hkfW#O;G`VPFt6pFY@3^vVc=u1f0)U'
    'MlS+5U#5tRxW9O*}I&*o`RegHzIL?Y%`L?W9zAmb}V>hXWl)KeusdH4V?!Iw8zNRK>B{V`cYUQ0;`RsHJ()r{4a#(#OEPp2C_MN*gYX>CcINs00CBkh<TyHcS*`tB?QQ'
    '1lQZO{e1NJVK*j9u$&e-L>@#(ORg4)?iN;@Qp6&!l$VT}_J86MjaF?FuuZye-BkKPg5?fB*pk1PBlyK!5-N{vI4dTZq4p#9lQ9{S@|uPeFeK_;H}^XwUX*($9XhUXT4l'
    '7-%=H4~E|zr|41>cn5fl_Y3f={Qt=p_OUEp!2a{o)0gD_`5P+(@~Dzf5^^%07>!>{B<21kBO|N2U6r3t4bW!NGA+Ag>uI8xx@8h2vt4jIMvvMhqTDN#l})2$Ws3zLqfu'
    'SS$mz;P&L)a&Y|*h)^x90tFtzoPo;SQz^n7-WdKT@fCG9|ovR2IJje`Ae^3l%p>#NK=#1P0)A7Se3D6GLVb%k`Vu8z1mf2^MqpyQc3MLOP~-VvvvrfTu?ei~)sXQ=`;i'
    'agdSQn^9=h%v~;6jS#|V|DvQ4>|u--P@3h=e(cF4c=*x&NKe_Zo<BwG|Jy~kR^c+34Yqv<bSgQbIhM4_^HYGv-#5?c7d?(P5yT#f$_)lo3KCopF#t<!Tw0^!yNtby-1c'
    '0kC){)VgEQINB^NF`QsYAi7kNtPLuol0dn-cOwben00'
)

LIBRARY_PATH = os.path.join(INSTALL_PATH, 'lib', 'libdropbox_ext4.so')
SCRIPT_PATH = os.path.join(INSTALL_PATH, 'bin', 'dropbox')

DROPBOX_WRAPPER_CONTENTS = '''
#!/bin/bash

LD_PRELOAD=%s exec /usr/bin/dropbox "$@"
'''.lstrip() % LIBRARY_PATH


def main():
    # Install the library.
    os.makedirs(os.path.join(INSTALL_PATH, 'bin'), exist_ok=True)

    with open(LIBRARY_PATH, 'wb') as fd:
        fd.write(gzip.decompress(base64.b85decode(ENCODED_LIB_CONTENTS)))
        os.fchmod(fd.fileno(), 0o755)

    # Install the wrapper script.
    os.makedirs(os.path.join(INSTALL_PATH, 'lib'), exist_ok=True)

    with open(SCRIPT_PATH, 'w') as fd:
        fd.write(DROPBOX_WRAPPER_CONTENTS)
        os.fchmod(fd.fileno(), 0o755)

    print("Installed the library and the wrapper script at:\n  %s\n  %s" % (LIBRARY_PATH, SCRIPT_PATH))
    print("(To uninstall, simply delete them.)")

    # Check that the correct 'dropbox' is in the $PATH.
    result = subprocess.check_output(['which', 'dropbox']).decode().rstrip()
    if result != SCRIPT_PATH:
        print()
        print("You will need to fix your $PATH! Currently, %r takes precedence." % result)


if __name__ == '__main__':
    main()