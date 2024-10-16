"""Studio setup file."""

from setuptools import find_packages, setup  # type: ignore


VERSION = "0.0.1"

setup(
    name="jac-studio",
    version=VERSION,
    packages=find_packages(include=["jac-studio", "jac-studio.*"]),
    install_requires=[
        "jaclang~=0.7.24",
        "jac-cloud~=0.1.5"
    ],
    include_package_data=True,
    entry_points={
        "jac": ["create_cmd = jac_studio.cli:JacCmd"],
    },
    author="TrueSelph Inc.",
    author_email="admin@trueselph.com",
    url="https://trueselph.com/",
)
