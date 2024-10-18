from setuptools import setup, find_packages

setup(
    name='InfoGerm',
    version='0.0.2',
    packages=find_packages(),
    install_requires=[

    ],
    entry_points={
        "console_scripts":[
            "infogerm-hello=InfoGerm:hello",
            "infogerm-intro=InfoGerm:intro",
        ],
    },
)