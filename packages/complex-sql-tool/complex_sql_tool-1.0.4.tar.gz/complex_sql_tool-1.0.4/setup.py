from setuptools import setup, find_packages

setup(
    name='complex_sql_tool',
    version='1.0.4',
    packages=find_packages(),
    install_requires=[
        'black>=23.3.0',
        'fpdf>=1.7.2',
        'matplotlib>=3.5.3',
        'pytest>=5.4.0',
        'ruff>=0.6.5',
        'jupyter>=1.1.1',
        'nbval>=0.11.0',
        'polars-lts-cpu>=0.18.4',
        'mysql-connector-python>=8.0.0',
        'tabulate>=0.8.0',
        'python-dotenv>=1.0.0',
        'pandas>=2.0.0'
    ],
    entry_points={
        'console_scripts': [
            'complex_sql_tool=mylib.main:main',
        ],
    },
    author='Hongji',
    description='A toy tool for IDS706 to run complex SQL with external MYSQL database.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/nogibjj/IDS706_package_python_CLI',
)