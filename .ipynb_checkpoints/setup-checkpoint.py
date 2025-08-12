from setuptools import setup

setup(
    name='leavitt_law_calibration',
    version='1.0',
    packages=['my_package'],
    install_requires=[matplotlib, pandas, numpy, scipy, seaborn],
    author='Shubham Mamgain',
    author_email='smamgain@aip.de',
    description='Calibrates Leavitt Law if multiband luminosity of Cepheids are given along with their distances and reddenings.'
)
