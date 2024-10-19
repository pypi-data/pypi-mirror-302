from setuptools import setup, find_packages

setup(
    name="internet-eng-znu",
    version="0.1.10",
    author="Ali Safapour",
    author_email="thisisalinton@gmail.com",
    description="Deploy your projects on the ZNU server.",
    packages=find_packages(),
    package_data={
        "internet_eng_znu": ["public_key.pem"],
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: Other/Proprietary License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.10',
    entry_points={
        "console_scripts": [
            "internet-eng-znu=internet_eng_znu.main:app",
        ],
    },
)

