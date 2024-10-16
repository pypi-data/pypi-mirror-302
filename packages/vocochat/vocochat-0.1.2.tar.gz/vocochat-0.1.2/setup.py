
from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="vocochat",
    version="0.1.2",
    author="Tom Sapletta",
    author_email="info@softreck.dev", 
    description="",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://python.dobyemail.com",
    packages=find_packages(where="src"),    
    package_dir={"": "src"},
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: Apache Software License", 
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
    ],    
    install_requires=[
        # Add your project dependencies here
    ],
    entry_points={
        'console_scripts': [
            'vocochat=vocochat.vocochat:main',
        ],
    },
)
