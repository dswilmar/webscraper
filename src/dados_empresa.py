from bs4 import BeautifulSoup
from selenium import webdriver
import time
import psycopg2 as pg


def conexao_pg():
    conexao = pg.connect(user='postgres', password='postgres',
                         host='localhost', database='scraper')
    return conexao


def buscar_dados_empresa():
    #url = f"https://andradas.portaldacidade.com/guia-comercial/andradas/adubos-real"
    url = "https://andradas.portaldacidade.com/guia-comercial/andradas/comercial-fertisolo"
    driver = webdriver.Firefox()
    driver.get(url)
    time.sleep(5)

    endereco = ""
    telefone = ""
    site = ""
    facebook = ""
    instagram = ""

    try:
        div_endereco = driver.find_element(
            "xpath", "/html/body/main/div[2]/section/div[1]/div[2]/p[2]")
        html_content = div_endereco.get_attribute('outerHTML')
        soup = BeautifulSoup(html_content, 'html.parser')
        endereco = soup.find_all("p", {"class": "text-md"})

        div_telefone = driver.find_element(
            "xpath", "/html/body/main/div[2]/section/div[1]/div[2]/div")
        content_telefone = div_telefone.get_attribute('outerHTML')
        soup_telefone = BeautifulSoup(content_telefone, 'html.parser')
        a_telefone = soup_telefone.find_all("a")
        telefone = a_telefone[0].get('href').replace("tel:", "")

        print(endereco + " " + telefone)
    except:
        print("Ops! Endereco e telefone nao encontrados...")

    try:
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

        links_social = soup_detalhes.find_all("a")
        for link in links_social:
            href = link.get('href')
            if (href.__contains__('instagram')):
                instagram = href

            if (href.__contains__('facebook')):
                facebook = href

            if (href.__contains__('.com.br')):
                site = href

    except:
        print("Ocorreu um erro ao buscar os dados da empresa...")


buscar_dados_empresa()
