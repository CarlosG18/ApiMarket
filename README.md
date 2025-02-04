# ApiMarket

> Este repositório contém uma API desenvolvida com **Django REST Framework (DRF)**. A API oferece funcionalidades para simular um sistema de supermercado simples, com funcionalidades basicas encontradas nesse meio.

## **Visão Geral**
Esta API permite a criação, leitura, atualização e exclusão (CRUD) de recursos como **usuários**, **Lista de compras** e **batida de ponto dos funcionarios**. Ela usa Django como o framework back-end e o Django REST Framework (DRF) para expor os recursos como endpoints HTTP RESTful.

## ⚙️ **Tecnologias Utilizadas**
![django-logo](https://img.shields.io/badge/django_5.1.4-green?style=for-the-badge&logo=django&logoColor=white&labelColor=green)
![drf-logo](https://img.shields.io/badge/DRF_3.15.2-green?style=for-the-badge&logo=django&logoColor=white&labelColor=green)
![postgress-logo](https://img.shields.io/badge/postgress-blue?style=for-the-badge&logo=postgresql&logoColor=white&labelColor=blue)
![docker-logo](https://img.shields.io/badge/docker-blue?style=for-the-badge&logo=docker&logoColor=white&labelColor=blue)

## 📌 Detalhes sobre a API

### ⏰ Batida de Ponto do Funcionário
- Endpoint para registrar as horas trabalhadas com a batida do ponto. O esquema abaixo mostra a estrategia utilizada:

![esquema de registro de ponto](./docs/imgs/esquema_de_ponto.png)

### 📦 Estoque de Produtos
- Endpoint para consultar e gerenciar o estoque de produtos disponíveis.

### 🛍️ Lista de Compras do Cliente
- Endpoint para visualizar e atualizar as compras feitas por um cliente, onde a cada item alocado o estoque é diretamente influenciado, sendo atualizado os dados.

## 🛠️ **Instalação e Configuração**

### **Pré-requisitos**
1. Python 3.12.7 instalado
2. Docker (se for usar o contêiner)
3. Acesso ao banco de dados (se necessário) como PostgreSQL ou outro.

### **Instalação**
Clone o repositório:
```bash
git clone https://github.com/usuario/repo.git
cd repo
```

Crie um ambiente virtual e ative-o:
```bash
python3 -m venv venv
source venv/bin/activate  # Para Linux/Mac
venv\Scripts\activate     # Para Windows
```

Instale as dependências:
```bash
pip install -r requirements.txt
```

### ➡️ **Configuração do Banco de Dados**
Configure as variáveis de ambiente para o banco de dados (no arquivo `.env` ou diretamente no `settings.py`).

Exemplo de configuração:
```plaintext
DATABASE_URL=postgres://usuario:senha@localhost:5432/nomedobanco
```

### ➡️ **Rodar as Migrações**
```bash
python manage.py migrate
```

### ➡️ **Rodar o Servidor**
Inicie o servidor de desenvolvimento:
```bash
python manage.py runserver
```

### ➡️ **Usando Docker**
Se preferir usar o Docker para rodar a aplicação, pode construir e iniciar os containers:

**Buildando a imagem**:
```bash
docker image build . -t <crie um nome para a imagem>
```

**Criando o container**:
```bash
docker run -p 8000:8000 <nome que voce deu para a imagem>
```

com isso a api vai esta acessivel em **127.0.0.1:8000**.

## 🗎 **Endpoints da API e Documentação**

A documentação da API pode ser acessada atraves da url `127.0.0.1:8000/docs`, onde conterá todos os endpoints e todas as informações nescessarias para se fazer a requisição da forma correta.

