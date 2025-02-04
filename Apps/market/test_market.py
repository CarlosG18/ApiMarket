import pytest
from rest_framework.test import APIClient
from django.contrib.auth import get_user_model

User = get_user_model()

@pytest.mark.django_db
def test_listar_objetos():
    # Cria o usuário com todos os campos obrigatórios
    user = User.objects.create_user(
        username="operator",  # Campo obrigatório
        email="operator@example.com",
        password="operator",
        hours_worked=268,  # Campos extras do seu modelo
        salario=9979
    )

    client = APIClient()
    url_token = "/api/token/"  # Use caminhos relativos, não URLs absolutas
    url_stocks = "/categorys/"

    payload = {
        "email": "operator@example.com",
        "password": "operator"
    }

    response_credentials = client.post(url_token, data=payload)
    print("Resposta do Token:", response_credentials.status_code, response_credentials.data)
    
    assert response_credentials.status_code == 200, f"Erro na autenticação: {response_credentials.data}"
    
    token = response_credentials.data["access"]
    client.credentials(HTTP_AUTHORIZATION=f"Bearer {token}")

    response = client.get(url_stocks)
    print("Resposta da listagem:", response.status_code, response.data)
    
    assert response.status_code == 200