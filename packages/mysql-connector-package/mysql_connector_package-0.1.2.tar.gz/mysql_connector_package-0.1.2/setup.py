from setuptools import setup, find_packages

setup(
    name="mysql-connector-package",  # Package name
    version="0.1.2",  # Version of the package
    author="Harish Daga",
    author_email="theharishdaga@gmail.com",
    description="A simple MySQL connector using pymysql",
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url="https://github.com/Harishdaga/mysql-connector-package",  # GitHub URL
    packages=find_packages(),  # Automatically finds packages in the folder
    install_requires=['pymysql'],  # Required external packages
    classifiers=[
        "Programming Language :: Python :: 3"
    ],
    python_requires='>=3',
)
