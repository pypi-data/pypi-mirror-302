# cnpjData

![License](https://img.shields.io/badge/license-MIT-blue.svg)
![PyPI - Version](https://img.shields.io/pypi/v/cnpjData)
![PyPI - Python Version](https://img.shields.io/pypi/pyversions/cnpjData)

**cnpjData** é uma biblioteca Python robusta e fácil de usar para consultar informações de CNPJ e validar inscrições no SUFRAMA utilizando a API Pública de CNPJ. Ela gerencia automaticamente os limites de requisições para evitar exceder as restrições da API, garantindo consultas eficientes e seguras.

## 📝 Índice

- [🔍 Visão Geral](#-visão-geral)
- [🚀 Funcionalidades](#-funcionalidades)
- [📦 Instalação](#-instalação)
- [🛠️ Uso](#️-uso)
  - [Consultar CNPJ](#consultar-cnpj)
  - [Validar Inscrição no SUFRAMA](#validar-inscrição-no-suframa)
- [⚙️ API Reference](#️-api-reference)
  - [CNPJAPIClient](#cnpjapiclient)
    - [consultar_cnpj(cnpj: str) -> dict](#consultar_cnpjcnpj-str--dict)
    - [validar_inscricao_suframa(cnpj: str, inscricao: str) -> dict](#validar_inscricao_suframacnpj-str-inscricao-str--dict)
- [🔒 Tratamento de Erros](#-tratamento-de-erros)
- [📈 Limitações](#-limitações)
- [🧪 Testes](#-testes)
- [🤝 Contribuição](#-contribuição)
- [📄 Licença](#-licença)
- [👤 Autor](#-autor)

## 🔍 Visão Geral

A API Pública de CNPJ permite realizar consultas de informações empresariais e validar inscrições no SUFRAMA. Com o `cnpjData`, você pode integrar facilmente essas funcionalidades em seus projetos Python, mantendo-se dentro dos limites de requisição estabelecidos pela API.

## 🚀 Funcionalidades

- **Consultar CNPJ:** Obtém informações detalhadas sobre um CNPJ específico.
- **Validar Inscrição no SUFRAMA:** Verifica a validade de uma inscrição no SUFRAMA para um determinado CNPJ.
- **Gerenciamento Automático de Limites de Requisições:** Controla o número de requisições para evitar exceder os limites da API.
- **Tratamento de Erros Personalizado:** Lida com respostas de erro, como limites excedidos, de forma elegante.
- **Fácil Integração:** Interfaces simples e intuitivas para facilitar o uso.

## 📦 Instalação

Você pode instalar a biblioteca diretamente do PyPI utilizando o `pip`:

```bash
pip install cnpjData
```

Ou instalar a partir do repositório GitHub:

```bash
pip install git+https://github.com/hqr90/cnpjData.git
```

### Pré-requisitos

- **Python 3.8 ou superior**
- **Biblioteca `requests`** (instalada automaticamente com o `cnpjData`)

## 🛠️ Uso

### Consultar CNPJ

Consulte informações detalhadas sobre um CNPJ específico.

```python
from cnpjData import CNPJAPIClient

# Inicialize o cliente
client = CNPJAPIClient()

# Consulte o CNPJ
cnpj_info = client.consultar_cnpj("27865757000102")

# Exiba as informações
print(cnpj_info)
```

### Validar Inscrição no SUFRAMA

Verifique a validade de uma inscrição no SUFRAMA para um determinado CNPJ.

```python
from cnpjData import CNPJAPIClient

# Inicialize o cliente
client = CNPJAPIClient()

# Valide a inscrição no SUFRAMA
suframa_info = client.validar_inscricao_suframa("61940292006682", "210140267")

# Exiba a validação
print(suframa_info)
```

## ⚙️ API Reference

### CNPJAPIClient

Classe principal para interagir com a API Pública de CNPJ.

#### consultar_cnpj(cnpj: str) -> dict

Consulta informações de um CNPJ utilizando o método GET.

- **Parâmetros:**
  - `cnpj` (str): Número do CNPJ sem caracteres especiais.

- **Retorna:**
  - `dict`: Dados do CNPJ ou detalhes de erro.

- **Exceções:**
  - `APIException`: Erros gerais da API.
  - `RateLimitException`: Quando o limite de requisições é excedido.

**Exemplo:**

```python
client = CNPJAPIClient()
try:
    cnpj_info = client.consultar_cnpj("27865757000102")
    print(cnpj_info)
except APIException as e:
    print(e)
```

#### validar_inscricao_suframa(cnpj: str, inscricao: str) -> dict

Valida uma inscrição no SUFRAMA utilizando o método POST.

- **Parâmetros:**
  - `cnpj` (str): Número do CNPJ sem caracteres especiais.
  - `inscricao` (str): Número da inscrição no SUFRAMA.

- **Retorna:**
  - `dict`: Resultado da validação ou detalhes de erro.

- **Exceções:**
  - `APIException`: Erros gerais da API.
  - `RateLimitException`: Quando o limite de requisições é excedido.

**Exemplo:**

```python
client = CNPJAPIClient()
try:
    suframa_info = client.validar_inscricao_suframa("61940292006682", "210140267")
    print(suframa_info)
except APIException as e:
    print(e)
```

## 🔒 Tratamento de Erros

A biblioteca `cnpjData` utiliza exceções personalizadas para facilitar o tratamento de erros:

- **APIException:** Representa erros gerais da API, como respostas inesperadas ou falhas de conexão.

  ```python
  try:
      cnpj_info = client.consultar_cnpj("27865757000102")
  except APIException as e:
      print(f"Erro ao consultar CNPJ: {e.message}")
  ```

- **RateLimitException:** Indica que o limite de requisições foi excedido. A biblioteca tenta aguardar o tempo necessário antes de realizar a próxima requisição.

  ```python
  try:
      suframa_info = client.validar_inscricao_suframa("61940292006682", "210140267")
  except RateLimitException as e:
      print(f"Limite de requisições atingido: {e.message}")
  ```

## 📈 Limitações

A API Pública de CNPJ impõe as seguintes limitações:

- **Limite de Requisições:**
  - Até 3 consultas por minuto por IP para cada método (`GET` e `POST`).
  - O pacote `cnpjData` gerencia esses limites automaticamente, aguardando o tempo necessário antes de realizar novas requisições.

- **Penalidades por Excesso de Erros:**
  - Mais de 360 consultas por hora resultam em penalidades, bloqueando novas requisições por 1 hora.
  - Penalizações adicionais são aplicadas se o excesso de erros persistir.

- **Mensagens de Erro:**
  - Erro HTTP `429 Too Many Requests` é retornado quando os limites são excedidos.

## 🧪 Testes

A biblioteca inclui um conjunto de testes automatizados para garantir a funcionalidade correta.

### Executando os Testes

1. **Instale as Dependências de Teste:**

   Assegure-se de que todas as dependências estão instaladas:

   ```bash
   pip install -e .
   ```

2. **Execute os Testes:**

   Utilize o módulo `unittest` para descobrir e executar os testes:

   ```bash
   python -m unittest discover tests
   ```

### Estrutura de Testes

- **tests/test_client.py:** Contém testes para as funcionalidades principais da classe `CNPJAPIClient`, incluindo cenários de sucesso e tratamento de erros.

**Exemplo de Teste:**

```python
import unittest
from unittest.mock import patch
from cnpjData import CNPJAPIClient, APIException, RateLimitException

class TestCNPJAPIClient(unittest.TestCase):

    @patch('cnpjData.client.requests.get')
    def test_consultar_cnpj_success(self, mock_get):
        mock_response = mock_get.return_value
        mock_response.status_code = 200
        mock_response.json.return_value = {"cnpj": "27865757000102", "razao_social": "Test Company"}
        
        client = CNPJAPIClient()
        result = client.consultar_cnpj("27865757000102")
        self.assertIn("cnpj", result)
        self.assertEqual(result["cnpj"], "27865757000102")

    @patch('cnpjData.client.requests.get')
    def test_consultar_cnpj_rate_limit(self, mock_get):
        mock_response = mock_get.return_value
        mock_response.status_code = 429
        mock_response.json.return_value = {
            "status": 429,
            "titulo": "Muitas requisições",
            "detahes": "Excedido o limite máximo de 3 consultas por minuto. Liberação ocorrerá em Thu Jun 03 2021 16:15:00 GMT-0300 (Horário Padrão de Brasília)"
        }
        
        client = CNPJAPIClient()
        with self.assertRaises(RateLimitException):
            client.consultar_cnpj("27865757000102")

    @patch('cnpjData.client.requests.post')
    def test_validar_inscricao_suframa_success(self, mock_post):
        mock_response = mock_post.return_value
        mock_response.status_code = 200
        mock_response.json.return_value = {"cnpj": "61940292006682", "inscricao_suframa": "210140267", "ativo": True}
        
        client = CNPJAPIClient()
        result = client.validar_inscricao_suframa("61940292006682", "210140267")
        self.assertIn("ativo", result)
        self.assertTrue(result["ativo"])

    @patch('cnpjData.client.requests.post')
    def test_validar_inscricao_suframa_rate_limit(self, mock_post):
        mock_response = mock_post.return_value
        mock_response.status_code = 429
        mock_response.json.return_value = {
            "status": 429,
            "titulo": "Muitas requisições",
            "detahes": "Excedido o limite máximo de 3 consultas por minuto. Liberação ocorrerá em Thu Jun 03 2021 16:15:00 GMT-0300 (Horário Padrão de Brasília)"
        }
        
        client = CNPJAPIClient()
        with self.assertRaises(RateLimitException):
            client.validar_inscricao_suframa("61940292006682", "210140267")

if __name__ == '__main__':
    unittest.main()
```

## 🤝 Contribuição

Contribuições são altamente bem-vindas! Sinta-se à vontade para abrir issues e pull requests para melhorar o projeto. Aqui estão algumas diretrizes para contribuir:

### 📋 Passos para Contribuir

1. **Fork o Repositório:**

   Clique no botão "Fork" no GitHub para criar uma cópia do repositório em sua conta.

2. **Clone o Repositório Forkado:**

   ```bash
   git clone https://github.com/hqr90/cnpjData.git
   cd cnpjData
   ```

3. **Crie uma Branch para Sua Feature:**

   ```bash
   git checkout -b feature/nova-funcionalidade
   ```

4. **Faça as Alterações Desejadas:**

   Adicione ou modifique o código conforme necessário.

5. **Adicione e Commite as Alterações:**

   ```bash
   git add .
   git commit -m "Descrição clara das mudanças"
   ```

6. **Envie a Branch para o Repositório Remoto:**

   ```bash
   git push origin feature/nova-funcionalidade
   ```

7. **Abra um Pull Request:**

   No GitHub, abra um Pull Request a partir da sua branch para o repositório original.

### 📚 Boas Práticas

- **Escreva Testes:** Certifique-se de que seu código é acompanhado por testes automatizados.
- **Siga o Estilo de Código PEP8:** Utilize ferramentas como `flake8` ou `black` para manter o código consistente.
- **Documente Suas Mudanças:** Atualize a documentação se adicionar ou modificar funcionalidades.

### 🤔 Como Reportar Problemas

Se você encontrar algum problema ou bug, por favor, abra uma issue no repositório com uma descrição detalhada do problema e, se possível, passos para reproduzi-lo.

## 📄 Licença

Este projeto está licenciado sob a Licença MIT. Veja o arquivo [LICENSE](LICENSE) para mais detalhes.

## 👤 Autor

- **Hilton Queiroz Rebello**  
  📧 [rebello.hiltonqueiroz@gmail.com](mailto:rebello.hiltonqueiroz@gmail.com)  
  🔗 [LinkedIn](https://www.linkedin.com/in/hqr90/)  
  🔗 [GitHub](https://github.com/hqr90)


## 📌 Notas Finais

Parabéns por utilizar o **cnpjData**! Se tiver dúvidas, sugestões ou precisar de assistência, não hesite em entrar em contato através dos canais fornecidos. Sua contribuição e feedback são valiosos para a evolução contínua deste projeto.
