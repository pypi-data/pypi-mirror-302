from setuptools import find_packages, setup

with open("./README.md", "r") as f:
    long_description = f.read()

setup(
    name="new_logicsdk",
    version="0.0.1",
    description="An avahiai library which makes your Gen-AI tasks effortless",
    # package_dir={"": "logicsdk"},
    packages=find_packages(),
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/avahi-org/logicai.git",
    author="Avahi AWS",
    author_email="info@avahitech.com",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.9",
        "Operating System :: OS Independent",
    ],
    install_requires=["boto3>=1.34.160", "loguru>=0.7.2", "python-docx>=1.1.2", "PyMuPDF>=1.24.9"],
    extras_require={
        "dev": ["twine>=4.0.2"],
    },
    python_requires=">=3.9",
)