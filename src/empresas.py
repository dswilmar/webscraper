from bs4 import BeautifulSoup
from selenium import webdriver
import psycopg2 as pg
import time


def conexao_pg():
    conexao = pg.connect(user='postgres', password='postgres',
                         host='localhost', database='scraper')
    return conexao


def buscar_categorias():
    # Abrindo a conexão com banco de dados
    db = conexao_pg()
    cursor = db.cursor()
    sql = 'select * from categorias where processada = 0 limit 1'
    cursor.execute(sql)
    consulta = cursor.fetchall()
    db.commit()
    db.close()
    return consulta


def inserir_empresa(nome, url):
    # Abrindo a conexão com banco de dados
    db = conexao_pg()
    cursor = db.cursor()
    sql = f"insert into empresas(nome, url) values ('{nome}', '{url}')"
    cursor.execute(sql)
    db.commit()
    db.close()


def buscar_empresas():
    categorias = buscar_categorias()

    for categoria in categorias:
        url_categoria = categoria[2]

        driver = webdriver.Firefox()
        driver.get(url_categoria)
        time.sleep(5)

        div_mae = driver.find_element(
            "xpath", "/html/body/main/section/div/section/div[4]")
        html_content = div_mae.get_attribute('outerHTML')
        soup = BeautifulSoup(html_content, 'html.parser')

        empresas_destacadas = soup.findAll(
            "a", {"class": "company-name grey-text text-darken-4 no-margin"})
        for empresa in empresas_destacadas:
            nome = empresa.text
            link = empresa.get('href')
            inserir_empresa(nome, link)

        empresas = soup.findAll(
            "a", {"class": "company-name grey-text text-darken-4"})
        for empresa in empresas:
            nome = empresa.text
            link = empresa.get('href')
            inserir_empresa(nome, link)


buscar_empresas()
