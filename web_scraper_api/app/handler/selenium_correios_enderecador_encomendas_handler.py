import os
import requests
import time

from retrying import retry

from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

from app.handler.selenium_handler import SeleniumHandler


class SeleniumCorreiosEnderecadorEncomendasHandler(SeleniumHandler):
    @retry(wait_fixed=60, stop_max_attempt_number=3)
    def _retrying_requests_get(self, url: str):
        return requests.get(url, timeout=600)

    def enderecador_encomendas(self, remetente: dict, destinatario_list: list) -> list:
        chrome_download_default_directory = self.connector.app_config.get(
            "chrome_download_default_directory"
        )

        js_window_open_path = os.path.join(
            self.connector.app_config.get("javascript_directory"),
            "correios_enderecador_encomendas.js"
        )

        try:
            with open(js_window_open_path, "r", encoding="utf-8") as js_file:
                js_window_open = js_file.read()

        except FileNotFoundError:
            print(f"File '{js_window_open_path}' not found.")

        xpath_copiar_remetente_anterior = {
            "2": "/html/body/div[1]/div[3]/div[2]/div/div/div[2]/div[2]/div[2]/form/div[4]/div/p/a[2]",
            "3": "/html/body/div[1]/div[3]/div[2]/div/div/div[2]/div[2]/div[2]/form/div[6]/div/p/a[2]",
            "4": "/html/body/div[1]/div[3]/div[2]/div/div/div[2]/div[2]/div[2]/form/div[8]/div/p/a[2]"
        }

        xpath_observacao = {
            "1": "/html/body/div[1]/div[3]/div[2]/div/div/div[2]/div[2]/div[2]/form/div[3]/div/span[9]/label/textarea",
            "2": "/html/body/div[1]/div[3]/div[2]/div/div/div[2]/div[2]/div[2]/form/div[5]/div/span[9]/label/textarea",
            "3": "/html/body/div[1]/div[3]/div[2]/div/div/div[2]/div[2]/div[2]/form/div[7]/div/span[9]/label/textarea",
            "4": "/html/body/div[1]/div[3]/div[2]/div/div/div[2]/div[2]/div[2]/form/div[9]/div/span[9]/label/textarea"
        }

        xpath_preencha_declaracao_conteudo = {
            "1": "/html/body/div[1]/div[3]/div[2]/div/div/div[2]/div[2]/div[2]/form/div[3]/div/span[9]/label/li/a",
            "2": "/html/body/div[1]/div[3]/div[2]/div/div/div[2]/div[2]/div[2]/form/div[5]/div/span[9]/label/li/a",
            "3": "/html/body/div[1]/div[3]/div[2]/div/div/div[2]/div[2]/div[2]/form/div[7]/div/span[9]/label/li/a",
            "4": "/html/body/div[1]/div[3]/div[2]/div/div/div[2]/div[2]/div[2]/form/div[9]/div/span[9]/label/li/a"
        }

        destinatario_id_list = []
        file_list = []

        for index, destinatario in enumerate(destinatario_list):
            if index == 0:
                remetente_cep = self.connector.driver.find_element(
                    By.XPATH, '//*[@id="cep_1"]'
                )
                remetente_cep.send_keys(remetente.get("cep").replace("-", ""))
                remetente_cep.send_keys(Keys.TAB)

                time.sleep(1)

                remetente_nome = self.connector.driver.find_element(
                    By.XPATH, '//*[@id="nome_1"]'
                )
                remetente_nome.send_keys(remetente.get("nome"))

                remetente_numero = self.connector.driver.find_element(
                    By.XPATH, '//*[@id="numero_1"]'
                )
                remetente_numero.send_keys(remetente.get("numero"))
            else:
                copiar_remetente_anterior = self.connector.driver.find_element(
                    By.XPATH, xpath_copiar_remetente_anterior.get(
                        f"{index + 1}"
                    )
                )
                copiar_remetente_anterior.click()

            ##########

            destinatario_id_list.append(destinatario.get("id"))

            destinatario_cep = self.connector.driver.find_element(
                By.XPATH, f'//*[@id="desCep_{index + 1}"]'
            )
            destinatario_cep.send_keys(
                destinatario.get("cep").replace("-", ""))
            destinatario_cep.send_keys(Keys.TAB)

            time.sleep(1)

            destinatario_nome = self.connector.driver.find_element(
                By.XPATH, f'//*[@id="desNome_{index + 1}"]'
            )
            destinatario_nome.send_keys(destinatario.get("nome"))

            destinatario_numero = self.connector.driver.find_element(
                By.XPATH, f'//*[@id="desNumero_{index + 1}"]'
            )
            destinatario_numero.send_keys(destinatario.get("numero"))

            destinatario_complemento = self.connector.driver.find_element(
                By.XPATH, f'//*[@id="desComplemento_{index + 1}"]'
            )
            destinatario_complemento.send_keys(destinatario.get("complemento"))

            observacao = self.connector.driver.find_element(
                By.XPATH, xpath_observacao.get(f"{index + 1}")
            )
            observacao.send_keys(f"ID {destinatario.get('id')}")

            preencha_declaracao_conteudo = self.connector.driver.find_element(
                By.XPATH, xpath_preencha_declaracao_conteudo.get(
                    f"{index + 1}"
                )
            )
            preencha_declaracao_conteudo.click()

            time.sleep(2)

            ##########

            new_window_handle = None

            while not new_window_handle:
                new_window_handle = self.connector.driver.window_handles[-1]

            self.connector.driver.switch_to.window(new_window_handle)

            dc_remetente_cpf_cnpj = self.connector.driver.find_element(
                By.XPATH, '//*[@id="cnpjcpf"]'
            )
            dc_remetente_cpf_cnpj.send_keys(remetente.get("cpf_cnpj"))

            dc_destinatario_cpf_cnpj = self.connector.driver.find_element(
                By.XPATH, '//*[@id="desCnpjcpf"]'
            )
            dc_destinatario_cpf_cnpj.send_keys(destinatario.get("cpf_cnpj"))

            for item_index, item in enumerate(destinatario.get("itens_declaracao_conteudo")):
                # Max. 6
                if item_index == 5:
                    break

                dc_item = self.connector.driver.find_element(
                    By.XPATH, f'//*[@id="item{item_index + 1}"]'
                )
                dc_item.send_keys(str(item_index + 1))

                dc_conteudo = self.connector.driver.find_element(
                    By.XPATH, f'//*[@id="cont{item_index + 1}"]'
                )
                dc_conteudo.send_keys(item.get("conteudo"))

                dc_quantidade = self.connector.driver.find_element(
                    By.XPATH, f'//*[@id="quant{item_index + 1}"]'
                )
                dc_quantidade.send_keys(item.get("quantidade"))

                dc_valor = self.connector.driver.find_element(
                    By.XPATH, f'//*[@id="val{item_index + 1}"]'
                )
                dc_valor.send_keys(item.get("valor"))

            dc_peso_total = self.connector.driver.find_element(
                By.XPATH, '//*[@id="pesototal"]'
            )
            dc_peso_total.send_keys(destinatario.get("peso_total"))

            dc_imprimir = self.connector.driver.find_element(
                By.XPATH, '/html/body/div[1]/div[3]/div[2]/div/div/div[2]/div[2]/div[2]/table[4]/tbody/tr/td[1]/a'
            )

            js_dc_imprimir_onclick = dc_imprimir.get_attribute("onclick")

            time.sleep(2)

            pdf_url = self.connector.driver.execute_script(f"""
                {js_window_open}
                {js_dc_imprimir_onclick}
                return openedUrl;
            """)

            time.sleep(1)

            response = self._retrying_requests_get(pdf_url)

            time.sleep(2)

            if response.status_code == 200:
                current_filename = "formDeclaracao.pdf"
                current_filename_path = os.path.join(
                    chrome_download_default_directory,
                    current_filename
                )

                new_filename = f"Declaracao_Conteudo-{destinatario.get('id')}.pdf"
                new_filename_path = os.path.join(
                    chrome_download_default_directory,
                    new_filename
                )

                # Headless Mode
                if os.path.exists(current_filename_path):
                    try:
                        time.sleep(1)
                        os.replace(current_filename_path, new_filename_path)

                    except FileExistsError:
                        os.remove(new_filename_path)
                        os.replace(current_filename_path, new_filename_path)
                # Non-headless Mode
                else:
                    with open(new_filename_path, "wb") as pdf_file:
                        pdf_file.write(response.content)

                file_list_item = {
                    "filename": f"{new_filename}",
                    "timestamp": f"{os.path.getctime(new_filename_path)}"
                }

                file_list.append(file_list_item)

            self.connector.driver.close()

            self.connector.driver.switch_to.window(
                self.connector.driver.window_handles[0]
            )

            time.sleep(2)

        gerar_etiquetas = self.connector.driver.find_element(
            By.XPATH, '//*[@id="btGerarEtiquetas"]'
        )
        gerar_etiquetas.click()

        time.sleep(2)

        if len(self.connector.driver.window_handles) > 1:
            # Switch to the new window
            new_window_handle = self.connector.driver.window_handles[1]
            self.connector.driver.switch_to.window(new_window_handle)

            # Close the new window
            self.connector.driver.close()

            # Switch back to the original window
            self.connector.driver.switch_to.window(
                self.connector.driver.window_handles[0]
            )

        destinatario_id_string = "_".join(destinatario_id_list)

        current_filename = "Encomenda.pdf"
        current_filename_path = os.path.join(
            chrome_download_default_directory,
            current_filename
        )

        new_filename = f"Encomenda-{destinatario_id_string}.pdf"
        new_filename_path = os.path.join(
            chrome_download_default_directory,
            new_filename
        )

        try:
            os.replace(current_filename_path, new_filename_path)

        except FileExistsError:
            os.remove(new_filename_path)
            os.replace(current_filename_path, new_filename_path)

        file_list_item = {
            "filename": f"{new_filename}",
            "timestamp": f"{os.path.getctime(new_filename_path)}"
        }

        file_list.append(file_list_item)

        return file_list
