#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Analisador Geral - Sistema de Análise UNA-SUS
=============================================

Módulo principal de análise que carrega e processa o banco de dados
criado pela varredura inicial.
"""

import os
import sqlite3
from datetime import datetime
from typing import Dict, List, Optional

import pandas as pd

from analise.cobertura_programatica import CoberturaProgramatica
from analise.distribuicao_geografica import DistribuicaoGeografica
from analise.estatisticas_basicas import (
    calcular_estatisticas_categoricas,
    calcular_estatisticas_numericas,
    gerar_resumo_colunas,
    identificar_colunas_problematicas,
)
from analise.mapeamento_programas import MapeamentoProgramas


class AnalisadorGeral:
    """
    Analisador geral do banco de dados UNA-SUS.
    """

    def __init__(self):
        """Inicializa o analisador."""
        self.dados = None
        self.database_path = None
        self.csv_path = None
        self.estatisticas = {}

    def carregar_dados(self) -> bool:
        """
        Carrega os dados do banco de dados ou CSV.

        Returns:
            True se os dados foram carregados com sucesso
        """
        # Procurar por arquivos de dados na raiz e na pasta data/
        diretorios = [".", "data"]
        arquivos_db = []
        arquivos_csv = []

        for diretorio in diretorios:
            if os.path.exists(diretorio):
                arquivos_db.extend(
                    [
                        os.path.join(diretorio, f)
                        for f in os.listdir(diretorio)
                        if f.endswith(".db")
                    ]
                )
                arquivos_csv.extend(
                    [
                        os.path.join(diretorio, f)
                        for f in os.listdir(diretorio)
                        if f.endswith(".csv")
                    ]
                )

        if arquivos_db:
            # Pegar o arquivo mais recente
            arquivos_db.sort(key=lambda x: os.path.getmtime(x), reverse=True)
            self.database_path = arquivos_db[0]
            return self._carregar_database()
        elif arquivos_csv:
            # Pegar o arquivo mais recente
            arquivos_csv.sort(key=lambda x: os.path.getmtime(x), reverse=True)
            self.csv_path = arquivos_csv[0]
            return self._carregar_csv()
        else:
            print("❌ Nenhum arquivo de dados encontrado!")
            print("💡 Execute primeiro a varredura completa")
            return False

    def _carregar_database(self) -> bool:
        """Carrega dados do SQLite."""
        try:
            print(f"📊 Carregando database: {self.database_path}")

            # Conectar ao banco
            conn = sqlite3.connect(self.database_path)

            # Verificar tabelas
            cursor = conn.cursor()
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
            tabelas = cursor.fetchall()

            if not tabelas:
                print("❌ Nenhuma tabela encontrada no database!")
                return False

            # Carregar dados da primeira tabela (assumindo que é a principal)
            tabela_principal = tabelas[0][0]
            self.dados = pd.read_sql_query(f"SELECT * FROM {tabela_principal}", conn)

            conn.close()

            print(f"✅ Dados carregados: {len(self.dados)} registros")
            return True

        except Exception as e:
            print(f"❌ Erro ao carregar database: {e}")
            return False

    def _carregar_csv(self) -> bool:
        """Carrega dados do CSV."""
        try:
            print(f"📊 Carregando CSV: {self.csv_path}")

            self.dados = pd.read_csv(self.csv_path)

            print(f"✅ Dados carregados: {len(self.dados)} registros")
            return True

        except Exception as e:
            print(f"❌ Erro ao carregar CSV: {e}")
            return False

    def gerar_estatisticas_basicas(self) -> Dict:
        """
        Gera estatísticas básicas dos dados.

        Returns:
            Dicionário com estatísticas
        """
        if self.dados is None:
            print("❌ Dados não carregados!")
            return {}

        print("📊 Gerando estatísticas básicas...")

        stats = {
            "total_registros": len(self.dados),
            "total_colunas": len(self.dados.columns),
            "colunas": list(self.dados.columns),
            "tipos_dados": self.dados.dtypes.to_dict(),
            "valores_nulos": self.dados.isnull().sum().to_dict(),
            "memoria_uso": self.dados.memory_usage(deep=True).sum(),
            "timestamp_analise": datetime.now().isoformat(),
        }

        # Estatísticas por coluna
        stats["colunas_info"] = {}
        for coluna in self.dados.columns:
            col_info = {
                "tipo": str(self.dados[coluna].dtype),
                "valores_unicos": self.dados[coluna].nunique(),
                "valores_nulos": self.dados[coluna].isnull().sum(),
                "percentual_nulos": (
                    self.dados[coluna].isnull().sum() / len(self.dados)
                )
                * 100,
            }

            # Para colunas numéricas
            if pd.api.types.is_numeric_dtype(self.dados[coluna]):
                col_info.update(
                    {
                        "min": self.dados[coluna].min(),
                        "max": self.dados[coluna].max(),
                        "media": self.dados[coluna].mean(),
                        "mediana": self.dados[coluna].median(),
                    }
                )

            # Para colunas de texto
            elif pd.api.types.is_string_dtype(self.dados[coluna]):
                col_info["valores_mais_comuns"] = (
                    self.dados[coluna].value_counts().head(5).to_dict()
                )

            stats["colunas_info"][coluna] = col_info

        self.estatisticas = stats
        print("✅ Estatísticas geradas!")

        return stats

    def analisar_cursos(self) -> Dict:
        """
        Análise específica dos cursos.

        Returns:
            Dicionário com análise dos cursos
        """
        if self.dados is None:
            print("❌ Dados não carregados!")
            return {}

        print("📚 Analisando cursos...")

        analise = {
            "total_cursos": 0,
            "cursos_unicos": 0,
            "areas_tematicas": {},
            "niveis": {},
            "instituicoes": {},
            "categorias": {},
        }

        # Identificar colunas relevantes
        colunas_curso = [
            col
            for col in self.dados.columns
            if any(
                termo in col.lower()
                for termo in [
                    "curso",
                    "titulo",
                    "area",
                    "nivel",
                    "instituicao",
                    "categoria",
                ]
            )
        ]

        if "no_curso" in self.dados.columns:
            analise["total_cursos"] = len(self.dados)
            analise["cursos_unicos"] = self.dados["no_curso"].nunique()

            # Análise por área temática
            if "area_tematica" in self.dados.columns:
                analise["areas_tematicas"] = (
                    self.dados["area_tematica"].value_counts().to_dict()
                )

            # Análise por nível
            if "no_nivel" in self.dados.columns:
                analise["niveis"] = self.dados["no_nivel"].value_counts().to_dict()

            # Análise por instituição
            if "no_orgao" in self.dados.columns:
                analise["instituicoes"] = (
                    self.dados["no_orgao"].value_counts().to_dict()
                )

            # Análise por categoria/formato
            if "no_formato" in self.dados.columns:
                analise["categorias"] = (
                    self.dados["no_formato"].value_counts().to_dict()
                )

        print("✅ Análise de cursos concluída!")
        return analise

    def analisar_ofertas(self) -> Dict:
        """
        Análise específica das ofertas.

        Returns:
            Dicionário com análise das ofertas
        """
        if self.dados is None:
            print("❌ Dados não carregados!")
            return {}

        print("🎯 Analisando ofertas...")

        analise = {
            "total_ofertas": 0,
            "ofertas_unicas": 0,
            "vagas_disponiveis": 0,
            "locais_oferta": {},
            "formatos_oferta": {},
            "publicos_alvo": {},
        }

        # Identificar colunas de oferta
        if "id_oferta" in self.dados.columns:
            analise["total_ofertas"] = len(self.dados)
            analise["ofertas_unicas"] = self.dados["id_oferta"].nunique()

            # Análise de vagas
            if "vagas" in self.dados.columns:
                vagas_numericas = pd.to_numeric(self.dados["vagas"], errors="coerce")
                analise["vagas_disponiveis"] = vagas_numericas.sum()
                analise["media_vagas"] = vagas_numericas.mean()

            # Análise por local
            if "local_oferta" in self.dados.columns:
                analise["locais_oferta"] = (
                    self.dados["local_oferta"].value_counts().to_dict()
                )

            # Análise por formato
            if "formato" in self.dados.columns:
                analise["formatos_oferta"] = (
                    self.dados["formato"].value_counts().to_dict()
                )

            # Análise por público-alvo
            if "publico_alvo" in self.dados.columns:
                analise["publicos_alvo"] = (
                    self.dados["publico_alvo"].value_counts().head(10).to_dict()
                )

        print("✅ Análise de ofertas concluída!")
        return analise

    def analisar_programas_governo(self) -> Dict:
        """
        Análise específica de programas de governo.

        Returns:
            Dicionário com análise de programas
        """
        if self.dados is None:
            print("❌ Dados não carregados!")
            return {}

        print("🏛️ Analisando programas de governo...")

        analise = {
            "mapeamento_programas": {},
            "cobertura_programatica": {},
            "distribuicao_geografica": {},
        }

        # Mapeamento de programas
        mapeador = MapeamentoProgramas()
        mapeador.carregar_dados(self.dados)
        analise["mapeamento_programas"] = mapeador.mapear_programas()

        # Cobertura programática
        cobertura = CoberturaProgramatica()
        cobertura.carregar_dados(self.dados)
        analise["cobertura_programatica"] = cobertura.analisar_cobertura()

        # Distribuição geográfica
        distribuicao = DistribuicaoGeografica()
        distribuicao.carregar_dados(self.dados)
        analise["distribuicao_geografica"] = distribuicao.analisar_distribuicao()

        print("✅ Análise de programas de governo concluída!")
        return analise

    def gerar_relatorio_completo(self) -> Dict:
        """
        Gera relatório completo de análise.

        Returns:
            Dicionário com relatório completo
        """
        print("📋 Gerando relatório completo...")

        relatorio = {
            "metadata": {
                "timestamp": datetime.now().isoformat(),
                "arquivo_dados": self.database_path or self.csv_path,
                "versao_analisador": "1.0.0",
            },
            "estatisticas_basicas": self.gerar_estatisticas_basicas(),
            "analise_cursos": self.analisar_cursos(),
            "analise_ofertas": self.analisar_ofertas(),
            "analise_programas": self.analisar_programas_governo(),
        }

        print("✅ Relatório completo gerado!")
        return relatorio


def main():
    """Função principal para teste do analisador."""
    analisador = AnalisadorGeral()

    if analisador.carregar_dados():
        relatorio = analisador.gerar_relatorio_completo()
        print("\n📊 RELATÓRIO RESUMIDO:")
        print(
            f"Total de registros: {relatorio['estatisticas_basicas']['total_registros']}"
        )
        print(f"Total de colunas: {relatorio['estatisticas_basicas']['total_colunas']}")
        print(f"Total de cursos únicos: {relatorio['analise_cursos']['cursos_unicos']}")
        print(
            f"Total de ofertas únicas: {relatorio['analise_ofertas']['ofertas_unicas']}"
        )


if __name__ == "__main__":
    main()
