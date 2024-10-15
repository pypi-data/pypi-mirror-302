import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="example-pkg-dldb-pd-columns",
    version="0.0.2",
    author="yakilee",
    author_email="yakilee@gmail.com",
    description="dldbcosmos sample lib",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/dldbcosmos/python-tutorials",
    project_urls={
        "Bug Tracker": "https://github.com/dldbcosmos/python-tutorials/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    python_requires=">=3.6",
)
