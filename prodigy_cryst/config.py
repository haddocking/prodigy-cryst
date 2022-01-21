#!/usr/bin/env python
#
# This code is part of the interface classifier tool distribution
# and governed by its license.  Please see the LICENSE file that should
# have been included as part of this package.
#

"""
Interface classification methods developed by the Bonvin Lab.

Configuration file.
"""
import shutil

__author__ = ["Anna Vangone", "Joao Rodrigues", "Brian Jimenez"]

# (Absolute) Paths to the freesasa binary and config files
FREESASA_BIN = ""

# No need to set this if FreeSASA version is >= 2:
FREESASA_PAR = ""

if not FREESASA_BIN:
    # not defined, maybe its on the path
    freesasa_exec = shutil.which("freesasa")
    if freesasa_exec:
        FREESASA_BIN = freesasa_exec
