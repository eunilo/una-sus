"""
🗄️ MÓDULO DE BANCO DE DADOS ESTRUTURADO
=======================================

Este módulo gerencia a persistência e estruturação dos dados coletados,
permitindo exportação em múltiplos formatos para uso em outras instâncias.
"""

import csv
import json
import os
import sqlite3
import xml.etree.ElementTree as ET
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional

import pandas as pd
import yaml
from modulos.logger_config import LoggerConfig


class BancoDadosEstruturado:
    """
    🗄️ Gerenciador de banco de dados estruturado para o projeto Grounded Theory.

    Permite persistência em múltiplos formatos e facilita a interoperabilidade
    com outras aplicações e sistemas.
    """

    def __init__(self, nome_banco: str = "unasus_grounded_theory"):
        """
        Inicializa o banco de dados estruturado.

        Args:
            nome_banco: Nome base do banco de dados
        """
        self.nome_banco = nome_banco
        self.timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        self.logger = LoggerConfig.get_analysis_logger()

        # Criar diretórios necessários
        self.diretorios = {
            "dados": "dados",
            "banco_sqlite": "banco_sqlite",
            "exportacoes": "exportacoes",
            "schemas": "schemas",
        }

        for diretorio in self.diretorios.values():
            os.makedirs(diretorio, exist_ok=True)

        # Estrutura do banco
        self.estrutura_tabelas = {
            "cursos": {
                "id_curso": "TEXT PRIMARY KEY",
                "no_curso": "TEXT",
                "no_orgao": "TEXT",
                "sg_orgao": "TEXT",
                "no_formato": "TEXT",
                "no_nivel": "TEXT",
                "no_modalidade": "TEXT",
                "status": "TEXT",
                "area_tematica": "TEXT",
                "objetivos": "TEXT",
                "metodologia": "TEXT",
                "carga_horaria": "INTEGER",
                "vagas_ofertadas": "INTEGER",
                "vagas_disponiveis": "INTEGER",
                "data_inicio": "TEXT",
                "data_fim": "TEXT",
                "timestamp_coleta": "TEXT",
                "metadata_coleta": "TEXT",
            },
            "conceitos_identificados": {
                "id_conceito": "INTEGER PRIMARY KEY AUTOINCREMENT",
                "conceito": "TEXT",
                "frequencia": "INTEGER",
                "categoria": "TEXT",
                "etapa_codificacao": "TEXT",
                "timestamp_identificacao": "TEXT",
                "contexto": "TEXT",
            },
            "categorias": {
                "id_categoria": "INTEGER PRIMARY KEY AUTOINCREMENT",
                "nome_categoria": "TEXT",
                "descricao": "TEXT",
                "tipo_codificacao": "TEXT",
                "conceitos_relacionados": "TEXT",
                "timestamp_criacao": "TEXT",
            },
            "relacoes": {
                "id_relacao": "INTEGER PRIMARY KEY AUTOINCREMENT",
                "categoria_origem": "TEXT",
                "categoria_destino": "TEXT",
                "tipo_relacao": "TEXT",
                "forca_relacao": "REAL",
                "timestamp_relacao": "TEXT",
            },
            "analises_exploratorias": {
                "id_analise": "INTEGER PRIMARY KEY AUTOINCREMENT",
                "tipo_analise": "TEXT",
                "parametros": "TEXT",
                "resultados": "TEXT",
                "timestamp_analise": "TEXT",
            },
        }

        # Inicializar conexão SQLite
        self.caminho_sqlite = (
            f"{self.diretorios['banco_sqlite']}/{self.nome_banco}_{self.timestamp}.db"
        )
        self.inicializar_sqlite()

    def inicializar_sqlite(self):
        """Inicializa o banco SQLite com as tabelas necessárias."""
        try:
            self.conn = sqlite3.connect(self.caminho_sqlite)
            self.cursor = self.conn.cursor()

            # Criar tabelas
            for nome_tabela, colunas in self.estrutura_tabelas.items():
                self._criar_tabela(nome_tabela, colunas)

            self.logger.info(f"🗄️ Banco SQLite inicializado: {self.caminho_sqlite}")

        except Exception as e:
            self.logger.error(f"❌ Erro ao inicializar SQLite: {str(e)}")
            raise

    def _criar_tabela(self, nome_tabela: str, colunas: Dict[str, str]):
        """Cria uma tabela no banco SQLite."""
        colunas_sql = ", ".join(
            [f"{coluna} {tipo}" for coluna, tipo in colunas.items()]
        )
        query = f"CREATE TABLE IF NOT EXISTS {nome_tabela} ({colunas_sql})"

        try:
            self.cursor.execute(query)
            self.conn.commit()
            self.logger.debug(f"📋 Tabela '{nome_tabela}' criada/verificada")
        except Exception as e:
            self.logger.error(f"❌ Erro ao criar tabela '{nome_tabela}': {str(e)}")

    def inserir_cursos(self, cursos: List[Dict]):
        """
        Insere cursos no banco de dados.

        Args:
            cursos: Lista de dicionários com dados dos cursos
        """
        try:
            for curso in cursos:
                # Preparar dados para inserção
                dados_curso = {
                    "id_curso": curso.get("id_curso", ""),
                    "no_curso": curso.get("no_curso", ""),
                    "no_orgao": curso.get("no_orgao", ""),
                    "sg_orgao": curso.get("sg_orgao", ""),
                    "no_formato": curso.get("no_formato", ""),
                    "no_nivel": curso.get("no_nivel", ""),
                    "no_modalidade": curso.get("no_modalidade", ""),
                    "status": curso.get("status", ""),
                    "area_tematica": curso.get("area_tematica", ""),
                    "objetivos": curso.get("objetivos", ""),
                    "metodologia": curso.get("metodologia", ""),
                    "carga_horaria": curso.get("carga_horaria", 0),
                    "vagas_ofertadas": curso.get("vagas_ofertadas", 0),
                    "vagas_disponiveis": curso.get("vagas_disponiveis", 0),
                    "data_inicio": curso.get("data_inicio", ""),
                    "data_fim": curso.get("data_fim", ""),
                    "timestamp_coleta": curso.get("metadata_coleta", {}).get(
                        "timestamp_coleta", ""
                    ),
                    "metadata_coleta": json.dumps(curso.get("metadata_coleta", {})),
                }

                # Inserir no SQLite
                colunas = ", ".join(dados_curso.keys())
                placeholders = ", ".join(["?" for _ in dados_curso])
                query = (
                    f"INSERT OR REPLACE INTO cursos ({colunas}) VALUES ({placeholders})"
                )

                self.cursor.execute(query, list(dados_curso.values()))

            self.conn.commit()
            self.logger.info(f"✅ {len(cursos)} cursos inseridos no banco")

        except Exception as e:
            self.logger.error(f"❌ Erro ao inserir cursos: {str(e)}")
            raise

    def inserir_conceitos(self, conceitos: List[Dict]):
        """
        Insere conceitos identificados no banco de dados.

        Args:
            conceitos: Lista de dicionários com conceitos identificados
        """
        try:
            for conceito in conceitos:
                dados_conceito = {
                    "conceito": conceito.get("conceito", ""),
                    "frequencia": conceito.get("frequencia", 0),
                    "categoria": conceito.get("categoria", ""),
                    "etapa_codificacao": conceito.get("etapa_codificacao", ""),
                    "timestamp_identificacao": datetime.now().isoformat(),
                    "contexto": json.dumps(conceito.get("contexto", {})),
                }

                colunas = ", ".join(dados_conceito.keys())
                placeholders = ", ".join(["?" for _ in dados_conceito])
                query = f"INSERT INTO conceitos_identificados ({colunas}) VALUES ({placeholders})"

                self.cursor.execute(query, list(dados_conceito.values()))

            self.conn.commit()
            self.logger.info(f"✅ {len(conceitos)} conceitos inseridos no banco")

        except Exception as e:
            self.logger.error(f"❌ Erro ao inserir conceitos: {str(e)}")
            raise

    def inserir_categorias(self, categorias: List[Dict]):
        """
        Insere categorias no banco de dados.

        Args:
            categorias: Lista de dicionários com categorias
        """
        try:
            for categoria in categorias:
                dados_categoria = {
                    "nome_categoria": categoria.get("nome", ""),
                    "descricao": categoria.get("descricao", ""),
                    "tipo_codificacao": categoria.get("tipo", ""),
                    "conceitos_relacionados": json.dumps(
                        categoria.get("conceitos", [])
                    ),
                    "timestamp_criacao": datetime.now().isoformat(),
                }

                colunas = ", ".join(dados_categoria.keys())
                placeholders = ", ".join(["?" for _ in dados_categoria])
                query = f"INSERT INTO categorias ({colunas}) VALUES ({placeholders})"

                self.cursor.execute(query, list(dados_categoria.values()))

            self.conn.commit()
            self.logger.info(f"✅ {len(categorias)} categorias inseridas no banco")

        except Exception as e:
            self.logger.error(f"❌ Erro ao inserir categorias: {str(e)}")
            raise

    def exportar_para_csv(self, tabela: str, caminho_saida: str = None):
        """
        Exporta uma tabela para CSV.

        Args:
            tabela: Nome da tabela a ser exportada
            caminho_saida: Caminho do arquivo de saída
        """
        try:
            if caminho_saida is None:
                caminho_saida = (
                    f"{self.diretorios['exportacoes']}/{tabela}_{self.timestamp}.csv"
                )

            query = f"SELECT * FROM {tabela}"
            df = pd.read_sql_query(query, self.conn)
            df.to_csv(caminho_saida, index=False, encoding="utf-8")

            self.logger.info(
                f"📊 Tabela '{tabela}' exportada para CSV: {caminho_saida}"
            )
            return caminho_saida

        except Exception as e:
            self.logger.error(f"❌ Erro ao exportar CSV: {str(e)}")
            raise

    def exportar_para_json(self, tabela: str, caminho_saida: str = None):
        """
        Exporta uma tabela para JSON.

        Args:
            tabela: Nome da tabela a ser exportada
            caminho_saida: Caminho do arquivo de saída
        """
        try:
            if caminho_saida is None:
                caminho_saida = (
                    f"{self.diretorios['exportacoes']}/{tabela}_{self.timestamp}.json"
                )

            query = f"SELECT * FROM {tabela}"
            df = pd.read_sql_query(query, self.conn)

            # Converter para formato JSON estruturado
            dados_json = {
                "metadata": {
                    "tabela": tabela,
                    "timestamp_exportacao": datetime.now().isoformat(),
                    "total_registros": len(df),
                    "colunas": list(df.columns),
                },
                "dados": df.to_dict("records"),
            }

            with open(caminho_saida, "w", encoding="utf-8") as f:
                json.dump(dados_json, f, ensure_ascii=False, indent=2)

            self.logger.info(
                f"📄 Tabela '{tabela}' exportada para JSON: {caminho_saida}"
            )
            return caminho_saida

        except Exception as e:
            self.logger.error(f"❌ Erro ao exportar JSON: {str(e)}")
            raise

    def exportar_para_xml(self, tabela: str, caminho_saida: str = None):
        """
        Exporta uma tabela para XML.

        Args:
            tabela: Nome da tabela a ser exportada
            caminho_saida: Caminho do arquivo de saída
        """
        try:
            if caminho_saida is None:
                caminho_saida = (
                    f"{self.diretorios['exportacoes']}/{tabela}_{self.timestamp}.xml"
                )

            query = f"SELECT * FROM {tabela}"
            df = pd.read_sql_query(query, self.conn)

            # Criar estrutura XML
            root = ET.Element("dados")
            root.set("tabela", tabela)
            root.set("timestamp", datetime.now().isoformat())
            root.set("total_registros", str(len(df)))

            # Adicionar metadados
            metadata = ET.SubElement(root, "metadata")
            colunas = ET.SubElement(metadata, "colunas")
            for coluna in df.columns:
                col = ET.SubElement(colunas, "coluna")
                col.text = coluna

            # Adicionar dados
            dados = ET.SubElement(root, "dados")
            for _, row in df.iterrows():
                registro = ET.SubElement(dados, "registro")
                for coluna, valor in row.items():
                    campo = ET.SubElement(registro, coluna)
                    campo.text = str(valor) if valor is not None else ""

            # Salvar arquivo
            tree = ET.ElementTree(root)
            tree.write(caminho_saida, encoding="utf-8", xml_declaration=True)

            self.logger.info(
                f"📋 Tabela '{tabela}' exportada para XML: {caminho_saida}"
            )
            return caminho_saida

        except Exception as e:
            self.logger.error(f"❌ Erro ao exportar XML: {str(e)}")
            raise

    def exportar_para_yaml(self, tabela: str, caminho_saida: str = None):
        """
        Exporta uma tabela para YAML.

        Args:
            tabela: Nome da tabela a ser exportada
            caminho_saida: Caminho do arquivo de saída
        """
        try:
            if caminho_saida is None:
                caminho_saida = (
                    f"{self.diretorios['exportacoes']}/{tabela}_{self.timestamp}.yaml"
                )

            query = f"SELECT * FROM {tabela}"
            df = pd.read_sql_query(query, self.conn)

            # Estruturar dados para YAML
            dados_yaml = {
                "metadata": {
                    "tabela": tabela,
                    "timestamp_exportacao": datetime.now().isoformat(),
                    "total_registros": len(df),
                    "colunas": list(df.columns),
                },
                "dados": df.to_dict("records"),
            }

            with open(caminho_saida, "w", encoding="utf-8") as f:
                yaml.dump(dados_yaml, f, default_flow_style=False, allow_unicode=True)

            self.logger.info(
                f"📝 Tabela '{tabela}' exportada para YAML: {caminho_saida}"
            )
            return caminho_saida

        except Exception as e:
            self.logger.error(f"❌ Erro ao exportar YAML: {str(e)}")
            raise

    def exportar_todas_tabelas(self, formato: str = "todos"):
        """
        Exporta todas as tabelas para o formato especificado.

        Args:
            formato: Formato de exportação ('csv', 'json', 'xml', 'yaml', 'todos')
        """
        try:
            tabelas = list(self.estrutura_tabelas.keys())
            arquivos_exportados = {}

            for tabela in tabelas:
                arquivos_exportados[tabela] = {}

                if formato in ["csv", "todos"]:
                    arquivos_exportados[tabela]["csv"] = self.exportar_para_csv(tabela)

                if formato in ["json", "todos"]:
                    arquivos_exportados[tabela]["json"] = self.exportar_para_json(
                        tabela
                    )

                if formato in ["xml", "todos"]:
                    arquivos_exportados[tabela]["xml"] = self.exportar_para_xml(tabela)

                if formato in ["yaml", "todos"]:
                    arquivos_exportados[tabela]["yaml"] = self.exportar_para_yaml(
                        tabela
                    )

            self.logger.info(f"✅ Todas as tabelas exportadas no formato: {formato}")
            return arquivos_exportados

        except Exception as e:
            self.logger.error(f"❌ Erro ao exportar todas as tabelas: {str(e)}")
            raise

    def gerar_relatorio_banco(self):
        """
        Gera um relatório completo do banco de dados.

        Returns:
            Dicionário com estatísticas do banco
        """
        try:
            relatorio = {
                "metadata": {
                    "nome_banco": self.nome_banco,
                    "timestamp": self.timestamp,
                    "caminho_sqlite": self.caminho_sqlite,
                },
                "estatisticas": {},
                "tabelas": {},
            }

            # Estatísticas por tabela
            for tabela in self.estrutura_tabelas.keys():
                try:
                    self.cursor.execute(f"SELECT COUNT(*) FROM {tabela}")
                    total_registros = self.cursor.fetchone()[0]

                    self.cursor.execute(f"PRAGMA table_info({tabela})")
                    colunas = self.cursor.fetchall()

                    relatorio["tabelas"][tabela] = {
                        "total_registros": total_registros,
                        "colunas": len(colunas),
                        "estrutura": {col[1]: col[2] for col in colunas},
                    }

                except Exception as e:
                    self.logger.warning(
                        f"⚠️ Erro ao obter estatísticas da tabela '{tabela}': {str(e)}"
                    )

            # Salvar relatório
            caminho_relatorio = f"{self.diretorios['exportacoes']}/relatorio_banco_{self.timestamp}.json"
            with open(caminho_relatorio, "w", encoding="utf-8") as f:
                json.dump(relatorio, f, ensure_ascii=False, indent=2)

            self.logger.info(f"📋 Relatório do banco gerado: {caminho_relatorio}")
            return relatorio

        except Exception as e:
            self.logger.error(f"❌ Erro ao gerar relatório: {str(e)}")
            raise

    def fechar_conexao(self):
        """Fecha a conexão com o banco SQLite."""
        try:
            if hasattr(self, "conn"):
                self.conn.close()
                self.logger.info("🔒 Conexão com banco SQLite fechada")
        except Exception as e:
            self.logger.error(f"❌ Erro ao fechar conexão: {str(e)}")

    def __enter__(self):
        """Context manager entry."""
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit."""
        self.fechar_conexao()


class GerenciadorDados:
    """
    🗂️ Gerenciador de dados para facilitar a integração com o banco estruturado.
    """

    def __init__(self):
        """Inicializa o gerenciador de dados."""
        self.logger = LoggerConfig.get_analysis_logger()
        self.banco = None

    def inicializar_banco(self, nome_banco: str = "unasus_grounded_theory"):
        """Inicializa o banco de dados."""
        self.banco = BancoDadosEstruturado(nome_banco)
        self.logger.info(f"🗄️ Banco de dados inicializado: {nome_banco}")

    def salvar_dados_coleta(self, dados_coletados: List[Dict]):
        """
        Salva dados de coleta no banco estruturado.

        Args:
            dados_coletados: Lista de dados coletados
        """
        if self.banco is None:
            self.inicializar_banco()

        try:
            # Salvar no banco SQLite
            self.banco.inserir_cursos(dados_coletados)

            # Salvar backup em JSON
            caminho_json = f"dados/dados_coletados_{self.banco.timestamp}.json"
            with open(caminho_json, "w", encoding="utf-8") as f:
                json.dump(dados_coletados, f, ensure_ascii=False, indent=2)

            self.logger.info(f"💾 Dados salvos: {len(dados_coletados)} registros")
            return caminho_json

        except Exception as e:
            self.logger.error(f"❌ Erro ao salvar dados: {str(e)}")
            raise

    def salvar_resultados_codificacao(self, resultados: Dict):
        """
        Salva resultados de codificação no banco estruturado.

        Args:
            resultados: Dicionário com resultados de codificação
        """
        if self.banco is None:
            self.inicializar_banco()

        try:
            # Salvar conceitos
            if "conceitos_identificados" in resultados:
                self.banco.inserir_conceitos(resultados["conceitos_identificados"])

            # Salvar categorias
            if "categorias" in resultados:
                self.banco.inserir_categorias(resultados["categorias"])

            self.logger.info("💾 Resultados de codificação salvos no banco")

        except Exception as e:
            self.logger.error(f"❌ Erro ao salvar resultados: {str(e)}")
            raise

    def exportar_dados_completos(self, formato: str = "todos"):
        """
        Exporta todos os dados em múltiplos formatos.

        Args:
            formato: Formato de exportação
        """
        if self.banco is None:
            self.logger.error("❌ Banco de dados não inicializado")
            return

        try:
            arquivos = self.banco.exportar_todas_tabelas(formato)
            relatorio = self.banco.gerar_relatorio_banco()

            self.logger.info(f"📤 Dados exportados em formato: {formato}")
            return arquivos, relatorio

        except Exception as e:
            self.logger.error(f"❌ Erro ao exportar dados: {str(e)}")
            raise

    def fechar_banco(self):
        """Fecha o banco de dados."""
        if self.banco:
            self.banco.fechar_conexao()
            self.logger.info("🔒 Banco de dados fechado")
