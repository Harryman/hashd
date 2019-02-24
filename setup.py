from setuptools import setup, find_packages
import sys, os

here = os.path.abspath(os.path.dirname(__file__))
README = open(os.path.join(here, "README.md")).read()
NEWS = open(os.path.join(here, "NEWS.txt")).read()


version = "0.1"

install_requires = [
    # List your project dependencies here.
    # For more details, see:
    # http://packages.python.org/distribute/setuptools.html#declaring-dependencies
]


setup(
    name="hashd",
    version=version,
    description="A fully decentralized broadcast system for the based on gossip and proof of work",
    long_description=README + "\n\n" + NEWS,
    classifiers=[
        # TODO Get strings from http://pypi.python.org/pypi?%3Aaction=list_classifiers
    ],
    keywords="database",
    # author="Joe", # TODO
    # author_email="joe@example.org", # TODO
    url="https://hashd.in/",
    # license="MIT", # TODO
    packages=find_packages("hashd"),
    package_dir={"": "hashd"},
    include_package_data=True,
    zip_safe=False,
    install_requires=install_requires,
    # entry_points={"console_scripts": ["hashd:main"]},
)
