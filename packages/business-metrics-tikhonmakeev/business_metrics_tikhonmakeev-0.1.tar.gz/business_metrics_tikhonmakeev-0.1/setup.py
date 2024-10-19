from setuptools import setup

setup(
    name='business_metrics_tikhonmakeev',
    version='0.1',
    py_modules=['business_metrics'],
    entry_points={
        'console_scripts': [
            'business_metrics = business_metrics:main'
        ]
    }
)