import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="cbim_utils",
    version="0.1.5",
    author_email="m.martinelli@cbim.it",
    description="Various utilities",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    url = 'https://github.com/mmartinelli00/package_cbim.git',
    install_requires=[
        'PyMySQL==1.1.1',
        ],
    extras_require = {
        "dev": ["pytest>=7.0", "twine>=4.0.2"],
    }
)