import setuptools

with open("README.md", "r") as file:
    long_description = file.read()


setuptools.setup(
    name="dafin",
    version="0.0.1",
    author="Moein Kareshk",
    author_email="mkareshk@outlook.com",
    description="Finance Data",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/mkareshk/dafin",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    install_requires=["seaborn", "yfinance>=0.2.31", "scipy"],
    python_requires=">=3.10",
    extras_require={
        "test": [
            "pytest",
            "pytest-cov",
            "pytest-parametrized",
            "pylint",
        ],
    },
)
