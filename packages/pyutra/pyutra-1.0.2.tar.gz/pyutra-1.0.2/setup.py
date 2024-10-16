from setuptools import setup, find_packages

with open('README.md', 'r', encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='pyutra',
    version='1.0.2',
    packages=find_packages(),
    install_requires=[],
    description='A Python library that tries to be a jack of all trades.',
    long_description=long_description,
    long_description_content_type='text/markdown',
    author='TheDiamondOG',
    author_email='thediamondogness@gmail.com',
    url='https://github.com/thediamondog/pyutra',
)
