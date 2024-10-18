from setuptools import setup, find_packages

setup(
    name="vector-sdk",
    version="0.0.1",
    author="Dhruv Anand",
    author_email="dhruv.anand@ainorthstartech.com",
    description="Universal SDK for Vector DBs",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)
