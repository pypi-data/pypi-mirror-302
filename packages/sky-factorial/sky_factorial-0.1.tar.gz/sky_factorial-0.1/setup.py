from setuptools import setup, find_packages

setup(
    name='sky_factorial',
    version='0.1',
    packages=find_packages(),
    install_requires=[
        # Add any dependencies you need here
    ]
)

setup(
    entry_points={
        'console_scripts': [
            'sky-factorial = sky_factorial:factorial',
        ],
    },
)