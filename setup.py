from setuptools import setup, find_packages
import sys, os

here = os.path.abspath(os.path.dirname(__file__))
README = open(os.path.join(here, "README.md")).read()
NEWS = open(os.path.join(here, "NEWS.txt")).read()


version = "0.1"

install_requires = ["mnemonic==0.18", "ecdsa==0.13"]


setup(
    name="hashd",
    version=version,
    description="A fully decentralized authenticated broadcast/discovery system based on gossip and proof of work",
    long_description=README + "\n\n" + NEWS,
    classifiers=[
        # Get strings from http://pypi.python.org/pypi?%3Aaction=list_classifiers
        "Topic :: Security :: Cryptography"
    ],
    keywords="database, identity, discovery",
    # author="Joe", # TODO
    # author_email="joe@example.org", # TODO
    url="https://hashd.in/",
    # license="MIT", # TODO
    packages=find_packages("hashd"),
    package_dir={"": "hashd"},
    include_package_data=True,
    zip_safe=False,
    install_requires=install_requires,
)
