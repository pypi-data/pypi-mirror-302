from setuptools import setup, find_packages

setup(
    name='sky_factorial',
    version='0.2',
    packages=find_packages(),
    install_requires=[
        # Add any dependencies you need here
    ],
    entry_points={
        'console_scripts': [
            'sky-factorial = sky_factorial:factorial',
        ],
    },
)