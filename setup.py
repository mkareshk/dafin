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
    install_requires=[
        "seaborn>=0.11.2",
        "yfinance>=0.1.68",
    ],
    tests_require=["pytest"],
    python_requires=">=3.8",
)
