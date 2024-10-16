from setuptools import setup, find_packages

setup(
    name='kg26_excel_writer',
    version='0.2.0',
    packages=find_packages(),
    description='A library to write pandas DataFrames to Excel with formatting',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author='Kiran R Gupta',
    author_email='kiran.rgupta26@gmail.com',
    url='https://github.com/yourusername/excel_writer',  # Replace with your GitHub URL
    classifiers=[
        'Programming Language :: Python :: 3',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
    install_requires=[
        'pandas>=1.0.0',
        'openpyxl>=3.0.0'
    ],
)
