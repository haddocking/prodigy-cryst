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

__author__ = ["Katarina Elez", "Anna Vangone", "Brian Jimenez"]

import os
import pickle
import sys
import warnings

with warnings.catch_warnings():
    warnings.simplefilter("ignore")
    features = sys.argv[1:]
    base_path = os.path.dirname(os.path.realpath(__file__))
    model = pickle.load(open(os.path.join(base_path, "data", "classifier.sav"), "rb"))
    proba = list(model.predict_proba([features])[0])
    print(["BIO", "XTAL"][proba.index(max(proba))], proba[0], proba[1])
