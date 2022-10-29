from bs4 import BeautifulSoup
from exceptiongroup import catch
from selenium import webdriver
import psycopg2 as pg
import time


def conexao_pg():
    conexao = pg.connect(user='postgres', password='postgres',
                         host='localhost', database='scraper')
    return conexao


def buscar_categorias():

    driver = webdriver.Firefox()
    url = 'https://andradas.portaldacidade.com/guia-comercial'
    driver.get(url)
    time.sleep(5)
    div_mae = driver.find_element("xpath", "/html/body/main/div[2]/div[4]")
    html_content = div_mae.get_attribute('outerHTML')
    soup = BeautifulSoup(html_content, 'html.parser')
    items = soup.find_all("div", {"class": "features__item-description"})

    # Abrindo a conexão com banco de dados
    db = conexao_pg()
    cursor = db.cursor()

    for grupos_categoria in items:
        for item_grupo in grupos_categoria:
            try:
                categoria = item_grupo.text
                url = item_grupo.get('href')
                sql = f"insert into categorias(nome, url) values ('{categoria}', '{url}')"
                cursor.execute(sql)
                print(categoria)
            except:
                print('...')

    db.commit()


buscar_categorias()
