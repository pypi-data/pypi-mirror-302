#!/usr/bin/env python
# -*- coding:utf-8 -*-

from setuptools import setup, find_packages

setup(
    name="bdci",
    version='0.0.1',
    keywords=["pip", "bdci", "vqi"],
    description="Bjontegaard Delta Confidence Interval",
    long_description="Python library for computing Bjontegaard Delta-Confidence Interval (BDCI)",
    license="MIT Licence",
    url="https://github.com/fgvfgfg564/BDCI",
    author="Xinyu Hang, NERCVT, PKU",
    author_email="xyhang@pku.edu.cn",
    packages=find_packages(),
    include_package_data=True,
    platforms="any",
    install_requires=[
        "python>=3.9",
        "numpy",
        "scipy",
        "torch>=1.7",
        "tqdm",
        "transformers",
        "typing_extensions",
    ],
)
