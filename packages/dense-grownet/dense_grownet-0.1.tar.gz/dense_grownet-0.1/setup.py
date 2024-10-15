from setuptools import setup, find_packages

setup(
    name="dense-grownet",
    version="0.01",
    packages=find_packages(),
    install_requires=[
        "torch",
        "scikit-learn",
    ],
)
