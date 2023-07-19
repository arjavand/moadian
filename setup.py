from setuptools import setup, find_packages

with open("README.md", "r") as f:
    long_description = f.read()

setup(
    name="moadian",
    version="1.0.1",
    author="Masoud Taee (Technical Team Lead at Arjavand Co.)",
    author_email="mmtaee64@gmail.com",
    description="Moadian (Iranian Tax) API service to handle invoices",
    long_description=long_description,
    data_files=[(".", ["LICENSE"])],
    long_description_content_type="text/markdown",
    url="https://github.com/arjavand/moadian",
    project_urls={
        "Bug Tracker": "https://github.com/arjavand/moadian/issues",
        "Repository": "https://github.com/arjavand/moadian",
    },
    classifiers=[
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent",
    ],
    packages=find_packages(),
    python_requires=">=3.7",
    install_requires=[
        "setuptools>=59",
        "wheel",
        "certifi==2023.5.7",
        "cffi==1.15.1",
        "charset-normalizer==3.2.0",
        "cryptography==41.0.1",
        "idna==3.4",
        "pycparser==2.21",
        "pycryptodome==3.18.0",
        "requests==2.31.0",
        "urllib3==2.0.3",
    ],
)

# python3 setup.py sdist bdist_wheel
# python3 -m build
