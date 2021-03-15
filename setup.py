import os
from setuptools import setup, find_packages


def read(filename: str) -> str:
    return open(os.path.join(os.path.dirname(__file__), filename)).read()


setup(
    name="pycmp",
    version="0.1.0",
    python_requires=">=3.9.0",
    packages=find_packages(),
    include_package_data=True,
    install_requieres=[
        "ply==3.11"
    ],
    extra_require={
        "linter_pack": [
            "mypy==0.812",
            "isort==5.7.0",
            "flake8==3.8.4",
        ],
        "test": [
            "pytest==6.2.2"
        ]
    },
    entry_points={
        "console_scripts": [
            "pycmp = cmp.__main__:main"
        ]
    },
    download_url="",
    author="Artem Eroshev",
    description="compiler matlab to python",
    long_description=read("README.md")
)
