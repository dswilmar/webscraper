from bs4 import BeautifulSoup
from selenium import webdriver
import time
import psycopg2 as pg


def conexao_pg():
    conexao = pg.connect(user='postgres', password='postgres',
                         host='localhost', database='scraper')
    return conexao


def buscar_empresas_processar():
    # Abrindo a conexão com banco de dados
    db = conexao_pg()
    cursor = db.cursor()
    sql = "select id, nome, url from empresas where telefone='' order by id"
    cursor.execute(sql)
    consulta = cursor.fetchall()
    db.commit()
    db.close()
    return consulta


def atualizar_empresa(id, telefone, endereco, site, facebook, instagram):
    db = conexao_pg()
    cursor = db.cursor()
    sql = f"update empresas set telefone= %s, endereco= %s, site= %s, fb= %s, ig= %s where id= {id}"
    cursor.execute(sql, [telefone, endereco, site, facebook, instagram])
    db.commit()
    db.close()


def buscar_dados_empresa():
    empresas = buscar_empresas_processar()

    for empresa in empresas:
        anuncio_padrao = False
        url = empresa[2]
        id_empresa = empresa[0]

        driver = webdriver.Firefox()
        driver.get(url)
        time.sleep(5)

        endereco = ""
        telefone = ""
        site = ""
        facebook = ""
        instagram = ""

        try:
            div_telefone = driver.find_element(
                "xpath", "/html/body/main/div[3]/section/div[1]/div[2]/div")
            content_telefone = div_telefone.get_attribute('outerHTML')
            soup_telefone = BeautifulSoup(content_telefone, 'html.parser')
            a_telefone = soup_telefone.find_all("a")
            telefone = str(a_telefone[0].get('href').replace("tel:", ""))
            anuncio_padrao = True
        except:
            print("Ops! Telefone nao encontrado")

        try:
            div_endereco = driver.find_element(
                "xpath", "/html/body/main/div[3]/section/div[1]/div[2]")
            html_content = div_endereco.get_attribute('outerHTML')
            soup = BeautifulSoup(html_content, 'html.parser')
            soup.find("br").replaceWith(" - ")
            p_endereco = soup.find_all("p", {"class": "text-md"})
            endereco = p_endereco[0].text
            anuncio_padrao = True
        except:
            print("Ops! Endereco nao encontrado")

        try:
            if not anuncio_padrao:
                div_detalhes = driver.find_element(
                    "xpath", "/html/body/main/div[2]/div[3]/section/div[1]/div/div[2]")
                conteudo_detalhes = div_detalhes.get_attribute("outerHTML")
                soup_detalhes = BeautifulSoup(conteudo_detalhes, 'html.parser')
                p_detalhes_endereco = soup_detalhes.find_all(
                    "p", {"itemprop": "address"})
                a_detalhes_telefone = soup_detalhes.find_all("a")
                telefone = a_detalhes_telefone[0].get(
                    'href').replace("tel:", "").strip()
                endereco = p_detalhes_endereco[0].text.strip()
                # endereco = endereco.replace('<br>', ' - ')

                links_social = soup_detalhes.find_all("a")
                for link in links_social:
                    href = link.get('href')
                    if (href.__contains__('instagram')):
                        instagram = href

                    if (href.__contains__('facebook')):
                        facebook = href

                    if (href.__contains__('.com.br')):
                        site = href

        except Exception as e:
            print("Ocorreu um erro ao buscar os dados da empresa: " + str(e))

        try:
            print('Atualizando: ' + telefone + ' ' + endereco +
                  ' ' + site + ' ' + facebook + ' ' + instagram)
            atualizar_empresa(id_empresa, telefone, endereco,
                              site, facebook, instagram)
        except Exception as e:
            print("Erro ao atualizar a empresa " +
                  str(id_empresa) + ": " + str(e))

        driver.close()


buscar_dados_empresa()
