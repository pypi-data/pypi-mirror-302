from setuptools import setup, find_packages

setup(
    name='gadgetlib',
    version='0.1',
    description='GadgetLab automation tools.',
    author='Kyle Dvorak',
    packages=find_packages(),
    install_requires=[
        'requests',
    ]
)