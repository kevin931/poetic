import setuptools

description = "For documentation and detials, "
description += "please refer to http://github.com/kevin931/poetic"

setuptools.setup(
    name = "poetic-py",
    version = "1.0.0b1",
    url = "https://github.com/kevin931/poetic",
    author = "Kevin Wang",
    author_email = "bridgemarian@gmail.com",
    description = "Predicts how poetic sentences are.",
    long_description = description,
    packages=["poetic"],
    install_requires = ["tensorflow>=2.1",
                        "gensim>=3.8",
                        "nltk>=3.4"
    ],
    install_package_data=True,
    package_data={"poetic":["*.txt"]},
    classifiers = [
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3 :: Only"
    ]
)