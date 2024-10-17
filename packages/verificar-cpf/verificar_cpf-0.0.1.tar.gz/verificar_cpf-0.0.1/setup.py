from setuptools import setup, find_packages

with open("README.md", "r") as f:
    page_description = f.read()


setup(
    name="verificar_cpf",
    version="0.0.1",
    author="Leonardo Diniz",
    description="Verifica se o número do CPF é válido",
    long_description=page_description,
    long_description_content_type="text/markdown",
    packages=find_packages(),
    python_requires='>=3.8',
)