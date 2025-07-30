#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Estatísticas Básicas - Sistema de Análise UNA-SUS
=================================================

Módulo para geração de estatísticas básicas dos dados.
"""

from typing import Dict, List

import pandas as pd


def calcular_estatisticas_numericas(dados: pd.DataFrame, coluna: str) -> Dict:
    """
    Calcula estatísticas para colunas numéricas.

    Args:
        dados: DataFrame com os dados
        coluna: Nome da coluna para análise

    Returns:
        Dicionário com estatísticas
    """
    if coluna not in dados.columns:
        return {}

    col_dados = pd.to_numeric(dados[coluna], errors="coerce")

    return {
        "min": col_dados.min(),
        "max": col_dados.max(),
        "media": col_dados.mean(),
        "mediana": col_dados.median(),
        "desvio_padrao": col_dados.std(),
        "quartil_25": col_dados.quantile(0.25),
        "quartil_75": col_dados.quantile(0.75),
        "valores_unicos": col_dados.nunique(),
        "valores_nulos": col_dados.isnull().sum(),
    }


def calcular_estatisticas_categoricas(
    dados: pd.DataFrame, coluna: str, top_n: int = 10
) -> Dict:
    """
    Calcula estatísticas para colunas categóricas.

    Args:
        dados: DataFrame com os dados
        coluna: Nome da coluna para análise
        top_n: Número de valores mais frequentes para mostrar

    Returns:
        Dicionário com estatísticas
    """
    if coluna not in dados.columns:
        return {}

    col_dados = dados[coluna]

    return {
        "valores_unicos": col_dados.nunique(),
        "valores_nulos": col_dados.isnull().sum(),
        "percentual_nulos": (col_dados.isnull().sum() / len(col_dados)) * 100,
        "valores_mais_frequentes": col_dados.value_counts().head(top_n).to_dict(),
        "valores_menos_frequentes": col_dados.value_counts().tail(top_n).to_dict(),
    }


def gerar_resumo_colunas(dados: pd.DataFrame) -> Dict:
    """
    Gera resumo de todas as colunas.

    Args:
        dados: DataFrame com os dados

    Returns:
        Dicionário com resumo das colunas
    """
    resumo = {}

    for coluna in dados.columns:
        col_info = {
            "tipo": str(dados[coluna].dtype),
            "valores_unicos": dados[coluna].nunique(),
            "valores_nulos": dados[coluna].isnull().sum(),
            "percentual_preenchido": (
                (len(dados) - dados[coluna].isnull().sum()) / len(dados)
            )
            * 100,
        }

        # Estatísticas específicas por tipo
        if pd.api.types.is_numeric_dtype(dados[coluna]):
            col_info["estatisticas_numericas"] = calcular_estatisticas_numericas(
                dados, coluna
            )
        else:
            col_info["estatisticas_categoricas"] = calcular_estatisticas_categoricas(
                dados, coluna
            )

        resumo[coluna] = col_info

    return resumo


def identificar_colunas_problematicas(
    dados: pd.DataFrame, limite_nulos: float = 0.5, limite_unicos: int = 1
) -> Dict:
    """
    Identifica colunas com problemas (muitos nulos, poucos valores únicos).

    Args:
        dados: DataFrame com os dados
        limite_nulos: Percentual máximo de valores nulos aceitável
        limite_unicos: Número mínimo de valores únicos aceitável

    Returns:
        Dicionário com colunas problemáticas
    """
    problematicas = {"muitos_nulos": [], "poucos_unicos": [], "colunas_vazias": []}

    for coluna in dados.columns:
        percentual_nulos = dados[coluna].isnull().sum() / len(dados)
        valores_unicos = dados[coluna].nunique()

        if percentual_nulos > limite_nulos:
            problematicas["muitos_nulos"].append(
                {"coluna": coluna, "percentual_nulos": percentual_nulos * 100}
            )

        if valores_unicos <= limite_unicos:
            problematicas["poucos_unicos"].append(
                {"coluna": coluna, "valores_unicos": valores_unicos}
            )

        if percentual_nulos == 1.0:
            problematicas["colunas_vazias"].append(coluna)

    return problematicas
