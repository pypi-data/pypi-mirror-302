from setuptools import setup, find_packages

setup(
    name="rnl-edge-sdk",
    version="1.0.0",
    packages=find_packages(),
    install_requires=[
        "requests>=2.26.0",
    ],
    author="Baby Manisha Sunkara",
    author_email="babymaneesha@gmail.com",
    description="Python SDK for RNL Edge API",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/ruffalo-noel-levitz/ai-rnl-edge-api/tree/master/rnl-edge-sdk/rnl-edge-sdk-python",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)