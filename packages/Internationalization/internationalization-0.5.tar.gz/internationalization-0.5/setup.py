from setuptools import setup, find_packages

def read_file(file_name):
    with open(file_name, 'r', encoding='utf-8') as file:
        return file.read()

setup(
    name='Internationalization', 
    version='0.5',
    packages=find_packages(include=['library', 'library.*']),  # Include the library package and sub-packages
    install_requires=[],  
    long_description=read_file('README.md'),  
    long_description_content_type='text/markdown',
    include_package_data=True,  # This line includes non-Python files
    package_data={
        'library.QTLauncher': ['*.json'],  # Adjusted to point to the QTLauncher directory
    },
)
