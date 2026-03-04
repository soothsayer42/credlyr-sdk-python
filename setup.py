from setuptools import setup, find_packages

setup(
    name="credlyr",
    version="1.0.0",
    packages=find_packages(),
    python_requires=">=3.8",
    install_requires=[
        "httpx>=0.24.0",
    ],
    author="Credlyr",
    author_email="support@credlyr.com",
    description="Official Python SDK for the Credlyr API",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/credlyr/sdk-python",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
