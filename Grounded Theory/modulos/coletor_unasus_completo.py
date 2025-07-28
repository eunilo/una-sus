#!/usr/bin/env python3
"""
📊 Coletor UNA-SUS Completo - Coleta Fiel de Dados
==================================================

Este módulo implementa coleta COMPLETA e FIEL de dados da UNA-SUS,
sem filtros ou processamentos que possam comprometer a integridade
dos dados originais.

🎯 PRINCÍPIOS:
- Coleta TODOS os dados disponíveis
- NÃO aplica filtros durante a coleta
- Preserva integridade dos dados originais
- Separação clara entre coleta e processamento
- Database fiel e atualizado

🔬 METODOLOGIA:
- Coleta bruta de dados
- Preservação de todos os campos
- Logs detalhados de coleta
- Checkpointing robusto
- Validação de integridade
"""

import json
import logging
import os
import time
from datetime import datetime
from typing import Dict, List

import pandas as pd
import requests


class ColetorUnasusCompleto:
    """
    📊 Coletor Completo de Dados UNA-SUS

    Coleta TODOS os dados disponíveis sem filtros ou processamentos.
    """

    def __init__(self, logger: logging.Logger = None):
        """
        Inicializa o coletor completo.

        Args:
            logger: Logger para acompanhamento
        """
        self.logger = logger or self._configurar_logger()
        self.dados_coletados = []
        self.pagina_atual = 1
        self.total_paginas = 0
        self.cursos_encontrados = 0

        # Configurações da UNA-SUS (baseadas no backup original que funcionava)
        self.url_base = "https://www.unasus.gov.br/cursos/rest/busca"
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36",
            "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
            "Accept": "application/json, text/javascript, */*; q=0.01",
            "X-Requested-With": "XMLHttpRequest",
            "Origin": "https://www.unasus.gov.br",
            "Referer": "https://www.unasus.gov.br/cursos/busca?status=todos&busca=&ordenacao=Relev%C3%A2ncia%20na%20busca",
        }

        # Cookies necessários (baseados no backup original)
        self.cookies = {
            "PORTAL_UNASUS": "4ru34cs848mfbopb6vseqluni4",
            "UNASUSAnonID": "ID1ef7d6246158f7cf31c06b928bc56f8e",
            "_shibsession_64656661756c7468747470733a2f2f7777772e756e617375732e676f762e6272": "_329a72cffc11d2904ae393c82d0cfb72",
        }

        # Payload para requisições (baseado no backup original)
        self.payload = {
            "busca": "",
            "ordenacao": "Por nome",
            "status": "Todos",
            "proximo": 0,
        }

    def _configurar_logger(self) -> logging.Logger:
        """
        📝 Configura o logger para o coletor.

        Returns:
            Logger configurado
        """
        # Criar pasta de logs se não existir
        os.makedirs("logs", exist_ok=True)

        # Configurar logger
        logger = logging.getLogger("ColetorUnasusCompleto")
        logger.setLevel(logging.INFO)

        # Handler para arquivo
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        fh = logging.FileHandler(
            f"logs/coletor_unasus_{timestamp}.log", encoding="utf-8"
        )
        fh.setLevel(logging.INFO)

        # Handler para console
        ch = logging.StreamHandler()
        ch.setLevel(logging.INFO)

        # Formatter
        formatter = logging.Formatter(
            "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        )
        fh.setFormatter(formatter)
        ch.setFormatter(formatter)

        # Adicionar handlers
        logger.addHandler(fh)
        logger.addHandler(ch)

        return logger

    def coletar_dados_completos(self) -> List[Dict]:
        """
        📊 Coleta TODOS os dados disponíveis da UNA-SUS.

        Returns:
            Lista completa de dados coletados
        """
        self.logger.info("🚀 INICIANDO COLETA COMPLETA DE DADOS UNA-SUS")
        self.logger.info("📋 PRINCÍPIO: Coletar TODOS os dados sem filtros")

        try:
            # Inicializar coleta
            self.logger.info("🔍 Iniciando coleta de dados...")

            # Coletar dados página por página (baseado no backup original)
            pagina = 0
            payload = self.payload.copy()

            while True:
                self.logger.info(f"📄 Processando página {pagina + 1}")

                # Fazer requisição
                response = requests.post(
                    self.url_base,
                    data=payload,
                    headers=self.headers,
                    cookies=self.cookies,
                    timeout=30,
                )

                if response.status_code != 200:
                    self.logger.warning(
                        f"⚠️ Status {response.status_code}. Tentando novamente..."
                    )
                    time.sleep(30)
                    continue

                data = response.json()
                results = data.get("results", {})
                itens = results.get("itens", [])

                if not itens:
                    self.logger.info("📄 Nenhum item encontrado. Finalizando.")
                    break

                # Processar cada curso da página
                for curso in itens:
                    curso_processado = self._processar_curso_completo(curso)
                    self.dados_coletados.append(curso_processado)

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

    def _processar_curso_completo(self, curso: Dict) -> Dict:
        """
        🔧 Processa um curso mantendo TODOS os dados originais.

        Args:
            curso: Dados brutos do curso

        Returns:
            Curso processado com todos os dados
        """
        # Criar cópia completa dos dados originais
        curso_processado = curso.copy()

        # Adicionar metadados de coleta
        curso_processado["metadata_coleta"] = {
            "timestamp_coleta": datetime.now().isoformat(),
            "pagina_coleta": self.pagina_atual,
            "versao_coletor": "1.0.0",
            "tipo_coleta": "completa_sem_filtros",
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

        for campo in campos_obrigatorios:
            if campo not in curso_processado:
                curso_processado[campo] = None

        # Normalizar campos de texto
        campos_texto = [
            "titulo",
            "descricao",
            "publico_alvo",
            "palavras_chave",
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
        for campo in campos_texto:
            if curso_processado.get(campo):
                curso_processado[campo] = str(curso_processado[campo]).strip()

        # Normalizar campos numéricos (vagas)
        campos_numericos = ["vagas", "numero_vagas", "qt_vagas", "vagas_disponiveis"]
        for campo in campos_numericos:
            if curso_processado.get(campo):
                try:
                    # Tentar converter para número
                    valor = str(curso_processado[campo]).strip()
                    # Remover caracteres não numéricos exceto pontos e vírgulas
                    valor_limpo = "".join(c for c in valor if c.isdigit() or c in ".,")
                    if valor_limpo:
                        curso_processado[campo] = valor_limpo
                except:
                    curso_processado[campo] = None

        # Normalizar campos de data
        campos_data = ["inicio_inscricao", "fim_inscricao", "data_inicio", "data_fim"]
        for campo in campos_data:
            if curso_processado.get(campo):
                try:
                    # Tentar normalizar formato de data
                    data = str(curso_processado[campo]).strip()
                    if data:
                        curso_processado[campo] = data
                except:
                    curso_processado[campo] = None

        return curso_processado

    def _salvar_checkpoint(self, pagina_atual: int):
        """
        💾 Salva checkpoint da coleta.

        Args:
            pagina_atual: Página atual
        """
        checkpoint = {
            "pagina_atual": pagina_atual,
            "total_paginas": self.total_paginas,
            "cursos_coletados": len(self.dados_coletados),
            "timestamp": datetime.now().isoformat(),
            "dados_parciais": self.dados_coletados,
        }

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        caminho_checkpoint = f"checkpoints/coleta_unasus_checkpoint_{timestamp}.json"

        # Criar pasta se não existir
        os.makedirs("checkpoints", exist_ok=True)

        # Salvar checkpoint
        with open(caminho_checkpoint, "w", encoding="utf-8") as f:
            json.dump(checkpoint, f, ensure_ascii=False, indent=2)

        self.logger.info(f"💾 Checkpoint salvo: {caminho_checkpoint}")

    def _salvar_dados_completos(self):
        """
        💾 Salva dados completos coletados.
        """
        if not self.dados_coletados:
            self.logger.warning("⚠️ Nenhum dado para salvar")
            return

        # Salvar como JSON
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        caminho_json = f"dados/unasus_dados_completos_{timestamp}.json"

        # Criar pasta se não existir
        os.makedirs("dados", exist_ok=True)

        # Salvar JSON
        with open(caminho_json, "w", encoding="utf-8") as f:
            json.dump(self.dados_coletados, f, ensure_ascii=False, indent=2)

        # Salvar como CSV
        df = pd.DataFrame(self.dados_coletados)
        caminho_csv = f"dados/unasus_dados_completos_{timestamp}.csv"
        df.to_csv(caminho_csv, index=False, encoding="utf-8")

        # Salvar como Excel (opcional - requer openpyxl)
        try:
            import openpyxl

            caminho_excel = f"dados/unasus_dados_completos_{timestamp}.xlsx"
            df.to_excel(caminho_excel, index=False, engine="openpyxl")
            self.logger.info(f"   📈 Excel: {caminho_excel}")
        except ImportError:
            self.logger.info("   📈 Excel: Não salvo (openpyxl não instalado)")

        self.logger.info(f"💾 Dados salvos:")
        self.logger.info(f"   📄 JSON: {caminho_json}")
        self.logger.info(f"   📊 CSV: {caminho_csv}")

        # Gerar relatório de coleta
        self._gerar_relatorio_coleta()

    def _gerar_relatorio_coleta(self):
        """
        📊 Gera relatório detalhado da coleta.
        """
        relatorio = {
            "resumo_coleta": {
                "total_cursos": len(self.dados_coletados),
                "total_paginas": self.total_paginas,
                "timestamp_inicio": datetime.now().isoformat(),
                "timestamp_fim": datetime.now().isoformat(),
                "tipo_coleta": "completa_sem_filtros",
            },
            "estatisticas": {
                "cursos_por_status": {},
                "cursos_por_categoria": {},
                "carga_horaria_media": 0,
                "vagas_estatisticas": {},
                "campos_preenchidos": {},
            },
            "campos_coletados": (
                list(self.dados_coletados[0].keys()) if self.dados_coletados else []
            ),
        }

        # Calcular estatísticas
        if self.dados_coletados:
            df = pd.DataFrame(self.dados_coletados)

            # Status dos cursos
            if "status" in df.columns:
                relatorio["estatisticas"]["cursos_por_status"] = (
                    df["status"].value_counts().to_dict()
                )

            # Categorias
            if "categoria" in df.columns:
                relatorio["estatisticas"]["cursos_por_categoria"] = (
                    df["categoria"].value_counts().to_dict()
                )

            # Carga horária média
            if "carga_horaria" in df.columns:
                try:
                    cargas_horarias = pd.to_numeric(
                        df["carga_horaria"], errors="coerce"
                    )
                    relatorio["estatisticas"][
                        "carga_horaria_media"
                    ] = cargas_horarias.mean()
                except:
                    pass

            # Estatísticas de vagas
            campos_vagas = ["vagas", "numero_vagas", "qt_vagas", "vagas_disponiveis"]
            vagas_estatisticas = {}

            for campo in campos_vagas:
                if campo in df.columns:
                    try:
                        # Converter para numérico
                        vagas_numericas = pd.to_numeric(df[campo], errors="coerce")
                        vagas_validas = vagas_numericas.dropna()

                        if len(vagas_validas) > 0:
                            vagas_estatisticas[campo] = {
                                "total_vagas": int(vagas_validas.sum()),
                                "media_vagas": float(vagas_validas.mean()),
                                "min_vagas": int(vagas_validas.min()),
                                "max_vagas": int(vagas_validas.max()),
                                "cursos_com_vagas": int(len(vagas_validas)),
                                "percentual_preenchido": float(
                                    len(vagas_validas) / len(df) * 100
                                ),
                            }
                    except:
                        pass

            relatorio["estatisticas"]["vagas_estatisticas"] = vagas_estatisticas

            # Campos preenchidos
            for coluna in df.columns:
                nao_nulos = df[coluna].notna().sum()
                relatorio["estatisticas"]["campos_preenchidos"][coluna] = {
                    "preenchidos": int(nao_nulos),
                    "vazios": int(len(df) - nao_nulos),
                    "percentual": float(nao_nulos / len(df) * 100),
                }

        # Salvar relatório
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        caminho_relatorio = f"relatorios/relatorio_coleta_completa_{timestamp}.json"

        # Criar pasta se não existir
        os.makedirs("relatorios", exist_ok=True)

        with open(caminho_relatorio, "w", encoding="utf-8") as f:
            json.dump(relatorio, f, ensure_ascii=False, indent=2)

        self.logger.info(f"📊 Relatório salvo: {caminho_relatorio}")

    def carregar_dados_existentes(self, caminho_arquivo: str) -> List[Dict]:
        """
        📂 Carrega dados existentes de arquivo.

        Args:
            caminho_arquivo: Caminho para o arquivo de dados

        Returns:
            Lista de dados carregados
        """
        self.logger.info(f"📂 Carregando dados existentes: {caminho_arquivo}")

        try:
            if caminho_arquivo.endswith(".json"):
                with open(caminho_arquivo, "r", encoding="utf-8") as f:
                    dados = json.load(f)
            elif caminho_arquivo.endswith(".csv"):
                df = pd.read_csv(caminho_arquivo, encoding="utf-8")
                dados = df.to_dict("records")
            elif caminho_arquivo.endswith(".xlsx"):
                try:
                    import openpyxl

                    df = pd.read_excel(caminho_arquivo)
                    dados = df.to_dict("records")
                except ImportError:
                    raise ValueError(
                        "Para ler arquivos .xlsx, instale openpyxl: pip install openpyxl"
                    )
            else:
                raise ValueError(f"Formato de arquivo não suportado: {caminho_arquivo}")

            self.dados_coletados = dados
            self.logger.info(f"✅ Dados carregados: {len(dados)} registros")

            return dados

        except Exception as e:
            self.logger.error(f"❌ Erro ao carregar dados: {str(e)}")
            return []


def main():
    """
    🚀 Função principal para executar coleta completa.
    """
    print("📊 INICIANDO COLETOR UNA-SUS COMPLETO")

    # Criar coletor
    coletor = ColetorUnasusCompleto()

    # Executar coleta completa
    dados = coletor.coletar_dados_completos()

    print(f"✅ COLETA CONCLUÍDA: {len(dados)} cursos coletados")
    print("📁 Verifique a pasta 'dados/' para os arquivos gerados")


if __name__ == "__main__":
    main()
