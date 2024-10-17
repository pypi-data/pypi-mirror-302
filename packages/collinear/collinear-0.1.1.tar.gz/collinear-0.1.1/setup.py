from setuptools import setup, find_packages


setup(
    name = 'collinear',
    version = "0.1.0",
    author = 'Collinear AI',
    author_email = 'info@collinear.ai',
    url = 'https://www.collinear.ai/',
    description = 'Collinear AI Python Client.',
    long_description_content_type = "text/x-rst",  # If this causes a warning, upgrade your setuptools package
    license = "MIT license",
    packages = find_packages(exclude=["test"]),  # Don't include test directory in binary distribution
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ]  # Update these accordingly
)
