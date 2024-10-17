from setuptools import setup, find_packages


setup(
    name='csa_common_lib_alpha',
    version="0.1",
    packages=find_packages(include=['csa_common_lib', 'csa_common_lib.*'])
)