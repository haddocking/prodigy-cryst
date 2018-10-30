import os
from setuptools import setup
import codecs

def read(fname):
    return codecs.open(os.path.join(os.path.dirname(__file__), fname), encoding='utf-8').read()

requirements = [
    "numpy",
    "biopython",
]

setup(
    name='prodigy_cryst',
    version = "1.0.0",
    description=("Predicts if a protein complex interface is biological or crystallographic."),
    url='http://github.com/haddocking/prodigy-cryst',
    author='Computational Structural Biology Group @ Utrecht University',
    author_email='prodigy.bonvinlab@gmail.com',
    license='Apache 2.0',
    packages=['prodigy_cryst'],
    long_description=read('README.md'),
    classifiers=[
        "Development Status :: 4 - Beta",
        "License :: OSI Approved :: Apache Software License",
    ],
    install_requires=requirements,
    entry_points={
        'console_scripts': [
            'prodigy_cryst = prodigy_cryst.interface_classifier:main',
        ]
    },
    zip_safe=False
)
