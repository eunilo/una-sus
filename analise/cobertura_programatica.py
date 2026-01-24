#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Cobertura Programática - Sistema de Análise UNA-SUS
===================================================

Módulo para análise de cobertura programática.
"""

from datetime import datetime
from typing import Any, Dict, List

import pandas as pd


class CoberturaProgramatica:
    """
    Análise de cobertura programática.
    """

    def __init__(self, dados: pd.DataFrame = None):
        """
        Inicializa a análise de cobertura programática.

        Args:
            dados: DataFrame com os dados
        """
        self.dados = dados
        self.cobertura = {}

    def carregar_dados(self, dados: pd.DataFrame):
        """Carrega dados para análise."""
        self.dados = dados

    def analisar_cobertura(self) -> Dict[str, Any]:
        """
        Analisa a cobertura programática.

        Returns:
            Dicionário com análise de cobertura
        """
        if self.dados is None:
            return {}

        print("📊 Analisando cobertura programática...")

        # Identificar coluna de programas
        coluna_programas = None
        for col in self.dados.columns:
            if "programa" in col.lower() or "programas" in col.lower():
                coluna_programas = col
                break

        if coluna_programas is None:
            print("⚠️ Coluna de programas não encontrada!")
            return {}

        # Análise de cobertura
        cobertura = {
            "total_registros": len(self.dados),
            "coluna_programas": coluna_programas,
            "programas_com_cobertura": 0,
            "programas_sem_cobertura": 0,
            "cursos_sem_cobertura_total": 0,
            "cursos_sem_cobertura": [],
            "cobertura_por_programa": {},
            "lacunas_programaticas": [],
            "concentracao_programatica": {},
            "distribuicao_geografica": {},
            "timestamp_analise": datetime.now().isoformat(),
        }

        # Identificar cursos sem cobertura (programa vazio/nulo)
        coluna_curso = "no_curso" if "no_curso" in self.dados.columns else None
        coluna_id_curso = (
            "co_seq_curso" if "co_seq_curso" in self.dados.columns else None
        )
        coluna_instituicao = "no_orgao" if "no_orgao" in self.dados.columns else None

        sem_programa = self.dados[self.dados[coluna_programas].isna() | (self.dados[coluna_programas] == "")]
        if not sem_programa.empty:
            # Consolidar por curso para evitar duplicidade de ofertas
            colunas_unicas = [c for c in [coluna_id_curso, coluna_curso, coluna_instituicao] if c]
            cursos_sem = sem_programa[colunas_unicas].drop_duplicates()
            cobertura["cursos_sem_cobertura_total"] = len(cursos_sem)
            cobertura["cursos_sem_cobertura"] = cursos_sem.to_dict("records")

        # Contar programas únicos
        programas_unicos = self.dados[coluna_programas].dropna().unique()

        # Analisar cobertura de cada programa
        for programa in programas_unicos:
            if pd.isna(programa) or programa == "":
                continue

            # Filtrar dados do programa
            dados_programa = self.dados[self.dados[coluna_programas] == programa]

            # Análise de cobertura do programa
            cobertura_programa = {
                "quantidade_cursos": len(dados_programa),
                "quantidade_ofertas": len(dados_programa),
                "cobertura_geografica": {},
                "cobertura_institucional": {},
                "cobertura_tematica": {},
                "cobertura_nivel": {},
                "cobertura_modalidade": {},
            }

            # Cobertura geográfica
            if "no_orgao" in dados_programa.columns:
                instituicoes = dados_programa["no_orgao"].value_counts()
                cobertura_programa["cobertura_institucional"] = instituicoes.to_dict()
                cobertura_programa["total_instituicoes"] = len(instituicoes)

            # Cobertura temática
            if "area_tematica" in dados_programa.columns:
                areas = dados_programa["area_tematica"].value_counts()
                cobertura_programa["cobertura_tematica"] = areas.to_dict()
                cobertura_programa["total_areas"] = len(areas)

            # Cobertura por nível
            if "no_nivel" in dados_programa.columns:
                niveis = dados_programa["no_nivel"].value_counts()
                cobertura_programa["cobertura_nivel"] = niveis.to_dict()
                cobertura_programa["total_niveis"] = len(niveis)

            # Cobertura por modalidade
            if "no_formato" in dados_programa.columns:
                modalidades = dados_programa["no_formato"].value_counts()
                cobertura_programa["cobertura_modalidade"] = modalidades.to_dict()
                cobertura_programa["total_modalidades"] = len(modalidades)

            # Calcular vagas
            if "vagas" in dados_programa.columns:
                vagas_numericas = pd.to_numeric(
                    dados_programa["vagas"], errors="coerce"
                )
                cobertura_programa["total_vagas"] = vagas_numericas.sum()
                cobertura_programa["media_vagas"] = vagas_numericas.mean()
            else:
                cobertura_programa["total_vagas"] = 0
                cobertura_programa["media_vagas"] = 0

            # Classificar cobertura
            if cobertura_programa["quantidade_cursos"] > 0:
                cobertura["programas_com_cobertura"] += 1
            else:
                cobertura["programas_sem_cobertura"] += 1

            # ANÁLISE SIMPLIFICADA - FOCADA APENAS NA QUANTIDADE DE CURSOS
            # Critério único: Programas com poucos cursos (menos de 10)
            if cobertura_programa["quantidade_cursos"] < 10:
                cobertura["lacunas_programaticas"].append(
                    {
                        "programa": programa,
                        "quantidade_cursos": cobertura_programa["quantidade_cursos"],
                        "categoria": (
                            "Poucos cursos"
                            if cobertura_programa["quantidade_cursos"] < 5
                            else "Cursos limitados"
                        ),
                    }
                )

            cobertura["cobertura_por_programa"][programa] = cobertura_programa

        # Análise de concentração
        cobertura["concentracao_programatica"] = {
            "programas_com_mais_cursos": dict(
                sorted(
                    [
                        (p, cobertura["cobertura_por_programa"][p]["quantidade_cursos"])
                        for p in cobertura["cobertura_por_programa"]
                    ],
                    key=lambda x: x[1],
                    reverse=True,
                )[:10]
            ),
            "programas_com_mais_ofertas": dict(
                sorted(
                    [
                        (
                            p,
                            cobertura["cobertura_por_programa"][p][
                                "quantidade_ofertas"
                            ],
                        )
                        for p in cobertura["cobertura_por_programa"]
                    ],
                    key=lambda x: x[1],
                    reverse=True,
                )[:10]
            ),
            "programas_com_mais_vagas": dict(
                sorted(
                    [
                        (p, cobertura["cobertura_por_programa"][p]["total_vagas"])
                        for p in cobertura["cobertura_por_programa"]
                    ],
                    key=lambda x: x[1],
                    reverse=True,
                )[:10]
            ),
        }

        self.cobertura = cobertura
        print(
            f"✅ Análise de cobertura concluída: {cobertura['programas_com_cobertura']} cursos com cobertura"
        )

        return cobertura

    def gerar_resumo_cobertura(self) -> str:
        """
        Gera resumo textual da cobertura.

        Returns:
            String com resumo formatado
        """
        if not self.cobertura:
            return "❌ Nenhuma análise de cobertura disponível!"

        texto = []
        texto.append("📊 ANÁLISE DE COBERTURA PROGRAMÁTICA")
        texto.append("=" * 50)
        texto.append(
            f"Total de programas: {self.cobertura['programas_com_cobertura'] + self.cobertura['programas_sem_cobertura']}"
        )
        texto.append(
            f"Cursos com cobertura: {self.cobertura['programas_com_cobertura']}"
        )
        texto.append(
            f"Programas sem cobertura: {self.cobertura['programas_sem_cobertura']}"
        )
        texto.append("")

        # Programas com mais cursos
        texto.append("🏆 PROGRAMAS COM MAIOR COBERTURA (CURSOS):")
        for i, (programa, quantidade) in enumerate(
            list(
                self.cobertura["concentracao_programatica"][
                    "programas_com_mais_cursos"
                ].items()
            )[:10],
            1,
        ):
            texto.append(f"  {i:2d}. {programa}: {quantidade:,} registros")

        texto.append("")

        # Todos os programas com seus registros detalhados
        if self.cobertura["lacunas_programaticas"]:
            texto.append("📋 TODOS OS PROGRAMAS E SEUS REGISTROS DETALHADOS:")
            texto.append("")

            # Ordenar por quantidade de registros (menor para maior)
            programas_ordenados = sorted(
                self.cobertura["lacunas_programaticas"],
                key=lambda x: x["quantidade_cursos"],
            )

            for lacuna in programas_ordenados:
                programa = lacuna["programa"]
                registros = lacuna["quantidade_cursos"]

                # Definir ícone baseado na quantidade
                if registros < 5:
                    icone = "🔴"
                elif registros < 10:
                    icone = "🟡"
                elif registros < 50:
                    icone = "🟢"
                else:
                    icone = "🏆"

                # Cabeçalho do programa
                texto.append(f"{icone} {programa}")
                texto.append(f"   📊 Total de registros: {registros}")
                texto.append("   📋 Registros individuais:")

                # Buscar registros específicos deste programa
                dados_programa = self.dados[self.dados["programas_governo"] == programa]

                for idx, (_, registro) in enumerate(dados_programa.iterrows(), 1):
                    curso = registro.get("no_curso", "N/A")
                    instituicao = registro.get("no_orgao", "N/A")
                    modalidade = registro.get("no_modalidade", "N/A")
                    vagas = registro.get("vagas", "N/A")

                    # Truncar textos longos
                    curso_short = curso[:50] + "..." if len(str(curso)) > 50 else curso
                    instituicao_short = (
                        instituicao[:30] + "..."
                        if len(str(instituicao)) > 30
                        else instituicao
                    )

                    texto.append(f"      {idx:2d}. {curso_short}")
                    texto.append(f"          🏢 {instituicao_short}")
                    texto.append(f"          📚 {modalidade} | 🎯 {vagas} vagas")

                texto.append("")

        return "\n".join(texto)

    def obter_cobertura_programa(self, nome_programa: str) -> Dict[str, Any]:
        """
        Obtém cobertura detalhada de um programa específico.

        Args:
            nome_programa: Nome do programa

        Returns:
            Dicionário com cobertura do programa
        """
        if (
            not self.cobertura
            or nome_programa not in self.cobertura["cobertura_por_programa"]
        ):
            return {}

        return self.cobertura["cobertura_por_programa"][nome_programa]


def main():
    """Função principal para teste."""
    import os
    import sys

    sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

    from analise.analisador_geral import AnalisadorGeral

    analisador = AnalisadorGeral()
    if analisador.carregar_dados():
        cobertura = CoberturaProgramatica()
        cobertura.carregar_dados(analisador.dados)
        analise = cobertura.analisar_cobertura()

        print("\n" + cobertura.gerar_resumo_cobertura())


if __name__ == "__main__":
    main()
