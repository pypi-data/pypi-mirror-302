import os

from setuptools import setup

with open(os.path.join(os.getcwd(), "requirements.txt")) as f:
    required = f.read().splitlines()
with open("./VERSION") as version_file:
    version = version_file.read()
setup(
    name="croudtech-bootstrap",
    version=version.strip(),
    install_requires=required,
    setup_requires=["setuptools_scm"],
    include_package_data=True,
)
