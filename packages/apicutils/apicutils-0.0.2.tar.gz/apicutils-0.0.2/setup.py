from setuptools import setup

long_description = "".join(
    [
        "Miscellaneous functions shared between packages"
    ]
)

setup(
    name="apicutils",
    version="0.0.2",
    author="Antoine Picard-Weibel",
    author_email="apicard.w@gmail.com",
    description="personal misc functions",
    long_description=long_description,
    packages=["apicutils"],
    package_dir={"apicutils": "apicutils"},
    install_requires=[
        "pandas",
        "numpy<=1.26",
        "multiprocess>=0.70",
    ],
    python_requires=">=3.9",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
