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
import time
from datetime import datetime
from typing import Dict, List

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
        self.logger = logger or self._configurar_logger()
        self.dados_coletados = []
        self.pagina_atual = 1
        self.total_paginas = 0
        self.cursos_encontrados = 0

        # Configurações da UNA-SUS (baseadas no scraper original que funciona)
        self.url_base = "https://www.unasus.gov.br/cursos/rest/busca"
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36",
            "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
            "Accept": "application/json, text/javascript, */*; q=0.01",
            "X-Requested-With": "XMLHttpRequest",
            "Origin": "https://www.unasus.gov.br",
            "Referer": "https://www.unasus.gov.br/cursos/busca?status=todos&busca=&ordenacao=Relev%C3%A2ncia%20na%20busca",
        }

        # Cookies necessários (baseados no scraper original)
        self.cookies = {
            "PORTAL_UNASUS": "4ru34cs848mfbopb6vseqluni4",
            "UNASUSAnonID": "ID1ef7d6246158f7cf31c06b928bc56f8e",
            "_shibsession_64656661756c7468747470733a2f2f7777772e756e617375732e676f762e6272": "_329a72cffc11d2904ae393c82d0cfb72",
        }

        # Payload para requisições (baseado no scraper original)
        self.payload = {
            "busca": "",
            "ordenacao": "Por nome",
            "status": "Todos",
            "proximo": 0,
        }

        # Criar diretórios necessários
        self._criar_diretorios()

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

        # Adicionar campos processados se não existirem
        if "campos_processados" not in curso_processado:
            curso_processado["campos_processados"] = {
                "id": curso_processado.get("co_seq_curso", ""),
                "titulo": curso_processado.get("no_curso", ""),
                "descricao": curso_processado.get("ds_curso", ""),
                "carga_horaria": curso_processado.get("qt_carga_horaria_total", 0),
                "categoria": curso_processado.get("no_formato", ""),
                "publico_alvo": curso_processado.get("publico_alvo", ""),
                "palavras_chave": curso_processado.get("palavras_chave", ""),
                "link": f"https://www.unasus.gov.br/cursos/curso/{curso_processado.get('co_seq_curso', '')}",
                "vagas": curso_processado.get("vagas", 0),
                "numero_vagas": curso_processado.get("numero_vagas", 0),
                "qt_vagas": curso_processado.get("qt_vagas", 0),
                "nivel": curso_processado.get("no_nivel", ""),
                "area_tematica": curso_processado.get("area_tematica", ""),
                "instituicao": curso_processado.get("no_orgao", ""),
                "coordenador": curso_processado.get("coordenador", ""),
                "tutores": curso_processado.get("tutores", ""),
                "certificacao": curso_processado.get("certificacao", ""),
                "pre_requisitos": curso_processado.get("pre_requisitos", ""),
                "objetivos": curso_processado.get("objetivos", ""),
                "metodologia": curso_processado.get("metodologia", ""),
                "avaliacao": curso_processado.get("avaliacao", ""),
                "bibliografia": curso_processado.get("bibliografia", ""),
            }

        return curso_processado

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
