import threading, time
from datetime import datetime, timedelta
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import PyPDF2
import json
import re
import os
import psycopg2

i = 0

ultima_hora = datetime.now()
while i < 10:

    try:
        conn = psycopg2.connect(
            dbname="",
            user="",
            password="",
            host="",
            port=""
        )
        print("Connection successful")
        cur = conn.cursor()
        while True:
            if (datetime.now().strftime("%H") != ultima_hora.strftime("%H")):
                resultado = []
                posto_atual = None
                aux = 1
                resultados = []
                paginas = []
                texto = ""
                regex_posto = re.compile(r'(?P<posto>\d+)\s+POSTO')

                # Regex do item
                regex_item = re.compile(
                    r'(?P<peso>\d{1,3}(?:[.,]\d{3})*(?:[.,]\d+)?|\d+(?:[.,]\d+)?)\s+'
                    r'(?P<sku>\d+(?:\s*-\s*\d+)?|descartar)\s+'
                    r'(?P<quantidade>\d+)\s+'
                    r'(?P<nome>.+)',
                    re.IGNORECASE
                )

                # download_path = os.path.abspath("C://Users//Guilherme Luna//Downloads//teste")
                download_path = os.path.abspath("C://Users//DADOS_REFILE//Desktop//refile//relatorio")
                # Variaveis
                login = ["", ""]

                # Configs do navegador
                options = webdriver.EdgeOptions()
                options.add_argument('--log-level=3')
                options.add_experimental_option("prefs", {
                    "download.default_directory": download_path,
                    "download.prompt_for_download": False,  # Optional: prevents the "Save As" dialog
                    "download.directory_upgrade": True,
                    "safebrowsing.enabled": True,
                    "savefile.default_directory": download_path  # May be needed for some versions/OS
                })
                # options.add_argument("--headless=new")
                service = webdriver.EdgeService(executable_path='msedgedriver.exe')
                driver = webdriver.Edge(options=options, service=service)

                driver.get("http://192.168.12.200:8080/jasperserver/login.html")

                time.sleep(1)
                palete_escravo = driver.find_element(By.XPATH,
                                                     '/html/body/div[4]/div/div/div[1]/form/div/div/div[2]/div[2]/fieldset[1]/input[1]')
                palete_escravo.send_keys("")
                palete_escravo = driver.find_element(By.XPATH,
                                                     '/html/body/div[4]/div/div/div[1]/form/div/div/div[2]/div[2]/fieldset[1]/input[2]')
                palete_escravo.send_keys("")
                palete_escravo.send_keys(Keys.RETURN)
                time.sleep(1)
                check_input = driver.find_element(By.XPATH,
                                                  "/html/body/div[4]/div/div/div[4]/div[3]/div[2]/ul/li/ul/li[3]/p/b")
                check_input.click()
                time.sleep(1)
                check_input = driver.find_element(By.XPATH,
                                                  "/html/body/div[4]/div/div/div[2]/div/div[2]/ul/li[1]/div/div[2]/p[1]/a")
                check_input.click()
                time.sleep(1)
                now = datetime.now()  ######################
                hora_anterior = now - timedelta(hours=1)
                check_input = driver.find_element(By.XPATH,
                                                  "/html/body/div[8]/div[2]/div[2]/div/div/div/ul/div[1]/label/input")
                check_input.send_keys(hora_anterior.strftime("%Y-%m-%d %H:00:00"))
                check_input.send_keys(Keys.RETURN)
                time.sleep(1)
                check_input = driver.find_element(By.XPATH,
                                                  "/html/body/div[7]/div[2]/div[2]/div/div/div/ul/div[2]/label/input")
                check_input.send_keys(now.strftime("%Y-%m-%d %H:00:00"))
                time.sleep(1)
                check_input = driver.find_element(By.XPATH, "/html/body/div[7]/div[2]/div[3]/button[1]/span")
                check_input.click()
                time.sleep(5)
                check_input = driver.find_element(By.XPATH, "/html/body/div[7]/div[2]/div[3]/button[2]/span")
                check_input.click()
                time.sleep(1)
                check_input = driver.find_element(By.XPATH,
                                                  "/html/body/div[4]/div/div/div[2]/div/div[2]/ul[1]/li[4]/button")
                check_input.click()
                # if os.path.isfile('C://Users//Guilherme Luna//Downloads//teste//JBS_R2.pdf'):
                #    os.remove('C://Users//Guilherme Luna//Downloads//teste//JBS_R2.pdf')

                if os.path.isfile('C://Users//DADOS_REFILE//Desktop//refile//relatorio//JBS_R2.pdf'):
                    os.remove('C://Users//DADOS_REFILE//Desktop//refile//relatorio//JBS_R2.pdf')
                time.sleep(1)
                check_input = driver.find_element(By.XPATH, "/html/body/div[6]/div[1]/div/ul/li[1]/p")
                check_input.click()
                time.sleep(5)
                driver.quit()

                # pdf_file = open('C://Users//Guilherme Luna//Downloads//teste//JBS_R2.pdf', 'rb')
                pdf_file = open('C://Users//DADOS_REFILE//Desktop//refile//relatorio//JBS_R2.pdf', 'rb')
                read_pdf = PyPDF2.PdfReader(pdf_file)

                for i in range(len(read_pdf.pages)):
                    page = read_pdf.pages[i]
                    page_content = page.extract_text()
                    # data = json.dumps(page_content) #fazer regex para coletar dados pont > peso - sku - quantidade - nome
                    # paginas.append(data)
                    arquivo = open('pg' + str(i), 'w')
                    arquivo.write(page_content)
                    arquivo.close()

                ###############################
                for i in range(len(read_pdf.pages)):
                    print("pagina ", i + 1)
                    with open('pg' + str(i), 'r') as f:
                        texto = f.read()

                    for linha in texto.splitlines():
                        linha = linha.strip()
                        if not linha:
                            continue

                        # Verifica posto
                        m_posto = regex_posto.search(linha)
                        if m_posto:
                            posto_atual = int(m_posto.group("posto"))
                            continue
                        # Verifica item
                        m_item = regex_item.search(linha)
                        if m_item and posto_atual is not None:
                            item = {
                                "posto": posto_atual,
                                "peso": m_item.group("peso"),
                                "sku": m_item.group("sku"),
                                "quantidade": int(m_item.group("quantidade")),
                                "nome": m_item.group("nome").strip()
                            }
                            if item['sku'] == 'descartar':
                                item['sku'] = '404'
                            item['sku'] = item["sku"].replace(' - ', '')
                            resultado.append(item)
                for r in resultado:
                    float_value = r["peso"].replace('.', '')
                    float_value = float(float_value.replace(',', '.'))
                    hora_atual = datetime.now()  ######################
                    hora_anterior_1 = now - timedelta(hours=1)
                    datatime = hora_anterior_1.strftime("%Y-%m-%d %H:00:15")
                    cur.execute(
                        f"INSERT INTO REFILE_H (PONTO,SKU, PESO, QUANTIDADE, NOME, DATETIME) VALUES ({r['posto']},{r["sku"]},{float_value},{r["quantidade"]}, \'{str(r["nome"])}\', \'{datatime}\');")
                    conn.commit()

                pdf_file.close()
                ultima_hora = datetime.now()
                time.sleep(1)
                print(datetime.now())

            else:
                print("HORA: ", datetime.now())
                time.sleep(60)

    except:
        cur.close()
        conn.close()
        print("Falha na execucao")
        time.sleep(60)

    i = i + 1
    print("quantidade de falhas: ", i)
