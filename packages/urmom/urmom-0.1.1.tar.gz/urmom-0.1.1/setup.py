from setuptools import setup, find_packages

setup(
    name="urmom",
    version="0.1.1",
    author="Daniel Merja",
    author_email="danielmerja@gmail.com",
    description="A Python package that prints 'URMOM' in ASCII art.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/danielmerja/urmom",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    entry_points={
        'console_scripts': [
            'urmom=urmom.ascii_art:print_urmom',
        ],
    },
)
