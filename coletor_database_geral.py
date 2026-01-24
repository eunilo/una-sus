#!/usr/bin/env python3
"""
📊 Coletor Database Geral UNA-SUS
=================================

Este script implementa coleta COMPLETA e FIEL de dados da UNA-SUS
no diretório raiz, criando um database geral sem análises.

🎯 PRINCÍPIOS:
- Coleta TODOS os dados disponíveis
- NÃO aplica filtros durante a coleta
- Preserva integridade dos dados originais
- Database fiel e atualizado
- Separação clara entre coleta e análise

🔬 METODOLOGIA:
- Coleta bruta de dados
- Preservação de todos os campos
- Logs detalhados de coleta
- Checkpointing robusto
- Validação de integridade

📁 LOCALIZAÇÃO: Diretório raiz (junto com scraper_unasus.py)
"""

import json
import logging
import os
import re
import subprocess
import sys
import time
from datetime import datetime
from typing import Dict, List

from bs4 import BeautifulSoup

# Garantir execução a partir da raiz do projeto e usar venv, se existir
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
os.chdir(BASE_DIR)
if sys.prefix == getattr(sys, "base_prefix", sys.prefix):
    venv_python = os.path.join(BASE_DIR, ".venv", "Scripts", "python.exe")
    if os.path.exists(venv_python):
        os.execv(venv_python, [venv_python, *sys.argv])


# Tentar importar dependências e instalar se necessário
def instalar_dependencias():
    """Instala automaticamente as dependências necessárias."""
    print("🔧 Verificando e instalando dependências...")

    # Lista de dependências essenciais
    dependencias = ["pandas", "requests", "beautifulsoup4", "openpyxl"]

    dependencias_faltando = []

    for dep in dependencias:
        try:
            __import__(dep)
            print(f"  ✅ {dep} já está instalado")
        except ImportError:
            dependencias_faltando.append(dep)
            print(f"  ❌ {dep} não encontrado")

    if dependencias_faltando:
        print(
            f"\n📦 Instalando dependências faltantes: "
            f"{', '.join(dependencias_faltando)}"
        )
        try:
            # Instalar individualmente (sem --user quando estiver em venv)
            usando_venv = sys.prefix != getattr(sys, "base_prefix", sys.prefix)
            for dep in dependencias_faltando:
                comando = [sys.executable, "-m", "pip", "install"]
                if not usando_venv:
                    comando.append("--user")
                comando.append(dep)
                subprocess.check_call(comando)
                print(f"  ✅ {dep} instalado")
        except subprocess.CalledProcessError as e:
            print(f"❌ Erro ao instalar dependências: {e}")
            print(
                "💡 Tente executar manualmente: "
                "pip install pandas requests beautifulsoup4"
            )
            return False

    return True


# Instalar dependências antes de importar
if not instalar_dependencias():
    print("❌ Falha na instalação de dependências. Encerrando...")
    sys.exit(1)

import pandas as pd
import requests


class ColetorDatabaseGeral:
    """
    📊 Coletor de Database Geral UNA-SUS

    Coleta TODOS os dados disponíveis sem filtros ou processamentos.
    """

    def __init__(self, logger: logging.Logger = None):
        """
        Inicializa o coletor de database geral.

        Args:
            logger: Logger para acompanhamento
        """
        # Criar diretórios necessários ANTES de configurar o logger
        self._criar_diretorios()

        self.logger = logger or self._configurar_logger()
        self.dados_coletados = []
        self.pagina_atual = 1
        self.total_paginas = 0
        self.cursos_encontrados = 0

        # Configurações da UNA-SUS (baseadas no scraper original que funciona)
        self.url_base = "https://www.unasus.gov.br/cursos/rest/busca"
        self.headers = {
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
                "https://www.unasus.gov.br/cursos/busca?"
                "status=todos&busca=&ordenacao=Relev%C3%A2ncia%20na%20busca"
            ),
        }

        # Cookies necessários (baseados no scraper original)
        shibsession_key = (
            "_shibsession_64656661756c7468747470733a2f2f7777772e756e617375732e676f762e6272"
        )
        self.cookies = {
            "PORTAL_UNASUS": "4ru34cs848mfbopb6vseqluni4",
            "UNASUSAnonID": "ID1ef7d6246158f7cf31c06b928bc56f8e",
            shibsession_key: "_329a72cffc11d2904ae393c82d0cfb72",
        }

        # Payload para requisições (baseado no scraper original)
        self.payload = {
            "busca": "",
            "ordenacao": "Por nome",
            "status": "Todos",
            "proximo": 0,
        }

    def _criar_diretorios(self):
        """Cria diretórios necessários para o funcionamento."""
        diretorios = ["data", "logs", "checkpoints"]
        for diretorio in diretorios:
            os.makedirs(diretorio, exist_ok=True)

    def _configurar_logger(self) -> logging.Logger:
        """
        📝 Configura o logger para o coletor.

        Returns:
            Logger configurado
        """
        # Configurar logger
        logger = logging.getLogger("ColetorDatabaseGeral")
        logger.setLevel(logging.INFO)

        # Limpar handlers existentes
        for handler in logger.handlers[:]:
            logger.removeHandler(handler)

        # Handler para arquivo
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        fh = logging.FileHandler(
            f"logs/coletor_database_geral_{timestamp}.log", encoding="utf-8"
        )
        fh.setLevel(logging.INFO)

        # Handler para console
        ch = logging.StreamHandler()
        ch.setLevel(logging.INFO)

        # Formato
        formatter = logging.Formatter(
            "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        )
        fh.setFormatter(formatter)
        ch.setFormatter(formatter)

        logger.addHandler(fh)
        logger.addHandler(ch)

        return logger

    def _request_with_retry(
        self,
        method,
        url: str,
        *,
        max_tentativas: int = 5,
        delay_base: int = 5,
        fail_on_status: bool = True,
        ok_statuses: tuple = (200,),
        **kwargs,
    ):
        """
        🔁 Executa requisições com retry e backoff simples.
        """
        last_response = None

        for tentativa in range(1, max_tentativas + 1):
            try:
                response = method(url, **kwargs)
                last_response = response

                if not fail_on_status or response.status_code in ok_statuses:
                    return response

                self.logger.warning(
                    f"⚠️ Status {response.status_code} em {url}. "
                    f"Tentativa {tentativa}/{max_tentativas}."
                )
            except requests.exceptions.RequestException as e:
                self.logger.warning(
                    f"⚠️ Erro de rede em {url} (tentativa {tentativa}/{max_tentativas}): {e}"
                )

            if tentativa < max_tentativas:
                time.sleep(delay_base * tentativa)

        # Retornar última resposta se existir, senão lançar erro
        if last_response is not None:
            return last_response

        raise RuntimeError(f"Falha ao conectar em {url} após {max_tentativas} tentativas")

    def _post_com_retry(self, url: str, **kwargs):
        """POST com retry para uso interno."""
        return self._request_with_retry(
            requests.post,
            url,
            fail_on_status=True,
            ok_statuses=(200,),
            **kwargs,
        )

    def _get_com_retry(
        self, url: str, *, fail_on_status: bool = True, ok_statuses: tuple = (200,), **kwargs
    ):
        """GET com retry para uso interno."""
        return self._request_with_retry(
            requests.get,
            url,
            fail_on_status=fail_on_status,
            ok_statuses=ok_statuses,
            **kwargs,
        )

    def coletar_dados_completos(self) -> List[Dict]:
        """
        📊 Coleta TODOS os dados disponíveis da UNA-SUS.

        Returns:
            Lista completa de dados coletados
        """
        self.logger.info("🚀 INICIANDO COLETA COMPLETA DE DADOS UNA-SUS")
        self.logger.info("📋 PRINCÍPIO: Coletar TODOS os dados sem filtros")
        self.logger.info("📁 LOCALIZAÇÃO: Diretório raiz")

        try:
            # Inicializar coleta
            self.logger.info("🔍 Iniciando coleta de dados...")

            # Coletar dados página por página (baseado no scraper original)
            pagina = 0
            payload = self.payload.copy()

            while True:
                self.logger.info(f"📄 Processando página {pagina + 1}")

                # Fazer requisição
                response = self._post_com_retry(
                    self.url_base,
                    data=payload,
                    headers=self.headers,
                    cookies=self.cookies,
                    timeout=30,
                )

                data = response.json()
                results = data.get("results", {})
                itens = results.get("itens", [])

                if not itens:
                    self.logger.info("📄 Nenhum item encontrado. Finalizando.")
                    break

                # Processar cada curso da página
                for curso in itens:
                    # Processar curso e suas ofertas
                    registros_curso = self._processar_curso_completo(curso)
                    self.dados_coletados.extend(registros_curso)

                self.logger.info(
                    f"✅ Página {pagina + 1}: {len(itens)} cursos coletados"
                )

                # Checkpoint a cada 10 páginas
                if (pagina + 1) % 10 == 0:
                    self._salvar_checkpoint(pagina + 1)

                # Verificar se há próxima página
                proximo = results.get("proximo")
                if not proximo:
                    self.logger.info("📄 Última página alcançada. Finalizando.")
                    break

                # Atualizar payload para próxima página
                payload["proximo"] = proximo
                pagina += 1

                # Pausa para não sobrecarregar o servidor
                time.sleep(1)

            self.logger.info(
                f"✅ COLETA COMPLETA FINALIZADA: {len(self.dados_coletados)} cursos"
            )

            # Salvar dados completos
            self._salvar_dados_completos()

            return self.dados_coletados

        except Exception as e:
            self.logger.error(f"❌ ERRO NA COLETA: {str(e)}")
            # Salvar dados coletados até o momento
            self._salvar_dados_completos()
            raise

    def _processar_curso_completo(self, curso: Dict) -> List[Dict]:
        """
        🔧 Processa um curso e suas ofertas, criando registros separados.

        Args:
            curso: Dados brutos do curso

        Returns:
            Lista de registros (um para cada oferta + um para o curso base)
        """
        # Criar cópia completa dos dados originais
        curso_processado = curso.copy()

        # Adicionar metadados de coleta
        curso_processado["metadata_coleta"] = {
            "timestamp_coleta": datetime.now().isoformat(),
            "pagina_coleta": self.pagina_atual,
            "versao_coletor": "1.0.0",
            "tipo_coleta": "database_geral_sem_filtros",
            "localizacao": "diretorio_raiz",
        }

        # Garantir que todos os campos estejam presentes
        campos_obrigatorios = [
            "id",
            "titulo",
            "descricao",
            "carga_horaria",
            "status",
            "categoria",
            "publico_alvo",
            "palavras_chave",
            "link",
            "vagas",
            "numero_vagas",
            "qt_vagas",
            "vagas_disponiveis",
            "inicio_inscricao",
            "fim_inscricao",
            "data_inicio",
            "data_fim",
            "modalidade",
            "tipo_curso",
            "nivel",
            "area_tematica",
            "instituicao",
            "coordenador",
            "tutores",
            "certificacao",
            "pre_requisitos",
            "objetivos",
            "metodologia",
            "avaliacao",
            "bibliografia",
        ]

        # Normalizar campos numéricos
        campos_numericos = ["vagas", "numero_vagas", "qt_vagas", "vagas_disponiveis"]
        for campo in campos_numericos:
            if campo in curso_processado:
                try:
                    valor = curso_processado[campo]
                    if isinstance(valor, str) and valor.strip():
                        curso_processado[campo] = int(valor)
                    elif valor is None or valor == "":
                        curso_processado[campo] = 0
                except (ValueError, TypeError):
                    curso_processado[campo] = 0

        # Normalizar campos de data
        campos_data = ["inicio_inscricao", "fim_inscricao", "data_inicio", "data_fim"]
        for campo in campos_data:
            if campo in curso_processado:
                valor = curso_processado[campo]
                if not valor or valor == "":
                    curso_processado[campo] = None

                # Extrair ofertas do curso
        id_curso = curso_processado.get("co_seq_curso", "")
        registros = []

        if id_curso:
            ofertas = self._extrair_ofertas_do_curso(id_curso)
            self.logger.info(f"📊 Curso {id_curso}: {len(ofertas)} ofertas encontradas")

            # Criar um registro para cada oferta
            for oferta in ofertas:
                registro_oferta = curso_processado.copy()
                registro_oferta.update(oferta)
                registros.append(registro_oferta)

            # Se não há ofertas, criar pelo menos um registro do curso
            if not ofertas:
                registro_curso = curso_processado.copy()
                registro_curso.update(
                    {"id_oferta": "", "erro": "Sem ofertas encontradas"}
                )
                registros.append(registro_curso)

            # Pausa para não sobrecarregar o servidor
            time.sleep(2)
        else:
            # Se não há ID do curso, criar um registro básico
            registro_curso = curso_processado.copy()
            registro_curso.update(
                {"id_oferta": "", "erro": "ID do curso não encontrado"}
            )
            registros.append(registro_curso)
            self.logger.warning(
                "⚠️ ID do curso não encontrado para extração de ofertas"
            )

        # Adicionar campos processados se não existirem
        for registro in registros:
            if "campos_processados" not in registro:
                registro["campos_processados"] = {
                    "id": registro.get("co_seq_curso", ""),
                    "titulo": registro.get("no_curso", ""),
                    "descricao": registro.get("ds_curso", ""),
                    "carga_horaria": registro.get("qt_carga_horaria_total", 0),
                    "categoria": registro.get("no_formato", ""),
                    "publico_alvo": registro.get("publico_alvo", ""),
                    "palavras_chave": registro.get("palavras_chave", ""),
                    "link": (
                        f"https://www.unasus.gov.br/cursos/curso/"
                        f"{registro.get('co_seq_curso', '')}"
                    ),
                    "vagas": registro.get("vagas", 0),
                    "numero_vagas": registro.get("numero_vagas", 0),
                    "qt_vagas": registro.get("qt_vagas", 0),
                    "nivel": registro.get("no_nivel", ""),
                    "area_tematica": registro.get("area_tematica", ""),
                    "instituicao": registro.get("no_orgao", ""),
                    "coordenador": registro.get("coordenador", ""),
                    "tutores": registro.get("tutores", ""),
                    "certificacao": registro.get("certificacao", ""),
                    "pre_requisitos": registro.get("pre_requisitos", ""),
                    "objetivos": registro.get("objetivos", ""),
                    "metodologia": registro.get("metodologia", ""),
                    "avaliacao": registro.get("avaliacao", ""),
                    "bibliografia": registro.get("bibliografia", ""),
                }

        return registros

    def _extrair_ofertas_do_curso(self, id_curso: str) -> List[Dict]:
        """
        🔍 Extrai ofertas de um curso específico.

        Args:
            id_curso: ID do curso

        Returns:
            Lista de ofertas encontradas
        """
        url_curso = f"https://www.unasus.gov.br/cursos/curso/{id_curso}"
        ofertas = []

        try:
            self.logger.info(f"🔍 Buscando ofertas do curso {id_curso}...")
            resp = self._get_com_retry(url_curso, headers=self.headers, timeout=30)

            if resp.status_code != 200:
                self.logger.warning(
                    f"⚠️ Erro HTTP {resp.status_code} ao acessar curso {id_curso}"
                )
                return []

            soup = BeautifulSoup(resp.text, "html.parser")

            # Buscar links de ofertas
            for link in soup.find_all("a", href=True):
                href = link["href"]

                # Verifica diferentes padrões de URL de oferta
                if any(
                    pattern in href
                    for pattern in ["/cursos/oferta/", "../oferta/", "oferta/"]
                ):
                    # Extrai o ID da oferta do final da URL
                    id_oferta = href.split("/")[-1]
                    if id_oferta.isdigit():
                        oferta_data = self._extrair_dados_oferta(id_oferta)
                        if oferta_data:
                            oferta_data["id_curso"] = id_curso
                            ofertas.append(oferta_data)
                            self.logger.info(f"  ✅ Oferta encontrada: {id_oferta}")

            self.logger.info(
                f"📊 Total de ofertas encontradas para curso {id_curso}: {len(ofertas)}"
            )
            return ofertas

        except Exception as e:
            self.logger.error(f"❌ Erro ao extrair ofertas do curso {id_curso}: {e}")
            return []

    def _extrair_dados_oferta(self, id_oferta: str) -> Dict:
        """
        🔍 Extrai dados de uma oferta específica.

        Args:
            id_oferta: ID da oferta

        Returns:
            Dados da oferta
        """
        url_oferta = f"https://www.unasus.gov.br/cursos/oferta/{id_oferta}"
        url_api = f"https://www.unasus.gov.br/cursos/rest/oferta/{id_oferta}"

        try:
            self.logger.info(f"  🔍 Extraindo dados da oferta {id_oferta}...")

            dados = {
                "id_oferta": id_oferta,
                "url_oferta": url_oferta,
                "codigo_oferta": id_oferta,
            }

            # Tentar API REST primeiro
            api_headers = {
                "User-Agent": self.headers["User-Agent"],
                "Accept": "application/json, text/javascript, */*; q=0.01",
                "X-Requested-With": "XMLHttpRequest",
                "Referer": url_oferta,
            }

            try:
                resp_api = self._get_com_retry(
                    url_api, headers=api_headers, timeout=30, fail_on_status=False
                )
                if resp_api.status_code == 200:
                    response_data = resp_api.json()
                    self.logger.info("    ✅ Dados obtidos via API REST")

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
                        self.logger.info(f"    ✅ Vagas extraídas: {dados['vagas']}")
                    else:
                        self.logger.warning("    ⚠️ Vagas não encontradas na API")

                    return dados
                else:
                    self.logger.warning(
                        f"    ⚠️ API REST retornou status {resp_api.status_code}"
                    )
            except Exception as e:
                self.logger.warning(f"    ⚠️ Erro na API REST: {e}")

            # Fallback: tentar extrair da página HTML
            self.logger.info("    🔄 Tentando extração da página HTML...")
            resp = self._get_com_retry(url_oferta, headers=self.headers, timeout=30)
            soup = BeautifulSoup(resp.text, "html.parser")

            # Buscar o div principal com os dados da oferta
            oferta_quadro = soup.find("div", id="oferta_quadro")
            if oferta_quadro:
                texto_completo = oferta_quadro.get_text()

                # Extrair vagas usando regex
                vagas_match = re.search(r"Vagas:\s*(\d+)", texto_completo)
                dados["vagas"] = vagas_match.group(1) if vagas_match else ""

                # Extrair público-alvo
                publico_pattern = (
                    r"Público-alvo:\s*(.*?)(?=\n\n|\nLocal|\nFormato|\nNível|"
                    r"\nModalidade|\nProgramas|\nTemas|\nDeCs|\nDescrição|"
                    r"\nPalavras-chave|$)"
                )
                publico_match = re.search(publico_pattern, texto_completo, re.DOTALL)
                publico_alvo = publico_match.group(1).strip() if publico_match else ""
                dados["publico_alvo"] = publico_alvo

                # Extrair local da oferta
                local_match = re.search(r"Local:\s*(.*?)(?=\n|$)", texto_completo)
                local_oferta = local_match.group(1).strip() if local_match else ""
                dados["local_oferta"] = local_oferta

                # Extrair formato
                formato_match = re.search(r"Formato:\s*(.*?)(?=\n|$)", texto_completo)
                dados["formato"] = (
                    formato_match.group(1).strip() if formato_match else ""
                )

                # Extrair programas de governo
                programas_match = re.search(
                    r"Programas:\s*(.*?)(?=\n|$)", texto_completo
                )
                dados["programas_governo"] = (
                    programas_match.group(1).strip() if programas_match else ""
                )

                # Extrair temas
                temas_match = re.search(r"Temas:\s*(.*?)(?=\n|$)", texto_completo)
                dados["temas"] = temas_match.group(1).strip() if temas_match else ""

                # Extrair DeCs
                decs_match = re.search(r"DeCs:\s*(.*?)(?=\n|$)", texto_completo)
                dados["decs"] = decs_match.group(1).strip() if decs_match else ""

                # Extrair descrição da oferta
                descricao_match = re.search(
                    r"Descrição:\s*(.*?)(?=\n|$)", texto_completo, re.DOTALL
                )
                dados["descricao_oferta"] = (
                    descricao_match.group(1).strip() if descricao_match else ""
                )

                # Extrair palavras-chave
                palavras_match = re.search(
                    r"Palavras-chave:\s*(.*?)(?=\n|$)", texto_completo
                )
                dados["palavras_chave"] = (
                    palavras_match.group(1).strip() if palavras_match else ""
                )

                self.logger.info("    ✅ Dados extraídos da página HTML")
                return dados

            self.logger.warning("    ⚠️ Não foi possível extrair dados da oferta")
            return dados

        except Exception as e:
            self.logger.error(
                f"    ❌ Erro ao extrair dados da oferta {id_oferta}: {e}"
            )
            return {"id_oferta": id_oferta, "erro": str(e)}

    def _salvar_checkpoint(self, pagina_atual: int):
        """
        💾 Salva checkpoint da coleta.

        Args:
            pagina_atual: Página atual sendo processada
        """
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        checkpoint_data = {
            "timestamp": datetime.now().isoformat(),
            "pagina_atual": pagina_atual,
            "cursos_coletados": len(self.dados_coletados),
            "versao_coletor": "1.0.0",
            "tipo_coleta": "database_geral",
        }

        # Garantir diretório de checkpoints
        os.makedirs("checkpoints", exist_ok=True)

        checkpoint_path = (
            f"checkpoints/coleta_database_geral_checkpoint_{timestamp}.json"
        )
        with open(checkpoint_path, "w", encoding="utf-8") as f:
            json.dump(checkpoint_data, f, ensure_ascii=False, indent=2)

        self.logger.info(f"💾 Checkpoint salvo: {checkpoint_path}")

    def _salvar_dados_completos(self):
        """
        💾 Salva dados completos em múltiplos formatos.
        """
        if not self.dados_coletados:
            self.logger.warning("⚠️ Nenhum dado para salvar")
            return

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

        # Garantir diretório de dados
        os.makedirs("data", exist_ok=True)

        # Salvar em JSON
        json_path = f"data/unasus_database_geral_{timestamp}.json"
        with open(json_path, "w", encoding="utf-8") as f:
            json.dump(self.dados_coletados, f, ensure_ascii=False, indent=2)

        self.logger.info(f"💾 Dados salvos em JSON: {json_path}")

        # Salvar em CSV
        csv_path = f"data/unasus_database_geral_{timestamp}.csv"
        df = pd.DataFrame(self.dados_coletados)
        df.to_csv(csv_path, index=False, encoding="utf-8-sig")

        self.logger.info(f"💾 Dados salvos em CSV: {csv_path}")

        # Salvar em Excel (opcional)
        try:
            excel_path = f"data/unasus_database_geral_{timestamp}.xlsx"
            df.to_excel(excel_path, index=False)
            self.logger.info(f"💾 Dados salvos em Excel: {excel_path}")
        except ImportError:
            self.logger.info("ℹ️ openpyxl não instalado. Pulando salvamento Excel.")

        # Gerar relatório de coleta
        self._gerar_relatorio_coleta(timestamp)

    def _gerar_relatorio_coleta(self, timestamp: str):
        """
        📊 Gera relatório detalhado da coleta.

        Args:
            timestamp: Timestamp da coleta
        """
        relatorio = {
            "resumo_geral": {
                "total_cursos": len(self.dados_coletados),
                "timestamp_coleta": datetime.now().isoformat(),
                "versao_coletor": "1.0.0",
                "tipo_coleta": "database_geral_sem_filtros",
                "localizacao": "diretorio_raiz",
            },
            "estatisticas": {
                "campos_disponiveis": (
                    list(self.dados_coletados[0].keys()) if self.dados_coletados else []
                ),
                "campos_preenchidos": {},
                "percentual_preenchimento": {},
                "vagas_estatisticas": {
                    "total_vagas": 0,
                    "media_vagas": 0,
                    "min_vagas": 0,
                    "max_vagas": 0,
                    "cursos_com_vagas": 0,
                    "percentual_preenchido": 0,
                },
            },
            "arquivos_gerados": {
                "json": f"data/unasus_database_geral_{timestamp}.json",
                "csv": f"data/unasus_database_geral_{timestamp}.csv",
                "excel": f"data/unasus_database_geral_{timestamp}.xlsx",
            },
        }

        # Garantir diretório de dados para o relatório
        os.makedirs("data", exist_ok=True)

        # Calcular estatísticas de preenchimento
        if self.dados_coletados:
            for campo in self.dados_coletados[0].keys():
                preenchidos = sum(
                    1 for curso in self.dados_coletados if curso.get(campo)
                )
                relatorio["estatisticas"]["campos_preenchidos"][campo] = preenchidos
                relatorio["estatisticas"]["percentual_preenchimento"][campo] = (
                    preenchidos / len(self.dados_coletados)
                ) * 100

            # Calcular estatísticas de vagas
            vagas_campos = ["vagas", "numero_vagas", "qt_vagas", "vagas_disponiveis"]
            vagas_valores = []
            for curso in self.dados_coletados:
                for campo in vagas_campos:
                    valor = curso.get(campo, 0)
                    if isinstance(valor, (int, float)) and valor > 0:
                        vagas_valores.append(valor)

            if vagas_valores:
                relatorio["estatisticas"]["vagas_estatisticas"] = {
                    "total_vagas": sum(vagas_valores),
                    "media_vagas": sum(vagas_valores) / len(vagas_valores),
                    "min_vagas": min(vagas_valores),
                    "max_vagas": max(vagas_valores),
                    "cursos_com_vagas": len(vagas_valores),
                    "percentual_preenchido": (
                        len(vagas_valores) / len(self.dados_coletados)
                    )
                    * 100,
                }

        # Salvar relatório
        relatorio_path = f"data/relatorio_coleta_database_geral_{timestamp}.json"
        with open(relatorio_path, "w", encoding="utf-8") as f:
            json.dump(relatorio, f, ensure_ascii=False, indent=2)

        self.logger.info(f"📊 Relatório salvo: {relatorio_path}")

        # Exibir resumo no console
        print("\n" + "=" * 60)
        print("📊 RELATÓRIO DE COLETA - DATABASE GERAL")
        print("=" * 60)
        print(
            f"📈 Total de cursos coletados: {relatorio['resumo_geral']['total_cursos']}"
        )
        print(f"⏰ Timestamp: {relatorio['resumo_geral']['timestamp_coleta']}")
        print(f"📁 Localização: {relatorio['resumo_geral']['localizacao']}")
        print(f"💾 Arquivos gerados:")
        print(f"   - JSON: {relatorio['arquivos_gerados']['json']}")
        print(f"   - CSV: {relatorio['arquivos_gerados']['csv']}")
        if "excel" in relatorio["arquivos_gerados"]:
            print(f"   - Excel: {relatorio['arquivos_gerados']['excel']}")
        print("=" * 60)

    def carregar_dados_existentes(self, caminho_arquivo: str) -> List[Dict]:
        """
        📂 Carrega dados existentes de arquivo.

        Args:
            caminho_arquivo: Caminho para o arquivo de dados

        Returns:
            Lista de dados carregados
        """
        if not os.path.exists(caminho_arquivo):
            raise FileNotFoundError(f"Arquivo não encontrado: {caminho_arquivo}")

        extensao = caminho_arquivo.lower().split(".")[-1]

        if extensao == "json":
            with open(caminho_arquivo, "r", encoding="utf-8") as f:
                return json.load(f)
        elif extensao == "csv":
            df = pd.read_csv(caminho_arquivo, encoding="utf-8-sig")
            return df.to_dict("records")
        elif extensao in ["xlsx", "xls"]:
            try:
                df = pd.read_excel(caminho_arquivo)
                return df.to_dict("records")
            except ImportError:
                raise ValueError(
                    "openpyxl não instalado. Instale com: pip install openpyxl"
                )
        else:
            raise ValueError(f"Formato não suportado: {extensao}")


def main():
    """
    🚀 Função principal para execução do coletor.
    """
    print("🚀 COLETOR DATABASE GERAL UNA-SUS")
    print("=" * 50)
    print("📋 Este script coleta TODOS os dados UNA-SUS sem filtros")
    print("📁 Localização: Diretório raiz")
    print("💾 Database fiel e atualizado")
    print("=" * 50)

    try:
        # Inicializar coletor
        coletor = ColetorDatabaseGeral()

        # Executar coleta
        dados = coletor.coletar_dados_completos()

        print(f"\n✅ COLETA FINALIZADA COM SUCESSO!")
        print(f"📊 Total de cursos coletados: {len(dados)}")
        print(f"💾 Dados salvos em: data/")

    except Exception as e:
        print(f"\n❌ ERRO NA COLETA: {str(e)}")
        print("🔧 Verifique os logs para mais detalhes.")


if __name__ == "__main__":
    main()
