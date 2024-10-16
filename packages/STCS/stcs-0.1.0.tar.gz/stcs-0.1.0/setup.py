from setuptools import setup

setup(
    name="STCS",
    version="0.1.0",
    description="The Standardized Time and Calendar System (STCS) is a system which replaces the traditional time and calendar systems to make them more intuitive and decimalized.",
    url="https://github.com/LiamSpatola/STCS",
    author="Liam Spatola",
    license="GNU GPLv3",
    packages=["stcs"],
    install_requires=["typer==0.12.5"],
)
