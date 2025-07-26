import os
import re
import time

import pandas as pd
import requests
from bs4 import BeautifulSoup

# Configurações da API (CORRIGIDAS)
url = "https://www.unasus.gov.br/cursos/rest/busca"
headers = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/138.0.0.0 Safari/537.36"
    ),
    "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",  # CORRIGIDO!
    "Accept": "application/json, text/javascript, */*; q=0.01",
    "X-Requested-With": "XMLHttpRequest",
    "Origin": "https://www.unasus.gov.br",
    "Referer": (
        "https://www.unasus.gov.br/cursos/busca?status=todos&busca="
        "&ordenacao=Relev%C3%A2ncia%20na%20busca"
    ),
}

cookies = {
    "PORTAL_UNASUS": "4ru34cs848mfbopb6vseqluni4",
    "UNASUSAnonID": "ID1ef7d6246158f7cf31c06b928bc56f8e",
    "_shibsession_64656661756c7468747470733a2f2f7777772e756e617375732e676f762e6272": (
        "_329a72cffc11d2904ae393c82d0cfb72"
    ),
}

payload = {"busca": "", "ordenacao": "Por nome", "status": "Todos", "proximo": 0}

descritores = [
    "Diversidade, Equidade e Integração",
    "Diversidade, Equidade, Inclusão e Pertencimento",
    "Diversidade, Equidade, Inclusão, Acessibilidade",
    "Diversidade, Equidade, Inclusão, Pertencimento",
    "Diversidade, Igualdade e Inclusão",
    "Diversidade, Igualdade, Inclusão e Acessibilidade",
    "Diversidade, Igualdade, Inclusão, Pertencimento",
    "Equidade, Diversidade e Inclusão",
    "Inclusão, Diversidade, Equidade e Acessibilidade",
    "Inclusão, Diversidade, Equidade, Acessibilidade",
]


def encontrar_descritor(titulo, descricao, descritores):
    """Encontra descritores DEIA no título e descrição do curso."""
    texto = (titulo or "") + " " + (descricao or "")
    for descritor in descritores:
        if descritor.lower() in texto.lower():
            return descritor
    return ""


def extrair_ofertas_do_curso(id_curso):
    """Extrai ofertas de um curso específico com logs detalhados."""
    url_curso = f"https://www.unasus.gov.br/cursos/curso/{id_curso}"
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
            ofertas_encerradas = buscar_ofertas_encerradas(soup, url_curso)
            ofertas.extend(ofertas_encerradas)

        # 3. Buscar por divs que possam conter ofertas
        divs_oferta = soup.find_all("div", class_=lambda c: c and "oferta" in c.lower())
        if divs_oferta:
            print(f"  📋 Encontrados {len(divs_oferta)} divs com 'oferta' na classe")

        # 4. Verificar se há JavaScript que carrega ofertas dinamicamente
        scripts = soup.find_all("script")
        scripts_com_oferta = [
            s for s in scripts if s.string and "oferta" in s.string.lower()
        ]
        if scripts_com_oferta:
            print(f"  📋 Encontrados {len(scripts_com_oferta)} scripts com 'oferta'")

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


def buscar_ofertas_encerradas(soup, url_curso):
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


def extrair_dados_oferta(id_oferta):
    """Extrai dados de uma oferta usando a API REST."""
    url_oferta = f"https://www.unasus.gov.br/cursos/oferta/{id_oferta}"
    url_api = f"https://www.unasus.gov.br/cursos/rest/oferta/{id_oferta}"

    try:
        print(f"  🔍 Extraindo dados da oferta {id_oferta}...")

        # Primeiro, tentar a API REST
        api_headers = {
            "User-Agent": (
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                "AppleWebKit/537.36 (KHTML, like Gecko) "
                "Chrome/138.0.0.0 Safari/537.36"
            ),
            "Accept": "application/json, text/javascript, */*; q=0.01",
            "X-Requested-With": "XMLHttpRequest",
            "Referer": url_oferta,
        }

        dados = {"id_oferta": id_oferta, "url_oferta": url_oferta}
        dados["codigo_oferta"] = id_oferta

        # Tentar API REST primeiro
        try:
            resp_api = requests.get(url_api, headers=api_headers, timeout=30)
            if resp_api.status_code == 200:
                response_data = resp_api.json()
                print("    ✅ Dados obtidos via API REST")

                # Os dados estão dentro do campo 'data'
                oferta_data = response_data.get("data", {})

                # Extrair dados da resposta JSON
                dados["vagas"] = str(oferta_data.get("qt_vaga", ""))
                dados["publico_alvo"] = oferta_data.get("ds_publico_alvo", "")
                dados["local_oferta"] = oferta_data.get("no_local_oferta", "")
                dados["formato"] = oferta_data.get("no_formato", "")

                # Programas de governo podem ser uma lista
                programas = oferta_data.get("no_programas_governo", [])
                if isinstance(programas, list):
                    dados["programas_governo"] = ", ".join(programas)
                else:
                    dados["programas_governo"] = str(programas) if programas else ""

                # Temas podem ser uma lista
                temas = oferta_data.get("no_temas", [])
                if isinstance(temas, list):
                    dados["temas"] = ", ".join(temas)
                else:
                    dados["temas"] = str(temas) if temas else ""

                # DeCs podem ser uma lista
                decs = oferta_data.get("no_decs", [])
                if isinstance(decs, list):
                    dados["decs"] = ", ".join(decs)
                else:
                    dados["decs"] = str(decs) if decs else ""

                dados["descricao_oferta"] = oferta_data.get("ds_oferta", "")

                # Palavras-chave podem ser uma lista
                palavras_chave = oferta_data.get("no_palavras_chave", [])
                if isinstance(palavras_chave, list):
                    dados["palavras_chave"] = ", ".join(palavras_chave)
                else:
                    dados["palavras_chave"] = (
                        str(palavras_chave) if palavras_chave else ""
                    )

                if dados["vagas"]:
                    print(f"    ✅ Vagas extraídas: {dados['vagas']}")
                else:
                    print("    ⚠️ Vagas não encontradas na API")

                return dados
            else:
                print(f"    ⚠️ API REST retornou status {resp_api.status_code}")
        except Exception as e:
            print(f"    ⚠️ Erro na API REST: {e}")

        # Fallback: tentar extrair da página HTML
        print("    🔄 Tentando extração da página HTML...")
        resp = requests.get(url_oferta, headers=headers, timeout=30)
        soup = BeautifulSoup(resp.text, "html.parser")

        # Buscar o div principal com os dados da oferta
        oferta_quadro = soup.find("div", id="oferta_quadro")
        if oferta_quadro:
            texto_completo = oferta_quadro.get_text()

            # Extrair vagas usando regex para encontrar o padrão "Vagas: número"
            vagas_match = re.search(r"Vagas:\s*(\d+)", texto_completo)
            dados["vagas"] = vagas_match.group(1) if vagas_match else ""

            # Extrair público-alvo
            publico_match = re.search(
                r"Público-alvo:\s*(.*?)(?=\n\n|\nLocal|\nFormato|\nNível|\nModalidade|\nProgramas|\nTemas|\nDeCs|\nDescrição|\nPalavras-chave|$)",
                texto_completo,
                re.DOTALL,
            )
            dados["publico_alvo"] = (
                publico_match.group(1).strip() if publico_match else ""
            )

            # Extrair local da oferta
            local_match = re.search(
                r"Local da Oferta:\s*(.*?)(?=\n\n|\nFormato|\nNível|\nModalidade|\nProgramas|\nTemas|\nDeCs|\nDescrição|\nPalavras-chave|$)",
                texto_completo,
                re.DOTALL,
            )
            dados["local_oferta"] = local_match.group(1).strip() if local_match else ""

            # Extrair formato
            formato_match = re.search(
                r"Formato:\s*(.*?)(?=\n\n|\nNível|\nModalidade|\nProgramas|\nTemas|\nDeCs|\nDescrição|\nPalavras-chave|$)",
                texto_completo,
                re.DOTALL,
            )
            dados["formato"] = formato_match.group(1).strip() if formato_match else ""

            # Extrair programas de governo
            programas_match = re.search(
                r"Programas de governo:\s*(.*?)(?=\n\n|\nTemas|\nDeCs|\nDescrição|\nPalavras-chave|$)",
                texto_completo,
                re.DOTALL,
            )
            dados["programas_governo"] = (
                programas_match.group(1).strip() if programas_match else ""
            )

            # Extrair temas
            temas_match = re.search(
                r"Temas:\s*(.*?)(?=\n\n|\nDeCs|\nDescrição|\nPalavras-chave|$)",
                texto_completo,
                re.DOTALL,
            )
            dados["temas"] = temas_match.group(1).strip() if temas_match else ""

            # Extrair DeCs
            decs_match = re.search(
                r"DeCs:\s*(.*?)(?=\n\n|\nDescrição|\nPalavras-chave|$)",
                texto_completo,
                re.DOTALL,
            )
            dados["decs"] = decs_match.group(1).strip() if decs_match else ""

            # Extrair descrição da oferta
            descricao_match = re.search(
                r"Descrição da oferta:\s*(.*?)(?=\n\n|\nPalavras-chave|$)",
                texto_completo,
                re.DOTALL,
            )
            dados["descricao_oferta"] = (
                descricao_match.group(1).strip() if descricao_match else ""
            )

            # Extrair palavras-chave
            palavras_match = re.search(
                r"Palavras-chave:\s*(.*?)(?=\n\n|$)", texto_completo, re.DOTALL
            )
            dados["palavras_chave"] = (
                palavras_match.group(1).strip() if palavras_match else ""
            )

        else:
            # Fallback para estrutura antiga (tabela)
            dados["vagas"] = ""
            dados["publico_alvo"] = ""
            dados["local_oferta"] = ""
            dados["formato"] = ""
            dados["programas_governo"] = ""
            dados["temas"] = ""
            dados["decs"] = ""
            dados["descricao_oferta"] = ""
            dados["palavras_chave"] = ""

            # Tentar extrair usando a estrutura de tabela antiga
            vagas = soup.find(string=lambda t: t and "Vagas" in t)
            if vagas:
                try:
                    dados["vagas"] = vagas.parent.find_next("td").text.strip()
                except Exception:
                    dados["vagas"] = ""

            publico = soup.find(string=lambda t: t and "Público-alvo" in t)
            if publico:
                try:
                    dados["publico_alvo"] = publico.parent.find_next("td").text.strip()
                except Exception:
                    dados["publico_alvo"] = ""

            local = soup.find(string=lambda t: t and "Local" in t)
            if local:
                try:
                    dados["local_oferta"] = local.parent.find_next("td").text.strip()
                except Exception:
                    dados["local_oferta"] = ""

            formato = soup.find(string=lambda t: t and "Formato" in t)
            if formato:
                try:
                    dados["formato"] = formato.parent.find_next("td").text.strip()
                except Exception:
                    dados["formato"] = ""

            programas = soup.find(string=lambda t: t and "Programas de governo" in t)
            if programas:
                try:
                    dados["programas_governo"] = programas.parent.find_next(
                        "td"
                    ).text.strip()
                except Exception:
                    dados["programas_governo"] = ""

            temas = soup.find(string=lambda t: t and "Temas" in t)
            if temas:
                try:
                    dados["temas"] = temas.parent.find_next("td").text.strip()
                except Exception:
                    dados["temas"] = ""

            decs = soup.find(string=lambda t: t and "DeCs" in t)
            if decs:
                try:
                    dados["decs"] = decs.parent.find_next("td").text.strip()
                except Exception:
                    dados["decs"] = ""

            descricao = soup.find(string=lambda t: t and "Descrição da oferta" in t)
            if descricao:
                try:
                    dados["descricao_oferta"] = descricao.parent.find_next(
                        "td"
                    ).text.strip()
                except Exception:
                    dados["descricao_oferta"] = ""

            palavras = soup.find(string=lambda t: t and "Palavras-chave" in t)
            if palavras:
                try:
                    dados["palavras_chave"] = palavras.parent.find_next(
                        "td"
                    ).text.strip()
                except Exception:
                    dados["palavras_chave"] = ""

        return dados
    except Exception as e:
        print(f"Erro ao buscar dados da oferta {id_oferta}: {e}")
        return {"id_oferta": id_oferta, "erro": str(e)}


def carregar_ids_processados(csv_path):
    """Carrega IDs de cursos já processados do CSV existente."""
    if not os.path.exists(csv_path):
        return set()
    try:
        df_existente = pd.read_csv(csv_path, encoding="utf-8-sig")
        # Verifica qual coluna de ID existe
        if "co_seq_curso" in df_existente.columns:
            return set(df_existente["co_seq_curso"].astype(str).unique())
        elif "id_curso" in df_existente.columns:
            return set(df_existente["id_curso"].astype(str).unique())
        elif "co_curso" in df_existente.columns:
            return set(df_existente["co_curso"].astype(str).unique())
        else:
            print("Nenhuma coluna de ID de curso encontrada no CSV existente")
            return set()
    except Exception as e:
        print(f"Erro ao carregar CSV existente: {e}")
        return set()


# Loop principal do scraper
todos_detalhes = []
pagina = 0
csv_path = "unasus_ofertas_detalhadas.csv"
lote = 10  # Salva a cada 10 cursos
cursos_processados = carregar_ids_processados(csv_path)
print(f"Cursos já processados: {len(cursos_processados)}")
print(f"Arquivo de saída: {csv_path}")

while True:
    try:
        # CORREÇÃO: usar data=payload em vez de json=payload
        resp = requests.post(
            url,
            data=payload,  # CORRIGIDO!
            headers=headers,
            cookies=cookies,  # CORRIGIDO!
            timeout=30,
        )
        data = resp.json()
        itens = data.get("results", {}).get("itens", [])
        if not itens:
            break
        for curso in itens:
            id_curso = (
                curso.get("co_seq_curso")
                or curso.get("id_curso")
                or curso.get("co_curso")
                or curso.get("id")
            )
            if not id_curso:
                continue
            id_curso_str = str(id_curso)
            if id_curso_str in cursos_processados:
                continue  # Pula cursos já processados
            titulo = curso.get("no_curso", "")
            descricao = curso.get("ds_curso", "")
            encontrado = encontrar_descritor(titulo, descricao, descritores)
            curso["tem_deia"] = "Sim" if encontrado else "Não"
            curso["deia_encontrado"] = encontrado
            ofertas = extrair_ofertas_do_curso(id_curso)
            if not ofertas:
                todos_detalhes.append(
                    {**curso, "id_oferta": "", "erro": "Sem ofertas encontradas"}
                )
            for id_oferta in ofertas:
                dados_oferta = extrair_dados_oferta(id_oferta)
                linha = {**curso, **dados_oferta}
                todos_detalhes.append(linha)
                time.sleep(1)
            cursos_processados.add(id_curso_str)
            # Salvamento incremental
            if len(todos_detalhes) >= lote:
                if os.path.exists(csv_path):
                    df_existente = pd.read_csv(csv_path, encoding="utf-8-sig")
                    df_novo = pd.DataFrame(todos_detalhes)
                    df_final = pd.concat([df_existente, df_novo], ignore_index=True)
                else:
                    df_final = pd.DataFrame(todos_detalhes)
                df_final.to_csv(csv_path, index=False, encoding="utf-8-sig")
                print(
                    f"Progresso salvo após {len(cursos_processados)} cursos em {csv_path}"
                )
                todos_detalhes = []
        pagina += 1
        print(f"Página {pagina} processada.")
        proximo = data.get("results", {}).get("proximo")
        if not proximo:
            break
        payload["proximo"] = proximo
        time.sleep(1)
    except Exception as e:
        print(f"Erro de conexão: {e}. Tentando novamente em 30 segundos...")
        time.sleep(30)
        continue

# Salva o restante
if todos_detalhes:
    if os.path.exists(csv_path):
        df_existente = pd.read_csv(csv_path, encoding="utf-8-sig")
        df_novo = pd.DataFrame(todos_detalhes)
        df_final = pd.concat([df_existente, df_novo], ignore_index=True)
    else:
        df_final = pd.DataFrame(todos_detalhes)
    df_final.to_csv(csv_path, index=False, encoding="utf-8-sig")
    print(f"Finalizado! Todos os dados salvos em {csv_path}")
else:
    print("Nenhum dado detalhado coletado.")
