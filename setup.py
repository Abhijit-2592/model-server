import setuptools
import model_server

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

with open("requirements.txt", "r") as f:
    requirements = f.read()

requirements = requirements.split("\n")
requirements = list(filter(lambda x: False if x == "" else True, requirements))

setuptools.setup(
    name=model_server.__title__,
    version=model_server.__version__,
    author=model_server.__author__,
    author_email=model_server.__email__,
    description=model_server.__summary__,
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Abhijit-2592/model-server",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=requirements
)
