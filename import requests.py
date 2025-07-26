import requests
from bs4 import BeautifulSoup
import pandas as pd
import time

BASE_URL = "https://www.unasus.gov.br"
SEARCH_URL = f"{BASE_URL}/cursos/busca?status=todos&busca=&ordenacao=por%20nome"
HEADERS = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"}

# Campos a coletar
CAMPOS = [
    "codigo_oferta", "data_incricao", "periodo_realizacao", "nome_curso", "link_curso", "carga_horaria", "vagas", "publico_alvo", "instituicao_ofertante", "formato", "nivel", "modalidade", "programa_de_governo", "matricula_ativa", "tem_deia", "qual_tipo_deia", "qual_sub_deia", "palavras_chave", "decs"
]

def get_soup(url):
    resp = requests.get(url, headers=HEADERS)
    resp.raise_for_status()
    return BeautifulSoup(resp.text, 'html.parser')

def extrair_links_cursos(soup):
    # Ajuste conforme o HTML real
    cursos = []
    for a in soup.select('a[href^="/curso/"]'):
        link = BASE_URL + a['href']
        nome = a.get_text(strip=True)
        cursos.append({"nome_curso": nome, "link_curso": link})
    return cursos

def extrair_dados_curso(link_curso):
    soup = get_soup(link_curso)
    dados = {campo: '' for campo in CAMPOS}
    dados["link_curso"] = link_curso
    # Exemplo de extração (ajuste os seletores conforme o HTML real)
    try:
        dados["nome_curso"] = soup.select_one('h1').get_text(strip=True)
    except Exception:
        pass
    # Adicione aqui a extração dos outros campos, por exemplo:
    # dados["codigo_oferta"] = soup.select_one('seletor').get_text(strip=True)
    # ...
    # Exemplo de DEIA:
    # if "diversidade" in soup.text.lower():
    #     dados["tem_deia"] = "Sim"
    #     dados["qual_tipo_deia"] = "Diversidade"
    #     dados["qual_sub_deia"] = "..."
    return dados

def proxima_pagina(soup):
    # Ajuste conforme o HTML real
    next_btn = soup.select_one('a[rel="next"]')
    if next_btn:
        return BASE_URL + next_btn['href']
    return None

def main():
    url = SEARCH_URL
    todos_cursos = []
    visitados = set()
    while url:
        print(f"Acessando: {url}")
        soup = get_soup(url)
        cursos = extrair_links_cursos(soup)
        for curso in cursos:
            if curso["link_curso"] in visitados:
                continue
            print(f"Extraindo: {curso['nome_curso']}")
            dados = extrair_dados_curso(curso["link_curso"])
            todos_cursos.append(dados)
            visitados.add(curso["link_curso"])
            time.sleep(1)  # Respeitar o site
        url = proxima_pagina(soup)
        time.sleep(2)
    df = pd.DataFrame(todos_cursos, columns=CAMPOS)
    df.to_csv("unasus_cursos.csv", index=False, encoding='utf-8-sig')
    print("Dados salvos em unasus_cursos.csv")

if __name__ == "__main__":
    main()
