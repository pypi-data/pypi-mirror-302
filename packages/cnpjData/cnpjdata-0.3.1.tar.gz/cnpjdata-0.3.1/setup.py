# setup.py

from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="cnpjData",  # Nome do pacote no PyPI
    version="0.3.1",  # Versão inicial
    author="Seu Nome",  # Seu nome
    author_email="seuemail@exemplo.com",  # Seu email
    description="Um pacote para consultar e validar dados de CNPJ utilizando a API pública cnpj.ws",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/seuusuario/cnpjData",  # URL do repositório
    packages=find_packages(),  # Encontrar pacotes automaticamente
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",  # Altere conforme sua licença
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',  # Versão mínima do Python
    install_requires=[
        "requests",  # Dependências necessárias
    ],
    include_package_data=True,  # Incluir arquivos adicionais
    zip_safe=False,
)
