# Documentação do Integrador Omie

## Dependencias
A única dependencia necessária é a biblioteca [zeep](https://docs.python-zeep.org/en/master/index.html), que é usada para criar os clientes SOAP. 

## Autenticação

Para autenticar na API do Omie, você precisa fornecer uma `app_key` e um (`app_secret`). Esse dados são obtidos no site da [omie](https://developer.omie.com.br/).

```python
import os

from omie_py.client import OmieClient

key = os.getenv('OMIE_APP_KEY')
secret = os.getenv('OMIE_APP_SECRET')
client = OmieClient(key, secret)
```

## Usar métodos das API

A Omie disponibiliza várias APIs e o cliente recebe uma chamada e verifica em qual API o método está disponível e executa a chamada. O mesmo vale para os tipos disponibilizados na API.

Para verificar os métodos e tipos disponiveis o [site da API](https://developer.omie.com.br/service-list/) deve ser usado.

Os tipos oferecem validação de campos e tipos.

Exemplo para listar departamentos.

```python
departamento_listar_request = client.get_type('departamento_listar_request')

response_pages = client.execute_call("ListarDepartamentos", departamento_listar_request(**{
  "pagina": 1,
  "registros_por_pagina": 20,
}), True)

for response in response_pages:
    print(response)
```

### Métodos principais do cliente

- `execute_call(method_name: str, params: dict, is_paginated: bool = False)`: Executa uma chamada à API.
- `get_type(type_name)`: Obtém um tipo específico para ser usado nas requisições.

### Classe PaginatedResponse

Quando o `is_paginated` é passado como `True` para o método execute_call, o retorno é um `Iterable` que faz as chamadas subsequentes para o método.

### Rate limit
A API atualmente limite a 4 req/s e o projeto não gerencia isso.

[Mais informações](https://ajuda.omie.com.br/pt-BR/articles/8112984-limites-de-consumo-da-api-do-omie).