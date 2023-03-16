from setuptools import setup


setup(
        name='md-translate',
        version='1.0.0',
        install_requires=['PyYAML==6.0', 'click==8.1.3', 'boto3==1.26.71'],
        entry_points={
            "console_scripts": ['mdt = cmd:main']
        }
)
