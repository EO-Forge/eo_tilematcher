#!/usr/bin/env python
from setuptools import setup, find_packages

with open("README.rst") as readme_file:
    readme = readme_file.read()

requirements = []

setup_requirements = []

setup(
    author="EO-Forge",
    author_email="eo.forge.analytics@gmail.com",
    python_requires=">=3.6",
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Natural Language :: English",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
    ],
    description=(
        "Tools to quickly find the Sentinel2, Landasat5, and Landsat8 tiles "
        "that a given region of interest."
    ),
    install_requires=requirements,
    license="MIT license",
    long_description=readme + "\n\n",
    include_package_data=True,
    keywords="eo_tilematcher",
    name="eo_tilematcher",
    packages=find_packages(include=["eo_tilematcher", "eo_tilematcher.*"]),
    setup_requires=setup_requirements,
    test_suite="tests",
    url="https://github.com/EO-Forge/eo_tilematcher",
    version="0.1.0",
    zip_safe=False,
)
