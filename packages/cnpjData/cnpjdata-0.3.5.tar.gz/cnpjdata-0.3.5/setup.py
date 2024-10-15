from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="cnpjData",
    version="0.3.5",  # Incrementar a versão
    author="Hilton Queiroz Rebello",
    author_email="rebello.hiltonqueiroz@gmail.com",
    description="Consulta de dados de empresas através do CNPJ",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/hqr90/cnpjData",
    packages=["cnpjData"],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    license="MIT",
    include_package_data=True,
    python_requires='>=3.8',
    install_requires=[
        "requests"
    ],
)
