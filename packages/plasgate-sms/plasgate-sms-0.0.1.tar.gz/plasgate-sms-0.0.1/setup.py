from setuptools import setup, find_packages

with open("README.md") as f:
    long_description = f.read()

# To install the twilio-python library, open a Terminal shell, then run this
# file by typing:
#
# python setup.py install
#
# You need to have the setuptools module installed. Try reading the setuptools
# documentation: http://pypi.python.org/pypi/setuptools

setup(
    name="plasgate-sms",
    version="0.0.1",
    description="Plasgate SMS API client",
    author="PlasgateCoLtd",
    help_center="https://plasgate.com/contact",
    url="https://github.com/plasgateCoLTD/python",
    keywords=["plasgate", "sms-api", "plasgate-otp"],
    python_requires=">=3.7.0",
    install_requires=[
        "requests >= 2.0.0",
        "aiohttp>=3.8.4",
        "aiohttp-retry>=2.8.3",
        "marshmallow>=3.22.0",
    ],
    packages=find_packages(exclude=["tests", "tests.*"]),
    include_package_data=True,
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: Implementation :: CPython",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Communications :: Telephony",
    ],
    long_description=long_description,
    long_description_content_type="text/markdown",
)
