from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="cnpjData",
    version="0.3.2",
    author="Hilton Queiroz Rebello",
    author_email="rebello.hiltonqueiroz@gmail.com",
    description="Consulta de dados de empresas através do CNPJ",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/hqr90/cnpjData",  # URL do repositório
    packages=find_packages(include=["CNPJAPIClient", "cnpjData.*"]),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    include_package_data=True,  # Inclui arquivos especificados no MANIFEST.in
    python_requires='>=3.8',
    install_requires=[
        "requests"
    ],
    entry_points={
        'console_scripts': [
            'cnpjData=cnpjData.client:main',
        ],
    },
)
