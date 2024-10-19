from setuptools import setup, find_packages
from pathlib import Path

this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text(encoding="utf-8")

setup(
    name='binaexperts',  # Package name
    version='0.4.0',  # Version number
    description='A dataset conversion SDK for different Computer Vision formats',
    long_description=long_description,
    long_description_content_type="text/markdown",
    author='Nastaran Dab',
    author_email='n.dab@binaexperts.com',
    license="MIT",
    packages=find_packages(),  # Automatically find and include all packages
    include_package_data=True,
    package_data={
            'binaexperts': ['schema/*.json'],
        },
    install_requires=[  # List dependencies here
        'PyYAML',
        'requests',
        'jsonschema',
        'opencv-python',
        'numpy'
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',  # Minimum Python version
)
