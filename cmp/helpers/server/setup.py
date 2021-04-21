from setuptools import setup, find_packages

setup(
    name="client cmp",
    version="0.1.0",
    python_requires=">=3.9.0",
    packages=find_packages(),
    include_package_data=True,
    install_requieres=[],
    extra_require={},
    entry_points={
        "console_scripts": [
            "tcmp = tcp_client:main"
        ]
    },
    download_url="",
    author="Artem Eroshev",
    description="client for compiler matlab to python"
)
