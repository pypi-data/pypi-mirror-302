from setuptools import find_packages, setup
from setuptools.config.expand import entry_points

setup(
    name='ranver_business_metrics',
    description='calculate roi',
    version='0.1.0',
    py_modules=['business_metrics'],
    entry_points={
        'console_scripts': [
            'business-metrics = business_metrics:main'
        ]
    },
)