import os
from setuptools import setup, find_packages


def read(filename: str) -> str:
    return open(os.path.join(os.path.dirname(__file__), filename)).read()


setup(
    name="pycmp",
    version="0.1.0",
    python_requires=">=3.9.0",
    license="MIT",
    packages=find_packages(),
    include_package_data=True,
    install_requieres=[
        "ply==3.11",
        "numpy==1.20.2"
    ],
    extra_requires={
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
    keywords=['MATLAB', 'Compiler'],
    download_url="https://github.com/aeroshev/CMP/archive/refs/tags/v0.1.0-alpha.tar.gz",
    url="https://github.com/aeroshev/CMP",
    author="Artem Eroshev",
    author_email="faster.boy2694@gmail.com",
    description="compiler matlab to python",
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.9'
    ]
)
