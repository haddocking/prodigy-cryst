import os
from setuptools import setup
import codecs


def read(fname):
    return codecs.open(
        os.path.join(os.path.dirname(__file__), fname), encoding="utf-8"
    ).read()


with open("requirements.txt") as f:
    required = f.read().splitlines()

setup(
    name="prodigy_cryst",
    version="1.0.1",
    description=(
        "Predicts if a protein complex interface is biological or crystallographic."
    ),
    url="http://github.com/haddocking/prodigy-cryst",
    author="Computational Structural Biology Group @ Utrecht University",
    author_email="prodigy.bonvinlab@gmail.com",
    license="Apache 2.0",
    packages=["prodigy_cryst", "prodigy_cryst.lib"],
    package_dir={"prodigy_cryst": "prodigy_cryst"},
    package_data={"prodigy_cryst": ["data/*.sav", "data/*.csv"]},
    long_description=read("README.md"),
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "License :: OSI Approved :: Apache Software License",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10"
        "Topic :: Scientific/Engineering :: Chemistry",
        "Topic :: Scientific/Engineering :: Bio-Informatics",
    ],
    python_requires=">=3.9, <3.10",
    install_requires=required,
    entry_points={
        "console_scripts": [
            "prodigy_cryst = prodigy_cryst.interface_classifier:main",
        ]
    },
    zip_safe=False,
)
