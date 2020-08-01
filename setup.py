import setuptools

setuptools.setup(
    name = "poetic",
    version = "1.0.0-Beta",
    url = "https://github.com/kevin931/poetic",
    author = "Kevin Wang",
    author_email = "bridgemarian@gmail.com",
    description = "Predicts how poetic sentences are.",
    long_description = open("README.md").read(),
    packages=["poetic"],
    install_requires = ["tensorflow>=2.1",
                        "gensim>=1.18",
                        "nltk>=3.8"
    ],
    data_files = [("data", ["word_dictionary_complete.txt"])],
    classifiers = [
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3 :: Only"
    ]
)