from setuptools import setup, find_packages

setup(
    name='clients_report_gen',
    version='0.1.0',
    author='Plavist Games',
    long_description=open('README.md',encoding='UTF-8').read(),
    long_description_content_type="text/markdown",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
)
