from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="fastCodePrompts",
    version="0.1.3",  # Incrementar a versão
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
        "certifi",
        "charset-normalizer",
        "docutils",
        "idna",
        "importlib_metadata",
        'jaraco.classes',
        "jaraco.context",
        "jaraco.functools",
        "keyring",
        "markdown-it-py",
        "mdurl",
        "more-itertools",
        "nh3",
        "pkginfo",
        "Pygments",
        "pyperclip",
        "PyQt5",
        "PyQt5-Qt5",
        "PyQt5_sip",
        "pywin32-ctypes",
        "PyYAML",
        "readme_renderer",
        "requests",
        "requests-toolbelt",
        "rfc3986",
        "rich",
        "setuptools",
        "twine",
        "urllib3",
        "zipp"
    ],
)
