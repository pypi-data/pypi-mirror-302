from setuptools import setup, find_packages

setup(
    name='finance_calc',
    version='0.5.0',
    author='Plavist Games',
    long_description=open('README.md',encoding='UTF-8').read(),
    long_description_content_type="text/markdown",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
)
