# =============================================================================
# Pacotes
# =============================================================================
import os
import sys
from setuptools import setup, find_packages

# =============================================================================
# Leitura de termos e requirements
# =============================================================================
def read_terms():
    with open('TERMO_DE_USO.txt', 'r', encoding='utf-8') as f:
        terms = f.read()
    print(terms)

    # Simular entrada para teste
    response = 's'  # ou 'n' para simular "não"
    
    # Se você precisar da entrada do usuário, descomente a linha abaixo
    # response = input("Você concorda com os termos? (s/n): ").strip().lower()

    if response in ['s', 'sim']:
        print("Você concordou com os termos.")
    elif response in ['n', 'não']:
        print("Instalação cancelada.")
        sys.exit(1)
    else:
        print("Resposta inválida. Por favor, responda com 's' ou 'n'.")

# Lê e exibe os termos antes de continuar
read_terms()

def read_requirements():
    return [
        # ... (suas dependências)
        'spacy',
    ]

def read_readme():
    with open('README.md', 'r', encoding='utf-8') as f:
        return f.read()

# =============================================================================
# Setup
# =============================================================================
setup(
    name='leitor_pdf_sensivel',
    version='1.0',
    packages=find_packages(where='src'),
    package_dir={'': 'src'},
    include_package_data=True,
    package_data={
        'leitor_pdf_sensivel': [
            'data/*.xlsx',           # Inclui arquivos .xlsx da pasta data
            'pt_core_news_lg-3.7.0/*'  # Inclui todos os arquivos da pasta pt_core_news_lg-3.7.0
        ],  
    },
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
    python_requires='>=3.6',
    install_requires=read_requirements(),  # Lê as dependências do projeto
    long_description=read_readme(),  # Lê o README para a descrição longa
    long_description_content_type='text/markdown',  # Especifica o formato do README
)
