import zeep.exceptions
from zeep import Client, xsd


class OmieClient:
    _WDSLS = [
        "https://app.omie.com.br/api/v1/financas/contapagar/?WSDL",
        "https://app.omie.com.br/api/v1/financas/contareceber/?WSDL",
        "https://app.omie.com.br/api/v1/geral/anexo/?WSDL",
        "https://app.omie.com.br/api/v1/geral/clientes/?WSDL",
        "https://app.omie.com.br/api/v1/geral/categorias/?WSDL",
        "https://app.omie.com.br/api/v1/geral/departamentos/?WSDL",
    ]

    def __init__(self, app_key, app_secret) -> None:
        self._app_key = app_key
        self._app_secret = app_secret
        self._clients = []

        auth_header = xsd.Element(
            "auth",
            xsd.ComplexType(
                [
                    xsd.Element("app_key", xsd.String()),
                    xsd.Element("app_secret", xsd.String()),
                ]
            ),
        )

        auth_value = auth_header(app_key=self._app_key, app_secret=self._app_secret)

        for wdsl in self._WDSLS:
            client = Client(wdsl)
            client.set_default_soapheaders([auth_value])
            self._clients.append(client)

    def execute_call(self, method_name: str, params: dict, is_paginated: bool = False):
        for client in self._clients:
            method = getattr(client.service, method_name, None)
            if method:
                response = method(params)
                if (
                    is_paginated
                    and "total_de_paginas" in response
                    or "nTotPaginas" in response
                ):
                    return PaginatedResponse(method, params, response)
                return response

        raise ValueError(
            f"Método '{method_name}' não encontrado em nenhum endpoint registrado."
        )

    def get_type(self, type_name):
        for client in self._clients:
            try:
                return client.get_type("ns0:" + type_name)
            except zeep.exceptions.LookupError:
                continue
        raise ValueError(
            f"Tipo '{type_name}' não encontrado em nenhum endpoint registrado."
        )


class PaginatedResponse:
    def __init__(self, method, params: dict, response: dict) -> None:
        self.page_number = getattr(
            response, "pagina", getattr(response, "nPagina", None)
        )
        self.page_total = getattr(
            response, "total_de_paginas", getattr(response, "nTotPaginas", None)
        )
        self.params = params
        self._method = method
        self._current_response = response
        self._first_return = False

    def __iter__(self):
        return self

    def __next__(self):
        if not self._first_return:
            self._first_return = True
            return self._current_response

        self.page_number += 1

        if self.page_number > self.page_total:
            raise StopIteration()

        if "pagina" in self.params:
            self.params["pagina"] = self.page_number
        if "nPagina" in self.params:
            self.params["nPagina"] = self.page_number

        self._current_response = self._method(self.params)

        return self._current_response
