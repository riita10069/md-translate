from setuptools import setup


setup(
        name='mdt',
        version='2.0.0',
        py_modules=['mdt'],
        packages=['modules'],
        license='MIT',
        install_requires=['PyYAML==6.0', 'click==8.1.3', 'boto3==1.29.6', 'botocore==1.32.6', 'requests==2.28.2', 'pytest==7.3.1', 'beautifulsoup4==4.12.2'],
        entry_points={
            "console_scripts": ['mdt = mdt:run']
        },
        python_requires=">=3.6",
)
