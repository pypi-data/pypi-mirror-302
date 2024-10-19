from setuptools import setup, find_packages

setup(
    name="biocomp",
    version="0.2.3",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    install_requires=[

    ],
    entry_points={
        "console_scripts": [
            "biocomp=biocomp.biocomp:main",
        ],
    },
    author="Tom Sapletta",
    author_email="info@softreck.dev",
    description="BioComp  'Coded Life' to propozycja języka domenowo-specyficznego (DSL) do edukacji i wdrażania biocomputingu ",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://www.biokomputer.pl",
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
)
