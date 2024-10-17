from setuptools import setup, find_packages

setup(
    name="AWKDE",
    version="0.1.1",
    packages=find_packages(),
    install_requires=[
        "numpy>=1.19.5"
    ],
    author="Javad Jafari",
    author_email="javad.jafari@mail.um.ac.ir",
    description="A package for Adaptive Weighted Kernel Density Estimation",
)
