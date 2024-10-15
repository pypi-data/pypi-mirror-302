from setuptools import setup, find_packages

setup(
    name="harish_daga",  # Package name
    version="0.0.2",  # Version of the package
    author="Harish Daga",
    author_email="theharishdaga@gmail.com",
    description="A simple module for testing",
    packages=find_packages(),  # Automatically finds packages in the folder
    install_requires=[],  # Required external packages
    classifiers=[
        "Programming Language :: Python :: 3"
    ],
    python_requires='>=3',
)
