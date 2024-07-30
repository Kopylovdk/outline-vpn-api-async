# -*-coding:utf-8-*-
"""setup for outline-vpn-api-async"""

from setuptools import setup

setup(
    name="outline-vpn-api-async",
    version="0.0.2",
    packages=["outline_vpn"],
    url="https://github.com/dogekiller21/outline-vpn-api-async",
    license="MIT",
    author="Maxim (dogekiller21) Polyakov",
    author_email="dogekiller21@gmail.com",
    description="Async Python API wrapper for Outline VPN",
    long_description=open("README.md", "r").read(),  # pylint: disable=R1732
    long_description_content_type="text/markdown",
    install_requires=("aiohttp",),
)
