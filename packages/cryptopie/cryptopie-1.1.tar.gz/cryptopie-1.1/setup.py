from setuptools import setup, find_packages

setup(
    name="cryptopie",
    version="1.1",
    packages=find_packages(),
    install_requires=[
        'pycryptodome',
    ],
    author="Dyaksa Jauharuddin Nour",
    author_email="diasnour0395@gmail.com",
    description="cryptopie is library crypto for encrypt data pii",
    long_description=open('README.md').read(),
    long_description_content_type="text/markdown",
    url="https://github.com/dyaksa/cryptopie",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)