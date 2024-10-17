from setuptools import setup, find_packages

setup(
    name="devs_tracelogger",
    version="0.1.0",
    author="Gelson Júnior",
    author_email="gelson.junior@grupobachega.com.br",
    description="Uma biblioteca de logger que envia mensagens para o Discord",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/originalprecatorios/tracelogger",
    packages=find_packages(),
    install_requires=[
        "requests"
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
