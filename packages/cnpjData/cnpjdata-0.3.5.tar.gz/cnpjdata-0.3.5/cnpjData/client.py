# cnpjData/client.py

import time
import requests
import json
from collections import deque
from datetime import datetime, timedelta

class RateLimiter:
    def __init__(self, max_calls, period_seconds):
        self.max_calls = max_calls
        self.period = timedelta(seconds=period_seconds)
        self.calls = deque()

    def wait(self):
        now = datetime.now()
        while self.calls and now - self.calls[0] > self.period:
            self.calls.popleft()
        if len(self.calls) >= self.max_calls:
            earliest = self.calls[0]
            wait_time = (earliest + self.period - now).total_seconds()
            print(f"Aguardando {wait_time:.2f} segundos para nova requisição...")
            time.sleep(wait_time)
        self.calls.append(datetime.now())


class APIException(Exception):
    def __init__(self, status, message):
        super().__init__(f"APIException: Status {status} - {message}")
        self.status = status
        self.message = message


class RateLimitException(APIException):
    def __init__(self, status, message):
        super().__init__(status, message)
        self.message = "Limite de requisições atingido."


class CNPJAPIClient:
    BASE_URL = "https://publica.cnpj.ws"

    def __init__(self):
        self.get_rate_limiter = RateLimiter(
            max_calls=3, period_seconds=60
        )  # 3 GET requests per minute
        self.post_rate_limiter = RateLimiter(
            max_calls=3, period_seconds=60
        )  # 3 POST requests per minute

    def consultar_cnpj(self, cnpj):
        """
        Consulta informações de um CNPJ utilizando o método GET.

        :param cnpj: Número do CNPJ sem caracteres especiais (string)
        :return: Dicionário com os dados do CNPJ ou mensagem de erro
        """
        self.get_rate_limiter.wait()
        endpoint = f"{self.BASE_URL}/cnpj/{cnpj}"
        try:
            response = requests.get(endpoint)
            if response.status_code == 200:
                return response.json()
            elif response.status_code == 429:
                return self._handle_rate_limit(response)
            else:
                raise APIException(status=response.status_code, message=response.text)
        except requests.RequestException as e:
            raise APIException(status="error", message=str(e))

    def validar_inscricao_suframa(self, cnpj, inscricao):
        """
        Valida uma inscrição no SUFRAMA utilizando o método POST.

        :param cnpj: Número do CNPJ sem caracteres especiais (string)
        :param inscricao: Número da inscrição no SUFRAMA (string)
        :return: Dicionário com a validação ou mensagem de erro
        """
        self.post_rate_limiter.wait()
        endpoint = f"{self.BASE_URL}/suframa"
        payload = {"cnpj": cnpj, "inscricao": inscricao}
        headers = {"Content-Type": "application/json"}
        try:
            response = requests.post(
                endpoint, headers=headers, data=json.dumps(payload)
            )
            if response.status_code == 200:
                return response.json()
            elif response.status_code == 429:
                return self._handle_rate_limit(response)
            else:
                raise APIException(status=response.status_code, message=response.text)
        except requests.RequestException as e:
            raise APIException(status="error", message=str(e))

    def _handle_rate_limit(self, response):
        """
        Trata erros de limite de requisições (HTTP 429).

        :param response: Objeto de resposta HTTP
        :return: Dicionário com detalhes do erro
        """
        try:
            error_info = response.json()
            reset_time_str = error_info.get("detahes", "")
            reset_time = self._parse_reset_time(reset_time_str)
            if reset_time:
                wait_seconds = (reset_time - datetime.now()).total_seconds()
                if wait_seconds > 0:
                    print(
                        f"Limite de requisições atingido. Aguardando {wait_seconds:.2f} segundos..."
                    )
                    time.sleep(wait_seconds)
                    # Após esperar, tenta novamente a requisição
                    return {
                        "status": 429,
                        "message": "Limite de requisições atingido. Tentando novamente...",
                    }
        except json.JSONDecodeError:
            pass
        raise RateLimitException(status=response.status_code, message=response.text)

    def _parse_reset_time(self, reset_time_str):
        """
        Extrai o horário de reset da mensagem de erro.

        :param reset_time_str: String contendo a data e hora do reset
        :return: Objeto datetime ou None
        """
        try:
            # Exemplo de formato: "Thu Jun 03 2021 16:15:00 GMT-0300 (Horário Padrão de Brasília)"
            reset_time_part = reset_time_str.split(" GMT")[0]
            reset_time = datetime.strptime(reset_time_part, "%a %b %d %Y %H:%M:%S")
            return reset_time
        except (ValueError, IndexError):
            return None
