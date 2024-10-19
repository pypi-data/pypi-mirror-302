from setuptools import setup, find_packages

setup(
    name="csco_tc123",
    version="3.1.0",
    packages=find_packages(),
    install_requires=[
        # Add your dependencies here
    ],
    author="tc123",
    author_email="tc@tc123xyz.com",
    description="tc local package",
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url="https://github.com/tiacui/testrepo1",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
