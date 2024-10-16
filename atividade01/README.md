# Site dos Anos 2000 de Montadoras de Veículos

Site com construção a molde dos anos 2000, com CRUDs de montadoras, modelos de veículos e veículos, com persistência em banco de dados local.

## Pré-requisitos

- Última versão do Python instalada

## Como instalar os pacotes

- Crie o ambiente virtual para instalação dos pacotes com o comando ```python -m venv .venv```
- Ative o ambiente virtual com o comando:
    - Windows: ```.venv\Scripts\Activate.ps1```
    - Linux: ```source .venv/bin/activate```
- Execute o comando ```pip install fastapi jinja2 uvicorn sqlalchemy sqlmodel python-multipart```

## Como usar

- Crie o servidor com o comando ```uvicorn main:app --reload```
- Entre no link e use as seguintes rotas:
    - CRUD de Montadoras: /montadoras
    - CRUD de Modelos de Veículo: /modelos_veiculo
    - CRUD de Veículos: /veiculos