import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="win10notify",
    version="0.0.5",
    author="phrasek",
    author_email="64117215+phrasek@users.noreply.github.com",
    description="A library to create Windows 10 Toast Notifications",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/phrasek/win10notify",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: Microsoft :: Windows :: Windows 10",
    ],
    python_requires=">=3.6",
)
