"""
File containing the required information to successfully build a python package
"""

import setuptools

with open("README.md", "r", encoding="utf-8", newline="\n") as fh:
    long_description = fh.read()

setuptools.setup(
    name='window_asset_tkinter',
    version='1.0.6',
    packages=setuptools.find_packages(),
    install_requires=[
        "tkcalendar>=1.6.1",
        "Pillow>=10.4.0"
    ],
    author="Henry Letellier",
    author_email="henrysoftwarehouse@protonmail.com",
    description="A module that contains boilerplates to speed up the creation of tkinter windows",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Hanra-s-work/window_asset_tkinter",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
