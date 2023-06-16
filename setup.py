from setuptools import setup


setup(
        name='mdt',
        version='1.0.1',
        py_modules=['mdt'],
        packages=['modules'],
        license='MIT',
        install_requires=['PyYAML==6.0', 'click==8.1.3', 'boto3==1.26.71', 'botocore==1.29.93', 'requests==2.28.2', 'pytest==7.3.1'],
        entry_points={
            "console_scripts": ['mdt = mdt:run']
        },
        python_requires=">=3.6",
)
