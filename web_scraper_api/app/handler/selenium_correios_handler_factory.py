from app.connector.base_connector import BaseConnector
from app.handler.selenium_handler import SeleniumHandler
from app.handler.selenium_correios_enderecador_encomendas_handler import SeleniumCorreiosEnderecadorEncomendasHandler


class SeleniumCorreiosHandlerFactory:
    @staticmethod
    def create(connector: BaseConnector, url: str) -> SeleniumHandler:
        if "www2.correios.com.br" in url:
            if "/enderecador/encomendas/default.cfm" in url:
                return SeleniumCorreiosEnderecadorEncomendasHandler(connector, url)
        else:
            raise ValueError("Unsupported URL.")
