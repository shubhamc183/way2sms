"""
Way2sms
"""

import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="sch-way2sms",
    version="0.0.1",
    author="Shubham Choudhary",
    author_email="shubhamc183@gmail.com",
    description="Send free sms WAY2SMS",
    long_description="Way2sms, 2 free messages per day in India",
    long_description_content_type="text/markdown",
    url="https://github.com/shubhamc183/way2sms",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    install_requires=[
        'beautifulsoup4',
        'requests'
    ]
)
