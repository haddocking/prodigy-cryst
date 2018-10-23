#!/usr/bin/env python3
#
# This code is part of the interface classifier tool distribution
# and governed by its license.  Please see the LICENSE file that should
# have been included as part of this package.
#

"""
Interface classification methods developed by the Bonvin Lab.

Classifier loader.
"""

__author__ = ["Katarina Elez", "Anna Vangone"]

import sys
import pickle
import warnings


with warnings.catch_warnings():
    warnings.simplefilter("ignore")
    features = sys.argv[1:]
    model = pickle.load(open('classifier.sav', 'rb'))
    print(model.predict([features])[0])
