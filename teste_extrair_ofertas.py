import requests
from bs4 import BeautifulSoup


def testar_extrair_ofertas():
    """Testa a extração de ofertas de um curso específico."""

    # Primeiro, vamos pegar um curso da API
    url_api = "https://www.unasus.gov.br/cursos/rest/busca"
    headers = {
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/138.0.0.0 Safari/537.36"
        ),
        "Content-Type": "application/json",
    }
    payload = {"busca": "", "ordenacao": "Por nome", "status": "Todos", "proximo": 0}

    try:
        print("Consultando API para obter um curso...")
        resp = requests.post(url_api, json=payload, headers=headers, timeout=30)

        if resp.status_code == 200:
            data = resp.json()
            itens = data.get("results", {}).get("itens", [])

            if itens:
                # Pegar o primeiro curso
                curso = itens[0]
                id_curso = curso.get("co_seq_curso") or curso.get("id_curso")
                nome_curso = curso.get("no_curso", "N/A")

                print(f"Testando curso: {nome_curso}")
                print(f"ID do curso: {id_curso}")

                # Testar extração de ofertas
                ofertas = extrair_ofertas_do_curso(id_curso)

                print(f"Ofertas encontradas: {len(ofertas)}")
                if ofertas:
                    print("IDs das ofertas:")
                    for i, oferta in enumerate(ofertas[:5]):
                        print(f"  {i+1}. {oferta}")
                else:
                    print("Nenhuma oferta encontrada")

                    # Vamos verificar a estrutura da página do curso
                    print("\nVerificando estrutura da página do curso...")
                    verificar_estrutura_pagina(id_curso)
            else:
                print("Nenhum curso encontrado na API")
        else:
            print(f"Erro HTTP: {resp.status_code}")

    except Exception as e:
        print(f"Erro ao consultar API: {e}")


def extrair_ofertas_do_curso(id_curso):
    """Extrai ofertas de um curso específico."""
    url_curso = f"https://www.unasus.gov.br/cursos/curso/{id_curso}"
    headers = {
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/138.0.0.0 Safari/537.36"
        )
    }

    try:
        print(f"Buscando ofertas do curso {id_curso}...")
        resp = requests.get(url_curso, headers=headers, timeout=30)

        if resp.status_code != 200:
            print(f"Erro HTTP {resp.status_code} ao acessar curso {id_curso}")
            return []

        soup = BeautifulSoup(resp.text, "html.parser")
        ofertas = []

        # Buscar links de ofertas de várias formas
        links_encontrados = []

        # 1. Buscar links diretos de ofertas
        for link in soup.find_all("a", href=True):
            href = link["href"]
            links_encontrados.append(href)

            # Verifica diferentes padrões de URL de oferta
            if any(
                pattern in href
                for pattern in ["/cursos/oferta/", "../oferta/", "oferta/"]
            ):
                # Extrai o ID da oferta do final da URL
                id_oferta = href.split("/")[-1]
                if id_oferta.isdigit():
                    ofertas.append(id_oferta)
                    print(f"  ✅ Oferta encontrada: {id_oferta}")

        # 2. Buscar por botões ou links que possam mostrar ofertas encerradas
        botoes_encerradas = soup.find_all(
            "a", string=lambda t: t and "encerrada" in t.lower()
        )
        if botoes_encerradas:
            print(
                f"  📋 Encontrados {len(botoes_encerradas)} links de ofertas encerradas"
            )
            for botao in botoes_encerradas:
                print(f"    - {botao.get_text().strip()}")

            # Tentar acessar as ofertas encerradas
            ofertas_encerradas = buscar_ofertas_encerradas(soup, url_curso, headers)
            ofertas.extend(ofertas_encerradas)

        ofertas_unicas = list(set(ofertas))  # Remove duplicados

        if ofertas_unicas:
            print(f"  ✅ Total de ofertas únicas encontradas: {len(ofertas_unicas)}")
        else:
            print(f"  ❌ Nenhuma oferta encontrada para o curso {id_curso}")
            print(f"  📋 Total de links na página: {len(links_encontrados)}")
            print(f"  📋 Primeiros 5 links: {links_encontrados[:5]}")

        return ofertas_unicas

    except Exception as e:
        print(f"Erro ao buscar ofertas do curso {id_curso}: {e}")
        return []


def buscar_ofertas_encerradas(soup, url_curso, headers):
    """Busca ofertas encerradas na página do curso."""
    ofertas_encerradas = []

    try:
        # Procurar por links que contenham "encerrada" ou "encerradas"
        links_encerradas = soup.find_all(
            "a",
            href=True,
            string=lambda t: t
            and any(palavra in t.lower() for palavra in ["encerrada", "encerradas"]),
        )

        for link in links_encerradas:
            href = link.get("href")
            if href:
                # Se for um link relativo, construir URL completa
                if href.startswith("/"):
                    url_encerradas = f"https://www.unasus.gov.br{href}"
                elif href.startswith("http"):
                    url_encerradas = href
                else:
                    # URL relativa ao curso
                    url_encerradas = f"{url_curso}/{href}"

                print(f"  🔍 Acessando ofertas encerradas: {url_encerradas}")

                # Acessar a página de ofertas encerradas
                resp_encerradas = requests.get(
                    url_encerradas, headers=headers, timeout=30
                )
                if resp_encerradas.status_code == 200:
                    soup_encerradas = BeautifulSoup(resp_encerradas.text, "html.parser")

                    # Buscar links de ofertas na página de encerradas
                    for link_oferta in soup_encerradas.find_all("a", href=True):
                        href_oferta = link_oferta["href"]
                        if "/cursos/oferta/" in href_oferta:
                            id_oferta = href_oferta.split("/")[-1]
                            if id_oferta.isdigit():
                                ofertas_encerradas.append(id_oferta)
                                print(
                                    f"    ✅ Oferta encerrada encontrada: {id_oferta}"
                                )

        return ofertas_encerradas

    except Exception as e:
        print(f"Erro ao buscar ofertas encerradas: {e}")
        return []


def verificar_estrutura_pagina(id_curso):
    """Verifica a estrutura da página do curso para entender por que não há ofertas."""
    url_curso = f"https://www.unasus.gov.br/cursos/curso/{id_curso}"
    headers = {
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/138.0.0.0 Safari/537.36"
        )
    }

    try:
        resp = requests.get(url_curso, headers=headers, timeout=30)
        soup = BeautifulSoup(resp.text, "html.parser")

        print(f"Status da resposta: {resp.status_code}")
        print(f"Tamanho da página: {len(resp.text)} caracteres")

        # Verificar se há links de ofertas
        links = soup.find_all("a", href=True)
        links_oferta = [link for link in links if "/cursos/oferta/" in link["href"]]

        print(f"Total de links encontrados: {len(links)}")
        print(f"Links de ofertas encontrados: {len(links_oferta)}")

        if links_oferta:
            print("Links de ofertas:")
            for link in links_oferta[:5]:
                print(f"  - {link['href']}")
        else:
            print("Nenhum link de oferta encontrado")

            # Verificar se há botão "mostrar ofertas encerradas"
            botoes = soup.find_all("button")
            links_encerradas = soup.find_all(
                "a", string=lambda t: t and "encerrada" in t.lower()
            )

            print(f"Botões encontrados: {len(botoes)}")
            print(f"Links com 'encerrada': {len(links_encerradas)}")

            for link in links_encerradas:
                print(f"  - {link.get_text().strip()}")

    except Exception as e:
        print(f"Erro ao verificar estrutura: {e}")


if __name__ == "__main__":
    testar_extrair_ofertas()
