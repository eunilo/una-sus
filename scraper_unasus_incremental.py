import json
import logging
import os
import time
from datetime import datetime
from typing import Dict, List, Set

import pandas as pd
import requests
from bs4 import BeautifulSoup

# Configuração de logging


def setup_logging():
    """Configura o sistema de logging."""
    log_dir = "logs"
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    log_file = f"{log_dir}/scraper_{timestamp}.log"
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s",
        handlers=[
            logging.FileHandler(log_file, encoding="utf-8"),
            logging.StreamHandler(),
        ],
    )
    return logging.getLogger(__name__)


# Configurações da API
URL = "https://www.unasus.gov.br/cursos/rest/busca"
HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/138.0.0.0 Safari/537.36"
    ),
    "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
    "Accept": "application/json, text/javascript, */*; q=0.01",
    "X-Requested-With": "XMLHttpRequest",
    "Origin": "https://www.unasus.gov.br",
    "Referer": (
        "https://www.unasus.gov.br/cursos/busca?status=todos&busca="
        "&ordenacao=Relev%C3%A2ncia%20na%20busca"
    ),
}

COOKIES = {
    "PORTAL_UNASUS": "4ru34cs848mfbopb6vseqluni4",
    "UNASUSAnonID": "ID1ef7d6246158f7cf31c06b928bc56f8e",
    "_shibsession_64656661756c7468747470733a2f2f7777772e756e617375732e676f762e6272": (
        "_329a72cffc11d2904ae393c82d0cfb72"
    ),
}

PAYLOAD_INICIAL = {
    "busca": "",
    "ordenacao": "Por nome",
    "status": "Todos",
    "proximo": 0,
}

DESCRITORES_DEIA = [
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


class ScraperProgress:
    """Gerencia o progresso do scraper."""

    def __init__(self, checkpoint_file: str = "checkpoint.json"):
        self.checkpoint_file = checkpoint_file
        self.data = self._load_checkpoint()

    def _load_checkpoint(self) -> Dict:
        """Carrega o checkpoint salvo."""
        if os.path.exists(self.checkpoint_file):
            try:
                with open(self.checkpoint_file, "r", encoding="utf-8") as f:
                    return json.load(f)
            except Exception as e:
                logging.error(f"Erro ao carregar checkpoint: {e}")
        return self._get_default_checkpoint()

    def _get_default_checkpoint(self) -> Dict:
        """Retorna o checkpoint padrão."""
        return {
            "pagina_atual": 0,
            "cursos_processados": 0,
            "ofertas_processadas": 0,
            "ultima_atualizacao": "",
            "proximo_token": 0,
        }

    def save_checkpoint(self, pagina: int, cursos: int, ofertas: int, proximo: int):
        """Salva o checkpoint atual."""
        self.data.update(
            {
                "pagina_atual": pagina,
                "cursos_processados": cursos,
                "ofertas_processadas": ofertas,
                "ultima_atualizacao": datetime.now().isoformat(),
                "proximo_token": proximo,
            }
        )
        self._write_checkpoint()

    def _write_checkpoint(self):
        """Escreve o checkpoint no arquivo."""
        try:
            with open(self.checkpoint_file, "w", encoding="utf-8") as f:
                json.dump(self.data, f, indent=2, ensure_ascii=False)
        except Exception as e:
            logging.error(f"Erro ao salvar checkpoint: {e}")


def encontrar_descritor_deia(
    titulo: str, descricao: str, descritores: List[str]
) -> str:
    """Verifica se algum descritor DEIA está presente no texto."""
    texto_completo = (titulo or "") + " " + (descricao or "")
    texto_lower = texto_completo.lower()

    for descritor in descritores:
        if descritor.lower() in texto_lower:
            return descritor
    return ""


def extrair_ofertas_do_curso(id_curso: str, logger: logging.Logger) -> List[str]:
    """Extrai IDs das ofertas de um curso, incluindo encerradas."""
    url_curso = f"https://www.unasus.gov.br/cursos/curso/{id_curso}"

    try:
        response = requests.get(url_curso, headers=HEADERS, timeout=30)
        soup = BeautifulSoup(response.text, "html.parser")

        ofertas = _encontrar_links_ofertas(soup)

        if not ofertas:
            _tentar_buscar_ofertas_encerradas(soup, id_curso, logger)

        ofertas_unicas = list(set(ofertas))
        logger.info(f"Curso {id_curso}: {len(ofertas_unicas)} ofertas encontradas")
        return ofertas_unicas

    except Exception as e:
        logger.error(f"Erro ao buscar ofertas do curso {id_curso}: {e}")
        return []


def _encontrar_links_ofertas(soup: BeautifulSoup) -> List[str]:
    """Encontra links de ofertas no HTML."""
    ofertas = []
    for link in soup.find_all("a", href=True):
        href = link["href"]
        if "/cursos/oferta/" in href:
            id_oferta = href.split("/")[-1]
            if id_oferta.isdigit():
                ofertas.append(id_oferta)
    return ofertas


def _tentar_buscar_ofertas_encerradas(
    soup: BeautifulSoup, id_curso: str, logger: logging.Logger
):
    """Tenta encontrar links para ofertas encerradas."""
    logger.info(f"Curso {id_curso}: tentando buscar ofertas encerradas...")

    encerradas_links = soup.find_all(
        "a", string=lambda t: t and "encerrada" in t.lower()
    )

    if encerradas_links:
        logger.info(f"Curso {id_curso}: encontrou link de ofertas encerradas")


def extrair_descricao_curso(id_curso: str, logger: logging.Logger) -> str:
    """Extrai a descrição do curso da página geral do curso."""
    url_curso = f"https://www.unasus.gov.br/cursos/curso/{id_curso}"

    try:
        response = requests.get(url_curso, headers=HEADERS, timeout=30)
        soup = BeautifulSoup(response.text, "html.parser")

        descricao = _buscar_descricao_por_seletores(soup, id_curso, logger)

        if not descricao:
            descricao = _buscar_descricao_por_texto(soup, id_curso, logger)

        _log_resultado_descricao(descricao, id_curso, logger)
        return descricao

    except Exception as e:
        logger.error(f"Erro ao extrair descrição do curso {id_curso}: {e}")
        return ""


def _buscar_descricao_por_seletores(
    soup: BeautifulSoup, id_curso: str, logger: logging.Logger
) -> str:
    """Busca descrição usando seletores CSS específicos."""
    selectores = [
        "div.descricao",
        "div.curso-descricao",
        "p.descricao",
        "div.conteudo",
        "div.curso-info",
        "section.descricao",
        ".descricao-curso",
    ]

    for seletor in selectores:
        elemento = soup.select_one(seletor)
        if elemento:
            descricao = elemento.get_text(strip=True)
            if descricao:
                logger.debug(f"Descrição encontrada com seletor: {seletor}")
                return descricao
    return ""


def _buscar_descricao_por_texto(
    soup: BeautifulSoup, id_curso: str, logger: logging.Logger
) -> str:
    """Busca descrição procurando por texto específico."""
    elementos = soup.find_all(
        string=lambda t: t
        and ("descrição" in t.lower() or "sobre o curso" in t.lower())
    )

    for elemento in elementos:
        parent = elemento.parent
        if parent:
            descricao = parent.get_text(strip=True)
            if len(descricao) > 50:  # Tamanho mínimo para descrição
                return descricao
    return ""


def _log_resultado_descricao(descricao: str, id_curso: str, logger: logging.Logger):
    """Registra o resultado da extração de descrição."""
    if descricao:
        logger.debug(
            f"Descrição extraída para curso {id_curso}: " f"{descricao[:100]}..."
        )
    else:
        logger.warning(f"Nenhuma descrição encontrada para curso {id_curso}")


def extrair_dados_oferta(id_oferta: str, logger: logging.Logger) -> Dict:
    """Extrai dados detalhados de uma oferta."""
    url_oferta = f"https://www.unasus.gov.br/cursos/oferta/{id_oferta}"

    try:
        response = requests.get(url_oferta, headers=HEADERS, timeout=30)
        soup = BeautifulSoup(response.text, "html.parser")

        dados = {"id_oferta": id_oferta, "url_oferta": url_oferta}
        campos = _get_campos_oferta(id_oferta)

        for campo, chave in campos:
            dados[campo] = _extrair_campo_oferta(soup, campo, chave)

        logger.debug(f"Oferta {id_oferta}: dados extraídos com sucesso")
        return dados

    except Exception as e:
        logger.error(f"Erro ao buscar dados da oferta {id_oferta}: {e}")
        return {"id_oferta": id_oferta, "erro": str(e)}


def _get_campos_oferta(id_oferta: str) -> List[tuple]:
    """Define os campos a serem extraídos da oferta."""
    return [
        ("codigo_oferta", id_oferta),
        ("vagas", "Vagas"),
        ("publico_alvo", "Público-alvo"),
        ("local_oferta", "Local"),
        ("formato", "Formato"),
        ("programas_governo", "Programas de governo"),
        ("temas", "Temas"),
        ("decs", "DeCs"),
        ("descricao_oferta", "Descrição da oferta"),
        ("palavras_chave", "Palavras-chave"),
    ]


def _extrair_campo_oferta(soup: BeautifulSoup, campo: str, chave: str) -> str:
    """Extrai um campo específico da oferta."""
    if campo == "codigo_oferta":
        return chave

    elemento = soup.find(string=lambda t: t and chave in t)
    if elemento:
        try:
            return elemento.parent.find_next("td").text.strip()
        except Exception:
            return ""
    return ""


def carregar_ids_processados(csv_path: str, logger: logging.Logger) -> Set[str]:
    """Carrega IDs de cursos já processados."""
    if not os.path.exists(csv_path):
        logger.info("Arquivo CSV não encontrado. Iniciando do zero.")
        return set()

    try:
        df_existente = pd.read_csv(csv_path, encoding="utf-8-sig")
        ids = _extrair_ids_do_dataframe(df_existente, logger)
        logger.info(f"Carregados {len(ids)} cursos já processados")
        return ids

    except Exception as e:
        logger.error(f"Erro ao carregar CSV existente: {e}")
        return set()


def _extrair_ids_do_dataframe(df: pd.DataFrame, logger: logging.Logger) -> Set[str]:
    """Extrai IDs de cursos do DataFrame."""
    colunas_id = ["co_seq_curso", "id_curso", "co_curso"]

    for col in colunas_id:
        if col in df.columns:
            ids = set(df[col].astype(str).unique())
            return ids

    logger.warning("Nenhuma coluna de ID encontrada no CSV")
    return set()


def salvar_dados(csv_path: str, dados: List[Dict], logger: logging.Logger) -> bool:
    """Salva os dados coletados no arquivo CSV."""
    if not dados:
        logger.info("Nenhum dado para salvar.")
        return False

    try:
        df_final = _preparar_dataframe_final(csv_path, dados)
        df_final.to_csv(csv_path, index=False, encoding="utf-8-sig")
        logger.info(f"Dados salvos: {len(df_final)} registros totais")
        return True

    except Exception as e:
        logger.error(f"Erro ao salvar dados: {e}")
        return False


def _preparar_dataframe_final(csv_path: str, dados: List[Dict]) -> pd.DataFrame:
    """Prepara o DataFrame final para salvar."""
    if os.path.exists(csv_path):
        df_existente = pd.read_csv(csv_path, encoding="utf-8-sig")
        df_novo = pd.DataFrame(dados)
        return pd.concat([df_existente, df_novo], ignore_index=True)
    else:
        return pd.DataFrame(dados)


def validar_curso(curso: Dict, logger: logging.Logger) -> bool:
    """Valida se um curso tem os dados mínimos necessários."""
    if not _validar_campos_obrigatorios(curso, logger):
        return False

    _marcar_curso_incompleto(curso, logger)
    return True


def _validar_campos_obrigatorios(curso: Dict, logger: logging.Logger) -> bool:
    """Valida campos obrigatórios do curso."""
    campos_obrigatorios = ["no_curso"]

    for campo in campos_obrigatorios:
        if not curso.get(campo):
            logger.warning(f"Curso sem {campo}: {curso.get('id_curso', 'N/A')}")
            return False
    return True


def _marcar_curso_incompleto(curso: Dict, logger: logging.Logger):
    """Marca se o curso está incompleto (sem descrição)."""
    if not curso.get("ds_curso"):
        logger.warning(
            f"Curso sem descrição: {curso.get('no_curso', 'N/A')} "
            f"(ID: {curso.get('id_curso', 'N/A')})"
        )
        curso["curso_incompleto"] = "Sim"
    else:
        curso["curso_incompleto"] = "Não"


def processar_curso(curso: Dict, id_curso: str, logger: logging.Logger) -> List[Dict]:
    """Processa um curso individual e retorna seus dados."""
    titulo = curso.get("no_curso", "")
    descricao = curso.get("ds_curso", "")

    if not descricao:
        logger.info(f"Extraindo descrição da página do curso {id_curso}")
        descricao = extrair_descricao_curso(id_curso, logger)
        curso["ds_curso"] = descricao

    if not descricao:
        logger.info(f"Analisando DEIA apenas no título: {titulo[:50]}...")

    _aplicar_analise_deia(curso, titulo, descricao, logger)

    ofertas = extrair_ofertas_do_curso(id_curso, logger)
    return _processar_ofertas_curso(curso, ofertas, id_curso, logger)


def _aplicar_analise_deia(
    curso: Dict, titulo: str, descricao: str, logger: logging.Logger
):
    """Aplica análise DEIA no curso."""
    found_descritor = encontrar_descritor_deia(titulo, descricao, DESCRITORES_DEIA)
    curso["tem_deia"] = "Sim" if found_descritor else "Não"
    curso["deia_encontrado"] = found_descritor

    if found_descritor:
        logger.info(f"DEIA encontrado: {found_descritor}")


def _processar_ofertas_curso(
    curso: Dict, ofertas: List[str], id_curso: str, logger: logging.Logger
) -> List[Dict]:
    """Processa as ofertas de um curso."""
    if not ofertas:
        logger.warning(f"Curso {id_curso} sem ofertas")
        return [{**curso, "id_oferta": "", "erro": "Sem ofertas encontradas"}]

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


def gerar_relatorio_final(csv_path: str, logger: logging.Logger):
    """Gera relatório final com estatísticas."""
    logger.info("=== RELATÓRIO FINAL ===")

    try:
        df = pd.read_csv(csv_path, encoding="utf-8-sig")
        logger.info(f"Arquivo final: {csv_path}")
        logger.info(f"Total de registros: {len(df)}")
        logger.info(f"Colunas: {list(df.columns)}")

        _gerar_estatisticas_deia(df, logger)
        logger.info("=== SCRAPER FINALIZADO ===")

    except Exception as e:
        logger.error(f"Erro ao gerar relatório final: {e}")


def _gerar_estatisticas_deia(df: pd.DataFrame, logger: logging.Logger):
    """Gera estatísticas sobre cursos DEIA."""
    if "tem_deia" in df.columns:
        deia_stats = df["tem_deia"].value_counts()
        logger.info(f"Cursos com DEIA: {deia_stats.get('Sim', 0)}")
        logger.info(f"Cursos sem DEIA: {deia_stats.get('Não', 0)}")


def main():
    """Função principal do scraper com logging detalhado."""
    logger = setup_logging()
    logger.info("=== INICIANDO SCRAPER UNA-SUS ===")

    # Configurações
    csv_path = "unasus_ofertas_detalhadas.csv"
    lote = 10
    todos_detalhes = []
    pagina = 0
    cursos_novos_processados = 0
    ofertas_processadas = 0

    # Inicialização
    progress = ScraperProgress()
    cursos_processados = carregar_ids_processados(csv_path, logger)
    payload = PAYLOAD_INICIAL.copy()

    logger.info(f"Cursos já processados: {len(cursos_processados)}")
    logger.info(f"Arquivo de saída: {csv_path}")
    logger.info(f"Checkpoint: página {progress.data['pagina_atual']}")

    # Restaurar estado se necessário
    if progress.data["proximo_token"] > 0:
        payload["proximo"] = progress.data["proximo_token"]
        pagina = progress.data["pagina_atual"]
        logger.info(f"Retomando da página {pagina}")

    # Loop principal
    while True:
        try:
            logger.info(f"=== PROCESSANDO PÁGINA {pagina + 1} ===")
            logger.info(f"Payload enviado: {payload}")

            response = requests.post(
                URL,
                data=payload,
                headers=HEADERS,
                cookies=COOKIES,
                timeout=30,
            )

            logger.info(f"Status da resposta: {response.status_code}")
            logger.info(
                "Total de resultados: %s",
                response.json().get("results", {}).get("total", "N/A"),
            )

            itens = response.json().get("results", {}).get("itens", [])

            if not itens:
                logger.info("Nenhum item encontrado. Finalizando...")
                break

            logger.info(f"Página {pagina + 1}: {len(itens)} cursos encontrados")

            # Processar cursos da página
            for i, curso in enumerate(itens, 1):
                if not validar_curso(curso, logger):
                    continue

                id_curso = _extrair_id_curso(curso)
                if not id_curso:
                    logger.warning(f"Curso sem ID: {curso.get('no_curso', 'N/A')}")
                    continue

                id_curso_str = str(id_curso)
                if id_curso_str in cursos_processados:
                    logger.debug(f"Curso {id_curso} já processado, pulando...")
                    continue

                logger.info(
                    f"Processando curso {i}/{len(itens)}: " f"{curso.get('no_curso')}"
                )

                # Processar curso
                dados_curso = processar_curso(curso, id_curso, logger)
                todos_detalhes.extend(dados_curso)

                # Atualizar contadores
                cursos_processados.add(id_curso_str)
                cursos_novos_processados += 1
                ofertas_processadas += len(dados_curso)

                # Salvamento incremental
                if len(todos_detalhes) >= lote:
                    if salvar_dados(csv_path, todos_detalhes, logger):
                        logger.info(
                            f"Checkpoint salvo: {cursos_novos_processados} "
                            f"cursos, {ofertas_processadas} ofertas"
                        )
                        todos_detalhes = []

            # Preparar próxima página
            proximo = response.json().get("results", {}).get("proximo")
            logger.info(f"Token atual: {payload.get('proximo', 0)}")
            logger.info(f"Token próximo: {proximo}")

            if not proximo:
                logger.info("Não há mais páginas. Finalizando...")
                break

            payload["proximo"] = proximo
            pagina += 1
            progress.save_checkpoint(
                pagina, cursos_novos_processados, ofertas_processadas, proximo
            )
            logger.info(f"Próxima página: {pagina} (token: {proximo})")
            time.sleep(1)

        except Exception as e:
            logger.error(f"Erro de conexão: {e}. Tentando novamente em 30s...")
            time.sleep(30)
            continue

    # Finalização
    logger.info("=== FINALIZANDO PROCESSAMENTO ===")

    if todos_detalhes:
        if salvar_dados(csv_path, todos_detalhes, logger):
            logger.info(
                f"Finalizado! {cursos_novos_processados} cursos, "
                f"{ofertas_processadas} ofertas processadas"
            )
        else:
            logger.error("Erro ao salvar dados finais!")
    else:
        logger.info("Nenhum dado novo para salvar.")

    gerar_relatorio_final(csv_path, logger)


def _extrair_id_curso(curso: Dict) -> str:
    """Extrai o ID do curso de diferentes campos possíveis."""
    return (
        curso.get("co_seq_curso")
        or curso.get("id_curso")
        or curso.get("co_curso")
        or curso.get("id")
    )


if __name__ == "__main__":
    main()
