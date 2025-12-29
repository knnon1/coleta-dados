import os
import threading, time
import json
import subprocess
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import psycopg
from dotenv import load_dotenv



load_dotenv()

# Variaveis
login = [os.getenv("LOGIN"), os.getenv("SENHA")]
USUARIO = os.getenv("USUARIO")
SENHA = os.getenv("SENHA")
IP = os.getenv("IP")
DB = os.getenv("DB")
print(DB)
conn = psycopg.connect(
    user=USUARIO,
    password=SENHA,
    host=IP,
    dbname=DB
)
print("Connected to Postgresql")

# Variaveis Hora Hora Transelevador
aux = 0
iLastHour = datetime.now().strftime("%H")
iPaleteAcum= [0,0,0,0,0,0]
vetPaleteCongHora = [0,0,0] #Valor Hora Hora do Armazenamento Congelado
vetPaleteResfHora = [0,0,0] #Valor Hora Hora do Armazenamento Resfriado

# Configs do navegador
options = webdriver.EdgeOptions()
options.add_argument('--log-level=3')
# options.add_argument("--headless=new")
service = webdriver.EdgeService(executable_path='msedgedriver.exe')
driver = webdriver.Edge(options=options, service=service)


# Funções
def verifica_contentor():
    try:
        retorno = [0,0,0,0]
        driver.get("https://192.168.20.60/SmartUI/smartui?viewname=JBS_SEARA%7CContainerVList&viewtype=ViewList")
        time.sleep(1)


        palete_escravo = driver.find_element(By.XPATH, '/html/body/smartui/div/home/app-viewlist/div/div[1]/app-viewgrid/div/div/kendo-grid/div/div/div/table/thead/tr[2]/td[5]/app-stringfilter/div/input')
        palete_escravo.send_keys("PE")
        palete_escravo.send_keys(Keys.RETURN)
        palete_escravo = driver.find_element(By.XPATH,'/html/body/smartui/div/home/app-viewlist/div/div[1]/app-viewgrid/div/div/kendo-grid/div/div/div/table/thead/tr[2]/td[7]/app-stringfilter/div/input')
        palete_escravo.send_keys("00")
        palete_escravo.send_keys(Keys.RETURN)
        time.sleep(1)
        palete_escravo_resf = driver.find_element(By.XPATH, '/html/body/smartui/div/home/app-viewlist/div/div[1]/app-viewgrid/div/div/div/app-tilestrip/div/div/div/div[2]/app-tile/div/p[2]')
        #print(palete_escravo_resf.text)
        total_palet_escr_resf = palete_escravo_resf.text.replace(".", "")
        time.sleep(1)


        palete_escravo = driver.find_element(By.XPATH,
                                             '/html/body/smartui/div/home/app-viewlist/div/div[1]/app-viewgrid/div/div/kendo-grid/div/div/div/table/thead/tr[2]/td[7]/app-stringfilter/div/input')
        palete_escravo.send_keys(Keys.BACKSPACE)
        palete_escravo.send_keys(Keys.BACKSPACE)
        palete_escravo.send_keys("01")
        palete_escravo.send_keys(Keys.RETURN)
        time.sleep(1)
        palete_escravo_cong = driver.find_element(By.XPATH,'/html/body/smartui/div/home/app-viewlist/div/div[1]/app-viewgrid/div/div/div/app-tilestrip/div/div/div/div[2]/app-tile/div/p[2]')
        #print(palete_escravo_cong.text)
        total_palet_escr_cong = palete_escravo_cong.text.replace(".", "")
        time.sleep(1)

        palete_escravo = driver.find_element(By.XPATH,'/html/body/smartui/div/home/app-viewlist/div/div[1]/app-viewgrid/div/div/kendo-grid/div/div/div/table/thead/tr[2]/td[5]/app-stringfilter/div/input')
        palete_escravo.send_keys(Keys.BACKSPACE)
        palete_escravo.send_keys(Keys.BACKSPACE)
        palete_escravo.send_keys(Keys.RETURN)
        time.sleep(1)
        palete_total_cong = driver.find_element(By.XPATH,'/html/body/smartui/div/home/app-viewlist/div/div[1]/app-viewgrid/div/div/div/app-tilestrip/div/div/div/div[2]/app-tile/div/p[2]')
        #print(palete_total_cong.text)
        total_palet_cong = palete_total_cong.text.replace(".", "")
        time.sleep(1)

        palete_escravo = driver.find_element(By.XPATH,'/html/body/smartui/div/home/app-viewlist/div/div[1]/app-viewgrid/div/div/kendo-grid/div/div/div/table/thead/tr[2]/td[7]/app-stringfilter/div/input')
        palete_escravo.send_keys(Keys.BACKSPACE)
        palete_escravo.send_keys(Keys.BACKSPACE)
        palete_escravo.send_keys("00")
        palete_escravo.send_keys(Keys.RETURN)
        time.sleep(1)
        palete_total_resf = driver.find_element(By.XPATH,'/html/body/smartui/div/home/app-viewlist/div/div[1]/app-viewgrid/div/div/div/app-tilestrip/div/div/div/div[2]/app-tile/div/p[2]')
        #print(palete_total_resf.text)
        total_palet_resf = palete_total_resf.text.replace(".", "")

        time.sleep(1)

        driver.get("https://192.168.20.60/smartui/smartui?viewname=JBS_SEARA|TasksPanelVList&viewtype=ViewList&identifier=58be10f8-116d-0d63-1e99-4cd8cea23a7e&infomode=60000")
        time.sleep(1)
        retorno = [int(total_palet_resf), int(total_palet_escr_resf), int(total_palet_cong), int(total_palet_escr_cong)]
        return retorno
    except:
        driver.get("https://192.168.20.60/smartui/smartui?viewname=JBS_SEARA|TasksPanelVList&viewtype=ViewList&identifier=58be10f8-116d-0d63-1e99-4cd8cea23a7e&infomode=60000")
        time.sleep(10)
        return retorno


try:
    # abre o navegador na pagina configurada
    driver.get(
        "https://192.168.20.60/smartui/smartui?viewname=JBS_SEARA|TasksPanelVList&viewtype=ViewList&identifier=58be10f8-116d-0d63-1e99-4cd8cea23a7e&infomode=60000")

    # entra na tela de login
    elem = driver.find_element(By.XPATH, '//*[@id="details-button"]')
    elem.click()

    elem = driver.find_element(By.XPATH, '//*[@id="proceed-link"]')
    elem.click()

    # login no wms
    loginInput = driver.find_element(By.XPATH, '//*[@id="formLogin"]/form/div[1]/input')
    loginInput.send_keys(login[0])
    login_ps = driver.find_element(By.XPATH, '/html/body/smartui/div/login/div/div/div[3]/form/div[2]/input')
    login_ps.send_keys(login[1])
    login_conf = driver.find_element(By.XPATH, '//*[@id="formLogin"]/form/button[1]')
    login_conf.click()



    """time.sleep(5)
    driver.refresh()"""
    i = 0
    tmp_ent_r, tmp_rej_r, tmp_exp_r, tmp_ent_c, tmp_rej_c, tmp_exp_c = 0, 0, 0, 0, 0, 0
    ult_valor_ent_r, ult_valor_rej_r, ult_valor_exp_r, ult_valor_ent_c, ult_valor_rej_c, ult_valor_exp_c = 0, 0, 0, 0, 0, 0
    tempo_up = 1

    detect = threading.Thread(target=input)
    detect.start()
    count = 0
    print("Pressione <ENTER> para parar.")

    while detect.is_alive():

        count += 1
        time.sleep(1)
        """if count % 90 == 0:
            driver.refresh()"""
        # print(driver.page_source)
        if count % 60 == 0:
            tempo_up += 1
            #print(tempo_up)
            # mostra o valor no console
            # RESFRIADO
            valor_entrada_resfriado = driver.find_element(By.XPATH,
                                                          '//*[@id="rightDiv"]/app-viewedit/div/div[2]/app-entity-editor/div/div/app-viewpanel/div/div[1]/div[1]/div/div/app-viewpanel/div/div[1]/div[1]/div/view-gauge/div/span')
            # print("Quantidade Total Armazenada RESFRIADO:", valor_entrada_resfriado.text)

            valor_expedido_resfriado = driver.find_element(By.XPATH,
                                                           '//*[@id="rightDiv"]/app-viewedit/div/div[2]/app-entity-editor/div/div/app-viewpanel/div/div[1]/div[1]/div/div/app-viewpanel/div/div[1]/div[3]/div/view-gauge/div/span')
            # print("Quantidade Total expedida RESFRIADO:", valor_expedido_resfriado.text)

            valor_rejeito_resfriado = driver.find_element(By.XPATH,
                                                          '//*[@id="rightDiv"]/app-viewedit/div/div[2]/app-entity-editor/div/div/app-viewpanel/div/div[1]/div[1]/div/div/app-viewpanel/div/div[1]/div[2]/div/view-gauge/div/span')
            # print("Quantidade Total rejeito RESFRIADO:", valor_rejeito_resfriado.text)

            # CONGELADO
            valor_entrada_congelado = driver.find_element(By.XPATH,
                                                          '//*[@id="rightDiv"]/app-viewedit/div/div[2]/app-entity-editor/div/div/app-viewpanel/div/div[1]/div[2]/div/div/app-viewpanel/div/div[1]/div[1]/div/view-gauge/div/span')
            # print("Quantidade Total Armazenado CONGELADO:", valor_entrada_congelado.text)

            valor_expedido_congelado = driver.find_element(By.XPATH,
                                                           '//*[@id="rightDiv"]/app-viewedit/div/div[2]/app-entity-editor/div/div/app-viewpanel/div/div[1]/div[2]/div/div/app-viewpanel/div/div[1]/div[3]/div/view-gauge/div/span')
            # print("Quantidade Total expedida CONGELADO:", valor_expedido_congelado.text)

            valor_rejeito_congelado = driver.find_element(By.XPATH,
                                                          '//*[@id="rightDiv"]/app-viewedit/div/div[2]/app-entity-editor/div/div/app-viewpanel/div/div[1]/div[2]/div/div/app-viewpanel/div/div[1]/div[2]/div/view-gauge/div/span')
            # print("Quantidade Total rejeito CONGELADO:", valor_rejeito_congelado.text


            valor_ent_resf = valor_entrada_resfriado.text.replace(".", "")
            valor_rej_resf = valor_rejeito_resfriado.text.replace(".", "")
            valor_exp_resf = valor_expedido_resfriado.text.replace(".", "")
            # Abre um payload para mensagem com o DB

            #verifica se o ultimo valor é igual ao anterior e soma 1 ao tempo
            if valor_ent_resf == ult_valor_ent_r:
                tmp_ent_r +=1
            else:
                ult_valor_ent_r = valor_ent_resf

            if valor_rej_resf == ult_valor_rej_r:
                tmp_rej_r +=1
            else:
                ult_valor_rej_r = valor_rej_resf

            if valor_exp_resf == ult_valor_exp_r:
                tmp_exp_r +=1
            else:
                ult_valor_exp_r = valor_exp_resf

            valor_ent_cong = valor_entrada_congelado.text.replace(".", "")
            valor_rej_cong = valor_rejeito_congelado.text.replace(".", "")
            valor_exp_cong = valor_expedido_congelado.text.replace(".", "")

            #Relatório Hora Hora Transelevador Congelados
            if iLastHour != datetime.now().strftime("%H"):
                arquivoHH = open("dadosHora.txt", "r")
                jsonHH = json.load(arquivoHH)
                arquivoHH.close()

                iPaleteAcum[0] = int(jsonHH["entCong"])
                iPaleteAcum[1] = int(jsonHH["rejCong"])
                iPaleteAcum[2] = int(jsonHH["expCong"])
                iPaleteAcum[3] = int(jsonHH["entResf"])
                iPaleteAcum[4] = int(jsonHH["rejResf"])
                iPaleteAcum[5] = int(jsonHH["expResf"])

                vetPaleteCongHora[0] = (int(valor_ent_cong) - iPaleteAcum[0])
                vetPaleteCongHora[1] = (int(valor_rej_cong) - iPaleteAcum[1])
                vetPaleteCongHora[2] = (int(valor_exp_cong) - iPaleteAcum[2])
                vetPaleteResfHora[0] = (int(valor_ent_resf) - iPaleteAcum[3])
                vetPaleteResfHora[1] = (int(valor_rej_resf) - iPaleteAcum[4])
                vetPaleteResfHora[2] = (int(valor_exp_resf) - iPaleteAcum[5])

                arquivoHH = open("dadosHora.txt", "w")
                #arquivoHH.write('{"entCong": 0, "rejCong": 0, "expCong": 0}')
                arquivoHH.write('{"entCong":'+valor_ent_cong+', "rejCong":'+valor_rej_cong+', "expCong":'+valor_exp_cong+', "entResf":'+valor_ent_resf+', "rejResf":'+valor_rej_resf+', "expResf":'+valor_exp_resf+'}')
                arquivoHH.close()

                HH_paletes = verifica_contentor()
                with conn.cursor() as cur:
                    cur.execute(f"INSERT INTO hhcongelado(entrada, saida, rejeito, total_palet, total_esc, datetime) VALUES ({vetPaleteCongHora[0]}, {vetPaleteCongHora[2]}, {vetPaleteCongHora[1]}, {HH_paletes[2]}, {HH_paletes[3]}, \'{datetime.now().strftime("%Y-%m-%d %H:00:01")}\');")
                    cur.execute(f"INSERT INTO hhresfriado(entrada, saida, rejeito, total_palet, total_esc, datetime) VALUES ({vetPaleteResfHora[0]}, {vetPaleteResfHora[2]}, {vetPaleteResfHora[1]}, {HH_paletes[0]}, {HH_paletes[1]}, \'{datetime.now().strftime("%Y-%m-%d %H:00:01")}\');")
                conn.commit()
            print(datetime.now().strftime("%m/%d/%Y, %H:%M:%S"))
            iLastHour = datetime.now().strftime("%H")


            if valor_ent_cong == ult_valor_ent_c:
                tmp_ent_c += 1
            else:
                ult_valor_ent_c = valor_ent_cong

            if valor_rej_cong == ult_valor_rej_c:
                tmp_rej_c += 1
            else:
                ult_valor_rej_c = valor_rej_cong

            if valor_exp_cong == ult_valor_exp_c:
                tmp_exp_c += 1
            else:
                ult_valor_exp_c = valor_exp_cong

            if (datetime.now().strftime("%H") == "05") and ((datetime.now().strftime("%M") == "02") or (datetime.now().strftime("%M") == "03")) and (aux == 0):
                tmp_ent_r, tmp_rej_r, tmp_exp_r, tmp_ent_c, tmp_rej_c, tmp_exp_c = 0, 0, 0, 0, 0, 0
                arquivoHH = open("dadosHora.txt", "w")
                arquivoHH.write('{"entCong":0, "rejCong":0, "expCong":0, "entResf":0, "rejResf":0, "expResf":0}')
                arquivoHH.close()
                aux = 1
            if datetime.now().strftime("%H") != "05":
                aux = 0
            #print(datetime.now().strftime("%m/%d/%Y, %H:%M:%S"))

            # envia o Payload para o POSTGRESQL
            with conn.cursor() as cur:
                cur.execute(
                    f"INSERT INTO totcongelado(entrada, saida, rejeito, datetime) VALUES ({int(valor_ent_cong)}, {int(valor_exp_cong)}, {int(valor_rej_cong)}, \'{datetime.now().strftime("%Y-%m-%d %H:%M:01")}\');")
                cur.execute(
                    f"INSERT INTO totresfriado(entrada, saida, rejeito, datetime) VALUES ({int(valor_ent_resf)}, {int(valor_exp_resf)},{int(valor_rej_resf)}, \'{datetime.now().strftime("%Y-%m-%d %H:%M:01")}\');")
            conn.commit()
            if tempo_up % 2 == 0:
                driver.refresh()
                time.sleep(5)
        if count >= 600:
            count = 0

    print("<ENTER> detectado -- finalizando")
    driver.close()
    driver.quit()
    print(1)
except Exception as e:
    driver.close()
    driver.quit()
    print("<ERRO> erro detectado")
    print(e)
exit()

"""

Autor: Guilherme Luna
Revisão: 1.16
Versão Python: 3.12.6
Versão: pip 23.2.1
Ultima atualização: 03/10/2025
Bibliotecas:    -Selenium 4.27.1
                -influxdb-client 1.48.0
"""

"""
####CHANGELOG####
V 1.16 - Realizado troca do banco de dados de INFLUXDB para POSTGRESQL - Guilherme Luna 29/12/2025
V 1.15 - Adicionado função para coleta de dados de: Quantidade de produto armazenado, quantidade de palete escravos armazenados - Guilherme Luna 03/10/2025
V 1.14.2 - HOTFIX - script quebrando as 5 da manhã pois salvava o arquivo erraado ao resetar a contagem do dia anterior
    de {"entCong":0, "rejCong":0, "expCong":0}' para '{"entCong":0, "rejCong":0, "expCong":0, "entResf":0, "rejResf":0, "expResf":0}' - Guilherme Luna 20/09/2025
V 1.14.1 - Script retorna no console a hora atual de cada loop do codigo
V 1.14 - Adicionado Coleta e envio de dados Hora a Hora do transelevador resfriado - Guilherme Luna 19/09/2025
V 1.13 - Adicionado retentividade para as informações dos ultimos paletes hora - Guilherme Luna 19/09/2025
V 1.12 - Adicionado envio de dados para influx de dados Hora a Hora - Guilherme luna 18/09/2025
"""


