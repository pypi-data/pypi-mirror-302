from setuptools import setup, find_packages

setup(
    name='finance_calc',
    version='0.4.0',
    packages=find_packages(where="src"),
    package_dir={"": "src"},
)
