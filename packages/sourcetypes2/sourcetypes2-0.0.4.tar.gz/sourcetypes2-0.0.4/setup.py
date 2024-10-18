from setuptools import setup

with open("README.md", "r") as fh:
    long_description = fh.read()
    img_url = "https://raw.githubusercontent.com/jurooravec/python-inline-source-2/main/sourcetypes/docs/examples.png"
    long_description = long_description.replace("(docs/examples.png)", f"({img_url})")

setup(
    name='sourcetypes2',
    version='0.0.4',
    author="Juro Oravec",
    description="Python Source Code Types For Inline Syntax Highlighting",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/jurooravec/python-inline-source-2/tree/main/sourcetypes",
    py_modules=['sourcetypes'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.7',
    install_requires=[
        'typing-extensions>=3.7.4',
    ]
)
