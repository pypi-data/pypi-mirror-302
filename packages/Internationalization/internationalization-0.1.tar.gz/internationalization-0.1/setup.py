from setuptools import setup, find_packages

def read_file(file_name):
    with open(file_name, 'r', encoding='utf-8') as file:
        return file.read()

setup(
    name='Internationalization', 
    version='0.1',
    packages=find_packages(),
    install_requires=[],  
    long_description=read_file('README.md'),  # Add this line
    long_description_content_type='text/markdown',  # Add this line
)