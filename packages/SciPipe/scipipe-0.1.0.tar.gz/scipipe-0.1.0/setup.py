from setuptools import find_packages, setup

setup(
    name="SciPipe",
    version="0.1.0",
    description="A data science and machine learning library that wraps and extends popular tools",  # noqa: E501
    author="Ron Snir",
    author_email="ronsnirmail@gmail.com",
    url="https://github.com/ronsnir/SciPipe",
    packages=find_packages(),  # Automatically find and include packages
    install_requires=[],  # List dependencies here
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)
