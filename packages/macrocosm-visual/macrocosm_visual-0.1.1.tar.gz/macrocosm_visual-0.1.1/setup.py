from os.path import abspath, dirname, join

from setuptools import find_packages, setup

this_dir = abspath(dirname(__file__))

with open(join(this_dir, "README.md"), encoding="utf-8") as file:
    long_description = file.read()

with open(join(this_dir, "requirements.txt")) as f:
    requirements = f.read().split("\n")

setup(
    name="macrocosm-visual",
    version="0.1.1",
    description="Macrocosm Visual Engine",
    url="https://github.com/macro-cosm/macrocosm-visual",
    long_description_content_type="text/markdown",
    long_description=long_description,
    author="Macrocosm",
    author_email="luca.mungo@macrocosm.group",
    license="MIT",
    install_requires=requirements,
    packages=find_packages(exclude=["docs"]),
    include_package_data=True,
)
