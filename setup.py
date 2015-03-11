#!/usr/bin/env python
try:
    from setuptools import setup
except ImportError:
    from ez_setup import use_setuptools
    use_setuptools()

from setuptools import setup  # noqa: F811


setup(
    name="vanhateren",
    version="0.0.1",
    author="Eric Hunsberger",
    author_email="ehunsber@uwaterloo.ca",
    url="https://github.com/hunse/vanhateren",
    license="MIT",
    description="Work with the VanHateren natural image database",
    requires=[
        "numpy (>=1.7.0)",
    ],
    packages=["vanhateren"],
    scripts=[],
)
