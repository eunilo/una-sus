#!/usr/bin/env python3
"""
🧠 Scraper UNA-SUS - Versão Grounded Theory
===========================================

Esta é uma versão modificável do scraper_unasus_melhorado.py criada especificamente
para aplicação da metodologia Grounded Theory em pesquisas educacionais.

🎯 PROPÓSITO:
- Versão modificável para pesquisa qualitativa
- Adapte critérios conforme necessidades da sua pesquisa
- Processo iterativo de coleta e análise
- Sistema de backup seguro

📋 COMO USAR:
1. Modifique os descritores DEIA conforme sua pesquisa
2. Ajuste campos coletados se necessário
3. Execute o scraper e analise os resultados
4. Refine critérios baseado nos insights
5. Repita até saturação teórica

💾 BACKUP:
- Mantenha o arquivo scraper_unasus_backup_original.py intacto
- Use como ponto de retorno se necessário

🔬 METODOLOGIA:
- Grounded Theory: desenvolvimento de teorias a partir dos dados
- Coleta e análise simultâneas
- Comparação constante entre dados
- Saturação teórica como critério de parada

📚 Para mais informações, consulte:
- README_Grounded_Theory.md
- Documentação principal do projeto
"""

import json
import logging
import os
import re
import time
from datetime import datetime
from typing import Dict, List, Set

import pandas as pd
import requests
from bs4 import BeautifulSoup

# Configurações da API
URL = "https://www.unasus.gov.br/cursos/rest/busca"
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36",
    "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
    "Accept": "application/json, text/javascript, */*; q=0.01",
    "X-Requested-With": "XMLHttpRequest",
    "Origin": "https://www.unasus.gov.br",
    "Referer": "https://www.unasus.gov.br/cursos/busca?status=todos&busca=&ordenacao=Relev%C3%A2ncia%20na%20busca",
}
COOKIES = {
    "PORTAL_UNASUS": "4ru34cs848mfbopb6vseqluni4",
    "UNASUSAnonID": "ID1ef7d6246158f7cf31c06b928bc56f8e",
    "_shibsession_64656661756c7468747470733a2f2f7777772e756e617375732e676f762e6272": "_329a72cffc11d2904ae393c82d0cfb72",
}
PAYLOAD_INICIAL = {
    "busca": "",
    "ordenacao": "Por nome",
    "status": "Todos",
    "proximo": 0,
}

# Descritores DEIA expandidos
DESCRITORES_DEIA = [
    # Descritores originais
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
    # Novos descritores e variações
    "Diversidade e Inclusão",
    "Equidade e Inclusão",
    "Diversidade, Equidade e Inclusão",
    "Inclusão e Diversidade",
    "Equidade e Diversidade",
    "Acessibilidade e Inclusão",
    "Diversidade, Equidade, Inclusão e Acessibilidade",
    "Inclusão, Equidade e Diversidade",
    "Diversidade, Inclusão e Equidade",
    "Equidade, Inclusão e Diversidade",
    # Termos individuais relacionados
    "Diversidade",
    "Equidade",
    "Inclusão",
    "Acessibilidade",
    "Pertencimento",
    "Inclusivo",
    "Inclusiva",
    "Diverso",
    "Diversa",
    "Equitativo",
    "Equitativa",
    "Acessível",
    # Termos específicos de saúde
    "Saúde Mental",
    "Saúde da População Negra",
    "Saúde Indígena",
    "Saúde LGBTQI+",
    "Saúde da Mulher",
    "Saúde do Idoso",
    "Saúde da Criança",
    "Saúde do Adolescente",
    "Saúde da Pessoa com Deficiência",
    "Saúde da População em Situação de Rua",
    "Saúde da População Privada de Liberdade",
    "Saúde da População do Campo",
    "Saúde da População da Floresta",
    "Saúde da População das Águas",
    # Termos de vulnerabilidade social
    "Vulnerabilidade Social",
    "População Vulnerável",
    "Grupos Vulneráveis",
    "População em Situação de Rua",
    "População Privada de Liberdade",
    "População do Campo",
    "População da Floresta",
    "População das Águas",
    "População Negra",
    "População Indígena",
    "População LGBTQI+",
    "Pessoa com Deficiência",
    "Pessoas com Deficiência",
    "Idoso",
    "Idosos",
    "Criança",
    "Crianças",
    "Adolescente",
    "Adolescentes",
    "Mulher",
    "Mulheres",
    "Homem",
    "Homens",
    "Trans",
    "Transgênero",
    "Transgênera",
    "Não-binário",
    "Não-binária",
    "Gay",
    "Lésbica",
    "Bissexual",
    "Pansexual",
    "Assexual",
    "Queer",
    "Intersexo",
    "Intersexual",
    "Negro",
    "Negra",
    "Negros",
    "Negras",
    "Indígena",
    "Indígenas",
    "Quilombola",
    "Quilombolas",
    "Ribeirinho",
    "Ribeirinhos",
    "Extrativista",
    "Extrativistas",
    "Pescador",
    "Pescadores",
    "Agricultor",
    "Agricultores",
    "Sem-terra",
    "Sem-terras",
    "Sem-teto",
    "Sem-tetos",
    "Refugiado",
    "Refugiada",
    "Refugiados",
    "Refugiadas",
    "Imigrante",
    "Imigrantes",
    "Migrantes",
    "Migrantes",
    "Deslocado",
    "Deslocada",
    "Deslocados",
    "Deslocadas",
    "Vítima de Violência",
    "Vítimas de Violência",
    "Sobrevivente de Violência",
    "Sobreviventes de Violência",
    "Vítima de Tráfico",
    "Vítimas de Tráfico",
    "Vítima de Exploração",
    "Vítimas de Exploração",
    "Vítima de Abuso",
    "Vítimas de Abuso",
    "Vítima de Discriminação",
    "Vítimas de Discriminação",
    "Vítima de Preconceito",
    "Vítimas de Preconceito",
    "Vítima de Racismo",
    "Vítimas de Racismo",
    "Vítima de Sexismo",
    "Vítimas de Sexismo",
    "Vítima de Homofobia",
    "Vítimas de Homofobia",
    "Vítima de Transfobia",
    "Vítimas de Transfobia",
    "Vítima de Lesbofobia",
    "Vítimas de Lesbofobia",
    "Vítima de Bifobia",
    "Vítimas de Bifobia",
    "Vítima de Gordofobia",
    "Vítimas de Gordofobia",
    "Vítima de Etarismo",
    "Vítimas de Etarismo",
    "Vítima de Capacitismo",
    "Vítimas de Capacitismo",
    "Vítima de Classismo",
    "Vítimas de Classismo",
    "Vítima de Xenofobia",
    "Vítimas de Xenofobia",
    "Vítima de Antissemitismo",
    "Vítimas de Antissemitismo",
    "Vítima de Islamofobia",
    "Vítimas de Islamofobia",
    "Vítima de Cristofobia",
    "Vítimas de Cristofobia",
    "Vítima de Ateofobia",
    "Vítimas de Ateofobia",
    "Vítima de Misoginia",
    "Vítimas de Misoginia",
    "Vítima de Misandria",
    "Vítimas de Misandria",
    "Vítima de Misantropia",
    "Vítimas de Misantropia",
    "Vítima de Misoginia",
    "Vítimas de Misoginia",
    "Vítima de Misandria",
    "Vítimas de Misandria",
    "Vítima de Misantropia",
    "Vítimas de Misantropia",
]


def setup_logging():
    """Configura o sistema de logging."""
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s",
        handlers=[
            logging.FileHandler("scraper_unasus_melhorado.log", encoding="utf-8"),
            logging.StreamHandler(),
        ],
    )
    return logging.getLogger(__name__)


def encontrar_descritor_deia_melhorado(texto_completo: str) -> str:
    """Busca descritores DEIA de forma mais abrangente."""
    if not texto_completo:
        return ""

    texto_lower = texto_completo.lower()
    descritores_encontrados = []

    for descritor in DESCRITORES_DEIA:
        if descritor.lower() in texto_lower:
            descritores_encontrados.append(descritor)

    # Retorna o descritor mais específico (mais longo) encontrado
    if descritores_encontrados:
        return max(descritores_encontrados, key=len)

    return ""


def extrair_texto_pagina_inicial(id_curso: str, logger: logging.Logger) -> str:
    """Extrai o texto completo da página inicial do curso."""
    url_curso = f"https://www.unasus.gov.br/cursos/curso/{id_curso}"

    try:
        response = requests.get(url_curso, headers=HEADERS, timeout=30)
        soup = BeautifulSoup(response.text, "html.parser")

        # Remove scripts e estilos
        for script in soup(["script", "style"]):
            script.decompose()

        # Extrai todo o texto da página
        texto_completo = soup.get_text()

        # Limpa o texto
        linhas = (linha.strip() for linha in texto_completo.splitlines())
        chunks = (frase.strip() for linha in linhas for frase in linha.split("  "))
        texto_limpo = " ".join(chunk for chunk in chunks if chunk)

        logger.debug(
            f"Texto da página inicial extraído para curso {id_curso}: {len(texto_limpo)} caracteres"
        )
        return texto_limpo

    except Exception as e:
        logger.error(
            f"Erro ao extrair texto da página inicial do curso {id_curso}: {e}"
        )
        return ""


def extrair_descricao_curso_melhorada(id_curso: str, logger: logging.Logger) -> str:
    """Extrai a descrição do curso de forma mais robusta."""
    url_curso = f"https://www.unasus.gov.br/cursos/curso/{id_curso}"

    try:
        response = requests.get(url_curso, headers=HEADERS, timeout=30)
        soup = BeautifulSoup(response.text, "html.parser")

        # Múltiplas estratégias para encontrar a descrição
        descricao = ""

        # 1. Buscar por seletores específicos
        selectores = [
            "div.descricao",
            "div.curso-descricao",
            "p.descricao",
            "div.conteudo",
            "div.curso-info",
            "section.descricao",
            ".descricao-curso",
            "div.curso-detalhes",
            "div.informacoes-curso",
            "div.sobre-curso",
            "div.apresentacao",
            "div.introducao",
        ]

        for seletor in selectores:
            elemento = soup.select_one(seletor)
            if elemento:
                descricao = elemento.get_text(strip=True)
                if descricao and len(descricao) > 50:
                    logger.debug(f"Descrição encontrada com seletor: {seletor}")
                    break

        # 2. Buscar por texto específico
        if not descricao:
            elementos = soup.find_all(
                string=lambda t: t
                and any(
                    palavra in t.lower()
                    for palavra in [
                        "descrição",
                        "sobre o curso",
                        "apresentação",
                        "introdução",
                        "objetivo",
                        "objetivos",
                        "público-alvo",
                        "público alvo",
                    ]
                )
            )

            for elemento in elementos:
                parent = elemento.parent
                if parent:
                    texto = parent.get_text(strip=True)
                    if len(texto) > 100:  # Tamanho mínimo para descrição
                        descricao = texto
                        break

        # 3. Buscar por meta tags
        if not descricao:
            meta_desc = soup.find("meta", attrs={"name": "description"})
            if meta_desc and meta_desc.get("content"):
                descricao = meta_desc["content"]

        logger.debug(
            f"Descrição extraída para curso {id_curso}: {len(descricao)} caracteres"
        )
        return descricao

    except Exception as e:
        logger.error(f"Erro ao extrair descrição do curso {id_curso}: {e}")
        return ""


def extrair_palavras_chave_curso(id_curso: str, logger: logging.Logger) -> str:
    """Extrai palavras-chave do curso."""
    url_curso = f"https://www.unasus.gov.br/cursos/curso/{id_curso}"

    try:
        response = requests.get(url_curso, headers=HEADERS, timeout=30)
        soup = BeautifulSoup(response.text, "html.parser")

        palavras_chave = ""

        # Buscar por meta tags de palavras-chave
        meta_keywords = soup.find("meta", attrs={"name": "keywords"})
        if meta_keywords and meta_keywords.get("content"):
            palavras_chave = meta_keywords["content"]

        # Buscar por tags ou elementos específicos
        if not palavras_chave:
            elementos = soup.find_all(
                string=lambda t: t and "palavras-chave" in t.lower()
            )

            for elemento in elementos:
                parent = elemento.parent
                if parent:
                    texto = parent.get_text(strip=True)
                    if "palavras-chave" in texto.lower():
                        palavras_chave = texto
                        break

        logger.debug(
            f"Palavras-chave extraídas para curso {id_curso}: {palavras_chave}"
        )
        return palavras_chave

    except Exception as e:
        logger.error(f"Erro ao extrair palavras-chave do curso {id_curso}: {e}")
        return ""


def analisar_deia_completo(curso: Dict, logger: logging.Logger) -> Dict:
    """Realiza análise DEIA completa em todos os campos do curso."""
    # Coleta todos os textos para análise
    textos_para_analise = []

    # Campos básicos
    titulo = curso.get("no_curso", "")
    descricao_curso = curso.get("ds_curso", "")
    descricao_oferta = curso.get("descricao_oferta", "")
    palavras_chave_curso = curso.get("palavras_chave_curso", "")
    palavras_chave_oferta = curso.get("palavras_chave", "")
    texto_pagina = curso.get("texto_pagina_inicial", "")

    # Adiciona todos os textos à lista
    if titulo:
        textos_para_analise.append(f"Título: {titulo}")
    if descricao_curso:
        textos_para_analise.append(f"Descrição do curso: {descricao_curso}")
    if descricao_oferta:
        textos_para_analise.append(f"Descrição da oferta: {descricao_oferta}")
    if palavras_chave_curso:
        textos_para_analise.append(f"Palavras-chave do curso: {palavras_chave_curso}")
    if palavras_chave_oferta:
        textos_para_analise.append(f"Palavras-chave da oferta: {palavras_chave_oferta}")
    if texto_pagina:
        textos_para_analise.append(f"Texto da página: {texto_pagina}")

    # Combina todos os textos
    texto_completo = " ".join(textos_para_analise)

    # Busca descritores DEIA
    descritor_encontrado = encontrar_descritor_deia_melhorado(texto_completo)

    # Atualiza o curso
    curso["tem_deia"] = "Sim" if descritor_encontrado else "Não"
    curso["deia_encontrado"] = descritor_encontrado
    curso["texto_analisado_deia"] = texto_completo[
        :1000
    ]  # Primeiros 1000 caracteres para debug

    if descritor_encontrado:
        logger.info(
            f"DEIA encontrado no curso {curso.get('co_seq_curso', 'N/A')}: {descritor_encontrado}"
        )

    return curso


def processar_curso_melhorado(
    curso: Dict, id_curso: str, logger: logging.Logger
) -> List[Dict]:
    """Processa um curso com coleta completa de dados."""
    # Extrai dados adicionais do curso
    logger.info(f"Processando curso {id_curso}: {curso.get('no_curso', 'N/A')}")

    # Extrai descrição do curso se não existir
    if not curso.get("ds_curso"):
        descricao = extrair_descricao_curso_melhorada(id_curso, logger)
        curso["ds_curso"] = descricao

    # Extrai palavras-chave do curso
    palavras_chave_curso = extrair_palavras_chave_curso(id_curso, logger)
    curso["palavras_chave_curso"] = palavras_chave_curso

    # Extrai texto da página inicial
    texto_pagina = extrair_texto_pagina_inicial(id_curso, logger)
    curso["texto_pagina_inicial"] = texto_pagina

    # Analisa DEIA em todos os campos
    curso = analisar_deia_completo(curso, logger)

    # Extrai ofertas (mantém a lógica existente)
    ofertas = extrair_ofertas_do_curso(id_curso, logger)

    if not ofertas:
        logger.warning(f"Curso {id_curso} sem ofertas")
        return [{**curso, "id_oferta": "", "erro": "Sem ofertas encontradas"}]

    # Processa ofertas
    dados_ofertas = []
    for j, id_oferta in enumerate(ofertas, 1):
        logger.info(f"  Oferta {j}/{len(ofertas)}: {id_oferta}")
        dados_oferta = extrair_dados_oferta(id_oferta, logger)
        linha = {**curso, **dados_oferta}

        if "rank" in linha:
            del linha["rank"]

        dados_ofertas.append(linha)
        time.sleep(1)

    return dados_ofertas


# Funções auxiliares (mantidas do código original)
def extrair_ofertas_do_curso(id_curso: str, logger: logging.Logger) -> List[str]:
    """Extrai ofertas de um curso específico com logs detalhados."""
    url_curso = f"https://www.unasus.gov.br/cursos/curso/{id_curso}"

    try:
        logger.info(f"Buscando ofertas do curso {id_curso}...")
        resp = requests.get(url_curso, headers=HEADERS, timeout=30)

        if resp.status_code != 200:
            logger.error(f"Erro HTTP {resp.status_code} ao acessar curso {id_curso}")
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
                    logger.info(f"  ✅ Oferta encontrada: {id_oferta}")

        # 2. Buscar por botões ou links que possam mostrar ofertas encerradas
        botoes_encerradas = soup.find_all(
            "a", string=lambda t: t and "encerrada" in t.lower()
        )
        if botoes_encerradas:
            logger.info(
                f"  📋 Encontrados {len(botoes_encerradas)} links de ofertas encerradas"
            )
            for botao in botoes_encerradas:
                logger.info(f"    - {botao.get_text().strip()}")

            # Tentar acessar as ofertas encerradas
            ofertas_encerradas = buscar_ofertas_encerradas(soup, url_curso, logger)
            ofertas.extend(ofertas_encerradas)

        # 3. Buscar por divs que possam conter ofertas
        divs_oferta = soup.find_all("div", class_=lambda c: c and "oferta" in c.lower())
        if divs_oferta:
            logger.info(
                f"  📋 Encontrados {len(divs_oferta)} divs com 'oferta' na classe"
            )

        # 4. Verificar se há JavaScript que carrega ofertas dinamicamente
        scripts = soup.find_all("script")
        scripts_com_oferta = [
            s for s in scripts if s.string and "oferta" in s.string.lower()
        ]
        if scripts_com_oferta:
            logger.info(
                f"  📋 Encontrados {len(scripts_com_oferta)} scripts com 'oferta'"
            )

        ofertas_unicas = list(set(ofertas))  # Remove duplicados

        if ofertas_unicas:
            logger.info(
                f"  ✅ Total de ofertas únicas encontradas: {len(ofertas_unicas)}"
            )
        else:
            logger.warning(f"  ❌ Nenhuma oferta encontrada para o curso {id_curso}")
            logger.info(f"  📋 Total de links na página: {len(links_encontrados)}")
            logger.info(f"  📋 Primeiros 5 links: {links_encontrados[:5]}")

        return ofertas_unicas

    except Exception as e:
        logger.error(f"Erro ao buscar ofertas do curso {id_curso}: {e}")
        return []


def buscar_ofertas_encerradas(
    soup: BeautifulSoup, url_curso: str, logger: logging.Logger
) -> List[str]:
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

                logger.info(f"  🔍 Acessando ofertas encerradas: {url_encerradas}")

                # Acessar a página de ofertas encerradas
                resp_encerradas = requests.get(
                    url_encerradas, headers=HEADERS, timeout=30
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
                                logger.info(
                                    f"    ✅ Oferta encerrada encontrada: {id_oferta}"
                                )

        return ofertas_encerradas

    except Exception as e:
        logger.error(f"Erro ao buscar ofertas encerradas: {e}")
        return []


def extrair_dados_oferta(id_oferta: str, logger: logging.Logger) -> Dict:
    """Extrai dados de uma oferta usando a API REST com fallback para HTML."""
    url_oferta = f"https://www.unasus.gov.br/cursos/oferta/{id_oferta}"
    url_api = f"https://www.unasus.gov.br/cursos/rest/oferta/{id_oferta}"

    try:
        logger.info(f"  🔍 Extraindo dados da oferta {id_oferta}...")

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
                logger.info("    ✅ Dados obtidos via API REST")

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
                    logger.info(f"    ✅ Vagas extraídas: {dados['vagas']}")
                else:
                    logger.warning("    ⚠️ Vagas não encontradas na API")

                return dados
            else:
                logger.warning(f"    ⚠️ API REST retornou status {resp_api.status_code}")
        except Exception as e:
            logger.warning(f"    ⚠️ Erro na API REST: {e}")

        # Fallback: tentar extrair da página HTML
        logger.info("    🔄 Tentando extração da página HTML...")
        resp = requests.get(url_oferta, headers=HEADERS, timeout=30)
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

        logger.debug(f"Oferta {id_oferta}: dados extraídos com sucesso")
        return dados

    except Exception as e:
        logger.error(f"Erro ao buscar dados da oferta {id_oferta}: {e}")
        return {"id_oferta": id_oferta, "erro": str(e)}


def main():
    """Função principal do scraper melhorado."""
    logger = setup_logging()
    logger.info("=== INICIANDO SCRAPER UNA-SUS MELHORADO ===")

    # Configurações
    csv_path = "unasus_ofertas_melhoradas.csv"
    lote = 10
    todos_detalhes = []
    pagina = 0
    cursos_processados = set()

    # Carregar dados existentes
    if os.path.exists(csv_path):
        try:
            df_existente = pd.read_csv(csv_path, encoding="utf-8-sig")
            if "co_seq_curso" in df_existente.columns:
                cursos_processados = set(
                    df_existente["co_seq_curso"].astype(str).unique()
                )
            logger.info(f"Cursos já processados: {len(cursos_processados)}")
        except Exception as e:
            logger.error(f"Erro ao carregar CSV existente: {e}")

    payload = PAYLOAD_INICIAL.copy()
    logger.info(f"Arquivo de saída: {csv_path}")

    # Loop principal
    while True:
        try:
            logger.info(f"=== PROCESSANDO PÁGINA {pagina + 1} ===")

            response = requests.post(
                URL,
                data=payload,
                headers=HEADERS,
                cookies=COOKIES,
                timeout=30,
            )

            data = response.json()
            itens = data.get("results", {}).get("itens", [])

            if not itens:
                logger.info("Nenhum item encontrado. Finalizando.")
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
                    continue

                # Processa o curso com as melhorias
                dados_curso = processar_curso_melhorado(curso, id_curso_str, logger)
                todos_detalhes.extend(dados_curso)
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
                    logger.info(
                        f"Progresso salvo: {len(cursos_processados)} cursos processados"
                    )
                    todos_detalhes = []

            pagina += 1
            proximo = data.get("results", {}).get("proximo")
            if not proximo:
                break
            payload["proximo"] = proximo
            time.sleep(1)

        except Exception as e:
            logger.error(f"Erro de conexão: {e}. Tentando novamente em 30 segundos...")
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
        logger.info(f"Finalizado! Todos os dados salvos em {csv_path}")

    # Gera relatório final
    try:
        df = pd.read_csv(csv_path, encoding="utf-8-sig")
        logger.info("=== RELATÓRIO FINAL ===")
        logger.info(f"Total de registros: {len(df)}")
        logger.info(f"Colunas: {list(df.columns)}")

        if "tem_deia" in df.columns:
            deia_stats = df["tem_deia"].value_counts()
            logger.info(f"Cursos com DEIA: {deia_stats.get('Sim', 0)}")
            logger.info(f"Cursos sem DEIA: {deia_stats.get('Não', 0)}")

            # Mostra alguns exemplos de cursos com DEIA
            if deia_stats.get("Sim", 0) > 0:
                cursos_deia = df[df["tem_deia"] == "Sim"]
                logger.info("Exemplos de cursos com DEIA:")
                for _, curso in cursos_deia.head(5).iterrows():
                    logger.info(
                        f"  - {curso.get('no_curso', 'N/A')}: {curso.get('deia_encontrado', 'N/A')}"
                    )

        logger.info("=== SCRAPER FINALIZADO ===")

    except Exception as e:
        logger.error(f"Erro ao gerar relatório final: {e}")


if __name__ == "__main__":
    main()
