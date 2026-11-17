#!/usr/bin/env python3
#
# This code is part of the interface classifier tool distribution
# and governed by its license.  Please see the LICENSE file that should
# have been included as part of this package.
#

"""
Interface classification methods developed by the Bonvin Lab.

Classifier loader. `data/classifier.npz` holds the 250 trees of the random
forest trained with scikit-learn 0.18.1 (formerly `data/classifier.sav`).
"""

__author__ = ["Katarina Elez", "Anna Vangone", "Brian Jimenez"]

import sys
from pathlib import Path

import numpy as np

FOREST = dict(np.load(Path(Path(__file__).resolve().parent, "data", "classifier.npz")))


def predict(features):
    """Return the class (BIO or XTAL) and the probabilities of both classes."""
    # As scikit-learn, compare the features in single precision
    x = np.array(features, dtype=np.float32)
    left, right = FOREST["left"], FOREST["right"]
    feature, threshold = FOREST["feature"], FOREST["threshold"]
    proba = np.zeros(2)
    for node in FOREST["roots"]:
        while left[node] != -1:
            node = left[node] if x[feature[node]] <= threshold[node] else right[node]
        proba += FOREST["proba"][node]
    proba = (proba / len(FOREST["roots"])).tolist()
    return ["BIO", "XTAL"][proba.index(max(proba))], proba[0], proba[1]


if __name__ == "__main__":
    print(*predict(sys.argv[1:]))
