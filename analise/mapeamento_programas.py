#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Mapeamento de Programas - Sistema de Análise UNA-SUS
====================================================

Módulo para mapeamento de cursos por programa de governo.
"""

from datetime import datetime
from typing import Any, Dict, List

import pandas as pd


class MapeamentoProgramas:
    """
    Mapeamento de cursos por programa de governo.
    """

    def __init__(self, dados: pd.DataFrame = None):
        """
        Inicializa o mapeamento de programas.

        Args:
            dados: DataFrame com os dados
        """
        self.dados = dados
        self.mapeamento = {}

    def carregar_dados(self, dados: pd.DataFrame):
        """Carrega dados para análise."""
        self.dados = dados

    def mapear_programas(self) -> Dict[str, Any]:
        """
        Mapeia todos os programas de governo encontrados.

        Returns:
            Dicionário com mapeamento completo
        """
        if self.dados is None:
            return {}

        print("📊 Mapeando programas de governo...")

        # Identificar coluna de programas
        coluna_programas = None
        for col in self.dados.columns:
            if "programa" in col.lower() or "programas" in col.lower():
                coluna_programas = col
                break

        if coluna_programas is None:
            print("⚠️ Coluna de programas não encontrada!")
            return {}

        # Mapeamento básico
        mapeamento = {
            "total_cursos": len(self.dados),
            "total_ofertas": len(self.dados),
            "coluna_programas": coluna_programas,
            "programas_unicos": 0,
            "programas_encontrados": {},
            "cursos_por_programa": {},
            "ofertas_por_programa": {},
            "vagas_por_programa": {},
            "timestamp_analise": datetime.now().isoformat(),
        }

        # Contar programas únicos
        programas_unicos = self.dados[coluna_programas].dropna().unique()
        mapeamento["programas_unicos"] = len(programas_unicos)

        # Mapear cada programa
        for programa in programas_unicos:
            if pd.isna(programa) or programa == "":
                continue

            # Filtrar dados do programa
            dados_programa = self.dados[self.dados[coluna_programas] == programa]

            # Estatísticas do programa
            stats_programa = {
                "quantidade_cursos": len(dados_programa),
                "quantidade_ofertas": len(dados_programa),
                "cursos_unicos": (
                    dados_programa.get("no_curso", pd.Series()).nunique()
                    if "no_curso" in dados_programa.columns
                    else 0
                ),
                "ofertas_unicas": (
                    dados_programa.get("id_oferta", pd.Series()).nunique()
                    if "id_oferta" in dados_programa.columns
                    else 0
                ),
                "instituicoes": (
                    dados_programa.get("no_orgao", pd.Series()).nunique()
                    if "no_orgao" in dados_programa.columns
                    else 0
                ),
                "areas_tematicas": (
                    dados_programa.get("area_tematica", pd.Series()).nunique()
                    if "area_tematica" in dados_programa.columns
                    else 0
                ),
                "niveis": (
                    dados_programa.get("no_nivel", pd.Series()).nunique()
                    if "no_nivel" in dados_programa.columns
                    else 0
                ),
                "modalidades": (
                    dados_programa.get("no_formato", pd.Series()).nunique()
                    if "no_formato" in dados_programa.columns
                    else 0
                ),
            }

            # Calcular vagas se disponível
            if "vagas" in dados_programa.columns:
                vagas_numericas = pd.to_numeric(
                    dados_programa["vagas"], errors="coerce"
                )
                stats_programa["total_vagas"] = vagas_numericas.sum()
                stats_programa["media_vagas_por_oferta"] = vagas_numericas.mean()
            else:
                stats_programa["total_vagas"] = 0
                stats_programa["media_vagas_por_oferta"] = 0

            # Adicionar ao mapeamento
            mapeamento["programas_encontrados"][programa] = stats_programa

            # Contadores por programa
            mapeamento["cursos_por_programa"][programa] = stats_programa[
                "quantidade_cursos"
            ]
            mapeamento["ofertas_por_programa"][programa] = stats_programa[
                "quantidade_ofertas"
            ]
            mapeamento["vagas_por_programa"][programa] = stats_programa["total_vagas"]

        # Ordenar por quantidade de cursos
        mapeamento["programas_ordenados_por_cursos"] = dict(
            sorted(
                mapeamento["cursos_por_programa"].items(),
                key=lambda x: x[1],
                reverse=True,
            )
        )

        # Ordenar por quantidade de ofertas
        mapeamento["programas_ordenados_por_ofertas"] = dict(
            sorted(
                mapeamento["ofertas_por_programa"].items(),
                key=lambda x: x[1],
                reverse=True,
            )
        )

        # Ordenar por quantidade de vagas
        mapeamento["programas_ordenados_por_vagas"] = dict(
            sorted(
                mapeamento["vagas_por_programa"].items(),
                key=lambda x: x[1],
                reverse=True,
            )
        )

        self.mapeamento = mapeamento
        print(
            f"✅ Mapeamento concluído: {mapeamento['programas_unicos']} programas encontrados"
        )

        return mapeamento

    def gerar_resumo_programas(self) -> str:
        """
        Gera resumo textual do mapeamento.

        Returns:
            String com resumo formatado
        """
        if not self.mapeamento:
            return "❌ Nenhum mapeamento disponível!"

        texto = []
        texto.append("📊 MAPEAMENTO DE PROGRAMAS DE GOVERNO")
        texto.append("=" * 50)
        texto.append(f"Total de programas: {self.mapeamento['programas_unicos']}")
        texto.append(f"Total de cursos: {self.mapeamento['total_cursos']:,}")
        texto.append(f"Total de ofertas: {self.mapeamento['total_ofertas']:,}")
        texto.append("")

        # Top 10 programas por cursos
        texto.append("🏆 TOP 10 PROGRAMAS POR QUANTIDADE DE CURSOS:")
        for i, (programa, quantidade) in enumerate(
            list(self.mapeamento["programas_ordenados_por_cursos"].items())[:10], 1
        ):
            texto.append(f"  {i:2d}. {programa}: {quantidade:,} cursos")

        texto.append("")

        # Top 10 programas por ofertas
        texto.append("🎯 TOP 10 PROGRAMAS POR QUANTIDADE DE OFERTAS:")
        for i, (programa, quantidade) in enumerate(
            list(self.mapeamento["programas_ordenados_por_ofertas"].items())[:10], 1
        ):
            texto.append(f"  {i:2d}. {programa}: {quantidade:,} ofertas")

        texto.append("")

        # Top 10 programas por vagas
        texto.append("💺 TOP 10 PROGRAMAS POR QUANTIDADE DE VAGAS:")
        for i, (programa, quantidade) in enumerate(
            list(self.mapeamento["vagas_por_programa"].items())[:10], 1
        ):
            texto.append(f"  {i:2d}. {programa}: {quantidade:,} vagas")

        return "\n".join(texto)

    def obter_programa_detalhado(self, nome_programa: str) -> Dict[str, Any]:
        """
        Obtém detalhes de um programa específico.

        Args:
            nome_programa: Nome do programa

        Returns:
            Dicionário com detalhes do programa
        """
        if (
            not self.mapeamento
            or nome_programa not in self.mapeamento["programas_encontrados"]
        ):
            return {}

        return self.mapeamento["programas_encontrados"][nome_programa]


def main():
    """Função principal para teste."""
    from analisador_geral import AnalisadorGeral

    analisador = AnalisadorGeral()
    if analisador.carregar_dados():
        mapeador = MapeamentoProgramas()
        mapeador.carregar_dados(analisador.dados)
        mapeamento = mapeador.mapear_programas()

        print("\n" + mapeador.gerar_resumo_programas())


if __name__ == "__main__":
    main()
