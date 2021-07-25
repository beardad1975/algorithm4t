import setuptools

# with open("README.md", "r",encoding="utf8") as fh:
#     long_description = fh.read()

setuptools.setup(
    name="algorithm4t",
    version="0.0.1",
    author="Wen-Hung, Chang 張文宏",
    author_email="beardad1975@nmes.tyc.edu.tw",
    description="algorithm modules for Teenagers",
    long_description="algorithm modules for Teenagers",
    long_description_content_type="text/markdown",
    url="https://github.com/beardad1975/algorithm4t",
    #packages=setuptools.find_packages(),
    platforms=["Windows"],
    python_requires=">=3.5",
    packages=['algorithm4t','演算法'],
    install_requires = ['pillow'],
    package_data={'algorithm4t': ['images/*'],
                },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: Microsoft :: Windows",
        #"Operating System :: MacOS",
        #"Operating System :: POSIX :: Linux",
        "Natural Language :: Chinese (Traditional)",
    ],
)