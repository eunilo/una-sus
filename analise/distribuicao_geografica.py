#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Distribuição Geográfica - Sistema de Análise UNA-SUS
====================================================

Módulo para análise de distribuição geográfica de programas.
"""

import re
from datetime import datetime
from typing import Any, Dict, List

import pandas as pd


class DistribuicaoGeografica:
    """
    Análise de distribuição geográfica de programas.
    """

    def __init__(self, dados: pd.DataFrame = None):
        """
        Inicializa a análise de distribuição geográfica.

        Args:
            dados: DataFrame com os dados
        """
        self.dados = dados
        self.distribuicao = {}

    def carregar_dados(self, dados: pd.DataFrame):
        """Carrega dados para análise."""
        self.dados = dados

    def extrair_estado(self, texto: str) -> str:
        """
        Extrai estado de um texto.

        Args:
            texto: Texto contendo informações de localização

        Returns:
            Sigla do estado ou "Não identificado"
        """
        if pd.isna(texto) or texto == "":
            return "Não identificado"

        texto = str(texto).upper()

        # Mapeamento de estados
        estados = {
            "AC": ["ACRE", "AC"],
            "AL": ["ALAGOAS", "AL"],
            "AP": ["AMAPA", "AP"],
            "AM": ["AMAZONAS", "AM"],
            "BA": ["BAHIA", "BA"],
            "CE": ["CEARA", "CE"],
            "DF": ["DISTRITO FEDERAL", "DF", "BRASILIA"],
            "ES": ["ESPIRITO SANTO", "ES"],
            "GO": ["GOIAS", "GO"],
            "MA": ["MARANHAO", "MA"],
            "MT": ["MATO GROSSO", "MT"],
            "MS": ["MATO GROSSO DO SUL", "MS"],
            "MG": ["MINAS GERAIS", "MG"],
            "PA": ["PARA", "PA"],
            "PB": ["PARAIBA", "PB"],
            "PR": ["PARANA", "PR"],
            "PE": ["PERNAMBUCO", "PE"],
            "PI": ["PIAUI", "PI"],
            "RJ": ["RIO DE JANEIRO", "RJ"],
            "RN": ["RIO GRANDE DO NORTE", "RN"],
            "RS": ["RIO GRANDE DO SUL", "RS"],
            "RO": ["RONDONIA", "RO"],
            "RR": ["RORAIMA", "RR"],
            "SC": ["SANTA CATARINA", "SC"],
            "SP": ["SAO PAULO", "SP"],
            "SE": ["SERGIPE", "SE"],
            "TO": ["TOCANTINS", "TO"],
        }

        for sigla, variacoes in estados.items():
            for variacao in variacoes:
                if variacao in texto:
                    return sigla

        return "Não identificado"

    def analisar_distribuicao(self) -> Dict[str, Any]:
        """
        Analisa a distribuição geográfica.

        Returns:
            Dicionário com análise de distribuição
        """
        if self.dados is None:
            return {}

        print("📊 Analisando distribuição geográfica...")

        # Identificar coluna de programas
        coluna_programas = None
        for col in self.dados.columns:
            if "programa" in col.lower() or "programas" in col.lower():
                coluna_programas = col
                break

        if coluna_programas is None:
            print("⚠️ Coluna de programas não encontrada!")
            return {}

        # Análise de distribuição
        distribuicao = {
            "total_registros": len(self.dados),
            "coluna_programas": coluna_programas,
            "estados_identificados": 0,
            "estados_sem_identificacao": 0,
            "distribuicao_por_estado": {},
            "distribuicao_por_regiao": {},
            "programas_por_estado": {},
            "programas_por_regiao": {},
            "polos_educacionais": {},
            "desertos_educacionais": [],
            "timestamp_analise": datetime.now().isoformat(),
        }

        # Mapeamento de regiões
        regioes = {
            "NORTE": ["AC", "AP", "AM", "PA", "RO", "RR", "TO"],
            "NORDESTE": ["AL", "BA", "CE", "MA", "PB", "PE", "PI", "RN", "SE"],
            "CENTRO-OESTE": ["DF", "GO", "MT", "MS"],
            "SUDESTE": ["ES", "MG", "RJ", "SP"],
            "SUL": ["PR", "RS", "SC"],
        }

        # Contar programas únicos
        programas_unicos = self.dados[coluna_programas].dropna().unique()

        # Inicializar contadores
        for estado in [
            "AC",
            "AL",
            "AP",
            "AM",
            "BA",
            "CE",
            "DF",
            "ES",
            "GO",
            "MA",
            "MT",
            "MS",
            "MG",
            "PA",
            "PB",
            "PR",
            "PE",
            "PI",
            "RJ",
            "RN",
            "RS",
            "RO",
            "RR",
            "SC",
            "SP",
            "SE",
            "TO",
        ]:
            distribuicao["distribuicao_por_estado"][estado] = {
                "cursos": 0,
                "ofertas": 0,
                "vagas": 0,
                "instituicoes": set(),
                "programas": set(),
                "cursos_unicos": set(),
            }

        for regiao in regioes.keys():
            distribuicao["distribuicao_por_regiao"][regiao] = {
                "cursos": 0,
                "ofertas": 0,
                "vagas": 0,
                "estados": regioes[regiao],
                "instituicoes": set(),
                "programas": set(),
                "cursos_unicos": set(),  # Para contar cursos únicos
            }

        # Analisar cada registro
        for _, registro in self.dados.iterrows():
            programa = registro.get(coluna_programas, "")

            # Extrair estado da instituição
            estado = "Não identificado"
            if "no_orgao" in registro:
                estado = self.extrair_estado(registro["no_orgao"])

            # Contar por estado
            if estado in distribuicao["distribuicao_por_estado"]:
                distribuicao["distribuicao_por_estado"][estado]["cursos"] += 1
                distribuicao["distribuicao_por_estado"][estado]["ofertas"] += 1

                # Adicionar curso único
                if "no_curso" in registro:
                    distribuicao["distribuicao_por_estado"][estado][
                        "cursos_unicos"
                    ].add(registro["no_curso"])

                if "no_orgao" in registro:
                    distribuicao["distribuicao_por_estado"][estado]["instituicoes"].add(
                        registro["no_orgao"]
                    )

                if programa:
                    distribuicao["distribuicao_por_estado"][estado]["programas"].add(
                        programa
                    )

                # Calcular vagas
                if "vagas" in registro:
                    vagas = pd.to_numeric(registro["vagas"], errors="coerce")
                    if not pd.isna(vagas):
                        distribuicao["distribuicao_por_estado"][estado][
                            "vagas"
                        ] += vagas

                # Contar por região
                for regiao, estados_regiao in regioes.items():
                    if estado in estados_regiao:
                        distribuicao["distribuicao_por_regiao"][regiao]["cursos"] += 1
                        distribuicao["distribuicao_por_regiao"][regiao]["ofertas"] += 1

                        # Adicionar curso único
                        if "no_curso" in registro:
                            distribuicao["distribuicao_por_regiao"][regiao][
                                "cursos_unicos"
                            ].add(registro["no_curso"])

                        if "no_orgao" in registro:
                            distribuicao["distribuicao_por_regiao"][regiao][
                                "instituicoes"
                            ].add(registro["no_orgao"])

                        if programa:
                            distribuicao["distribuicao_por_regiao"][regiao][
                                "programas"
                            ].add(programa)

                        if "vagas" in registro:
                            vagas = pd.to_numeric(registro["vagas"], errors="coerce")
                            if not pd.isna(vagas):
                                distribuicao["distribuicao_por_regiao"][regiao][
                                    "vagas"
                                ] += vagas
                        break
            else:
                distribuicao["estados_sem_identificacao"] += 1

        # Converter sets para listas para serialização
        for estado in distribuicao["distribuicao_por_estado"]:
            distribuicao["distribuicao_por_estado"][estado]["instituicoes"] = list(
                distribuicao["distribuicao_por_estado"][estado]["instituicoes"]
            )
            distribuicao["distribuicao_por_estado"][estado]["programas"] = list(
                distribuicao["distribuicao_por_estado"][estado]["programas"]
            )
            distribuicao["distribuicao_por_estado"][estado]["cursos_unicos"] = list(
                distribuicao["distribuicao_por_estado"][estado]["cursos_unicos"]
            )
            distribuicao["distribuicao_por_estado"][estado]["total_instituicoes"] = len(
                distribuicao["distribuicao_por_estado"][estado]["instituicoes"]
            )
            distribuicao["distribuicao_por_estado"][estado]["total_programas"] = len(
                distribuicao["distribuicao_por_estado"][estado]["programas"]
            )
            distribuicao["distribuicao_por_estado"][estado]["total_cursos_unicos"] = (
                len(distribuicao["distribuicao_por_estado"][estado]["cursos_unicos"])
            )

        for regiao in distribuicao["distribuicao_por_regiao"]:
            distribuicao["distribuicao_por_regiao"][regiao]["instituicoes"] = list(
                distribuicao["distribuicao_por_regiao"][regiao]["instituicoes"]
            )
            distribuicao["distribuicao_por_regiao"][regiao]["programas"] = list(
                distribuicao["distribuicao_por_regiao"][regiao]["programas"]
            )
            distribuicao["distribuicao_por_regiao"][regiao]["cursos_unicos"] = list(
                distribuicao["distribuicao_por_regiao"][regiao]["cursos_unicos"]
            )
            distribuicao["distribuicao_por_regiao"][regiao]["total_instituicoes"] = len(
                distribuicao["distribuicao_por_regiao"][regiao]["instituicoes"]
            )
            distribuicao["distribuicao_por_regiao"][regiao]["total_programas"] = len(
                distribuicao["distribuicao_por_regiao"][regiao]["programas"]
            )
            distribuicao["distribuicao_por_regiao"][regiao]["total_cursos_unicos"] = (
                len(distribuicao["distribuicao_por_regiao"][regiao]["cursos_unicos"])
            )

        # Identificar polos educacionais (estados com mais de 100 cursos)
        for estado, dados in distribuicao["distribuicao_por_estado"].items():
            if dados["cursos"] > 100:
                distribuicao["polos_educacionais"][estado] = {
                    "cursos": dados["cursos"],
                    "cursos_unicos": dados["total_cursos_unicos"],
                    "instituicoes": dados["total_instituicoes"],
                    "programas": dados["total_programas"],
                }

        # Identificar desertos educacionais (estados com menos de 10 cursos)
        for estado, dados in distribuicao["distribuicao_por_estado"].items():
            if dados["cursos"] < 10:
                distribuicao["desertos_educacionais"].append(
                    {
                        "estado": estado,
                        "cursos": dados["cursos"],
                        "cursos_unicos": dados["total_cursos_unicos"],
                        "instituicoes": dados["total_instituicoes"],
                        "programas": dados["total_programas"],
                    }
                )

        # Estatísticas gerais
        estados_com_dados = sum(
            1
            for dados in distribuicao["distribuicao_por_estado"].values()
            if dados["cursos"] > 0
        )
        distribuicao["estados_identificados"] = estados_com_dados

        self.distribuicao = distribuicao
        print(
            f"✅ Análise de distribuição concluída: {estados_com_dados} estados com dados"
        )

        return distribuicao

    def gerar_resumo_distribuicao(self) -> str:
        """
        Gera resumo textual da distribuição.

        Returns:
            String com resumo formatado
        """
        if not self.distribuicao:
            return "❌ Nenhuma análise de distribuição disponível!"

        texto = []
        texto.append("📊 DISTRIBUIÇÃO GEOGRÁFICA DE PROGRAMAS")
        texto.append("=" * 50)
        texto.append(f"Estados com dados: {self.distribuicao['estados_identificados']}")
        texto.append(
            f"Estados sem identificação: {self.distribuicao['estados_sem_identificacao']}"
        )
        texto.append("")

        # Distribuição por região
        texto.append("🗺️ DISTRIBUIÇÃO POR REGIÃO:")
        for regiao, dados in self.distribuicao["distribuicao_por_regiao"].items():
            texto.append(
                f"  {regiao}: {dados['cursos']:,} cursos, {dados['total_instituicoes']} instituições"
            )

        texto.append("")

        # Polos educacionais
        if self.distribuicao["polos_educacionais"]:
            texto.append("🏆 POLOS EDUCACIONAIS (mais de 100 cursos):")
            for estado, dados in self.distribuicao["polos_educacionais"].items():
                texto.append(
                    f"  • {estado}: {dados['cursos']:,} cursos, {dados['instituicoes']} instituições"
                )

        texto.append("")

        # Desertos educacionais
        if self.distribuicao["desertos_educacionais"]:
            texto.append("⚠️ DESERTOS EDUCACIONAIS (menos de 10 cursos):")
            for deserto in self.distribuicao["desertos_educacionais"]:
                texto.append(
                    f"  • {deserto['estado']}: {deserto['cursos']} cursos, {deserto['instituicoes']} instituições"
                )

        return "\n".join(texto)

    def obter_distribuicao_estado(self, estado: str) -> Dict[str, Any]:
        """
        Obtém distribuição detalhada de um estado específico.

        Args:
            estado: Sigla do estado

        Returns:
            Dicionário com distribuição do estado
        """
        if (
            not self.distribuicao
            or estado not in self.distribuicao["distribuicao_por_estado"]
        ):
            return {}

        return self.distribuicao["distribuicao_por_estado"][estado]


def main():
    """Função principal para teste."""
    from analisador_geral import AnalisadorGeral

    analisador = AnalisadorGeral()
    if analisador.carregar_dados():
        distribuicao = DistribuicaoGeografica()
        distribuicao.carregar_dados(analisador.dados)
        analise = distribuicao.analisar_distribuicao()

        print("\n" + distribuicao.gerar_resumo_distribuicao())


if __name__ == "__main__":
    main()
