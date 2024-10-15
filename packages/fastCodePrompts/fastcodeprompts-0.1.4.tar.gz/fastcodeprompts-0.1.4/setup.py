from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="fastCodePrompts",
    version="0.1.4",  # Incrementar a versão
    author="Hilton Queiroz Rebello",
    author_email="rebello.hiltonqueiroz@gmail.com",
    description="Pegar códigos python e inserir no contexto de um prompt",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/hqr90/fastCodePrompts",
    packages=["fastCodePrompts"],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    license="MIT",
    include_package_data=True,
    python_requires='>=3.8',
    install_requires=[
        "pyperclip",
        "argparse",
        "PyQt5"
    ],
)
