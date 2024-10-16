#!/usr/bin/env python
# -*- coding:utf-8 -*-

from setuptools import setup, find_packages

setup(
    name="bdci",
    version='1.0.0',
    keywords=["pip", "bdci", "vqi"],
    description="Bjontegaard Delta Confidence Interval",  # 描述
    long_description="Python library for computing Bjontegaard Delta-Confidence Interval (BDCI)",
    license="MIT Licence",  # 许可证
    url="https://github.com/fgvfgfg564/BDCI",  # 项目相关文件地址，一般是github项目地址即可
    author="fgvfgfg564",  # 作者
    author_email="xyhang@pku.edu.cn",
    packages=find_packages(),
    include_package_data=True,
    platforms="any",
    install_requires=[
        "numpy",
        "scipy",
        "torch>=2.0.1",
        "tqdm",
        "transformers",
        "typing_extensions",
    ],  # 这个项目依赖的第三方库
)
