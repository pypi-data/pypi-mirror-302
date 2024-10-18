from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="fx-python-sdk-cli",
    version="0.1.1",
    author="FX",
    author_email="fx@fx.com",
    description="Interact with FX Port to share / retrieve AAS Submodel",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/fvolz/fx-python-sdk-cli",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    install_requires=[
        'PyYAML>=6.0.2',
        'requests>=2.32.3',
    ],
)