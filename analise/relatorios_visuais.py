#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Relatórios Visuais - Sistema de Análise UNA-SUS
===============================================

Módulo para geração de relatórios visuais com formatação clara e gráficos ASCII.
"""

import json
import os
from datetime import datetime
from typing import Any, Dict, List

import pandas as pd


class RelatoriosVisuais:
    """
    Geração de relatórios visuais para análise de programas de governo.
    """

    def __init__(self, dados: pd.DataFrame = None):
        """Inicializa o gerador de relatórios visuais."""
        self.criar_diretorio_relatorios()
        self.dados = dados

    def criar_diretorio_relatorios(self):
        """Cria diretório de relatórios se não existir."""
        if not os.path.exists("relatorios"):
            os.makedirs("relatorios")

    def gerar_cabecalho(self, titulo: str) -> str:
        """
        Gera cabeçalho formatado para relatórios.

        Args:
            titulo: Título do relatório

        Returns:
            String com cabeçalho formatado
        """
        linha = "=" * 80
        data_hora = datetime.now().strftime("%d/%m/%Y às %H:%M:%S")

        return f"""
{linha}
🏥 UNA-SUS - SISTEMA DE ANÁLISE DE PROGRAMAS DE GOVERNO
{linha}
📋 {titulo.upper()}
📅 Gerado em: {data_hora}
{linha}
"""

    def gerar_rodape(self) -> str:
        """
        Gera rodapé formatado para relatórios.

        Returns:
            String com rodapé formatado
        """
        return f"""
{'=' * 80}
📊 Sistema de Análise UNA-SUS - Relatório Gerado Automaticamente
{'=' * 80}
"""

    def criar_barra_progresso(self, valor: int, maximo: int, largura: int = 50) -> str:
        """
        Cria barra de progresso ASCII.

        Args:
            valor: Valor atual
            maximo: Valor máximo
            largura: Largura da barra

        Returns:
            String com barra de progresso
        """
        if maximo == 0:
            return "█" * largura

        percentual = valor / maximo
        barras = int(percentual * largura)

        barra = "█" * barras + "░" * (largura - barras)
        return f"[{barra}] {percentual:.1%}"

    def criar_grafico_barras(
        self, dados: Dict[str, int], titulo: str, max_barras: int = 10
    ) -> str:
        """
        Cria gráfico de barras ASCII.

        Args:
            dados: Dicionário com dados
            titulo: Título do gráfico
            max_barras: Máximo de barras a mostrar

        Returns:
            String com gráfico de barras
        """
        if not dados:
            return f"📊 {titulo}\n   Nenhum dado disponível\n"

        # Ordenar por valor e pegar os top
        dados_ordenados = sorted(dados.items(), key=lambda x: x[1], reverse=True)[
            :max_barras
        ]
        max_valor = max(dados.values()) if dados.values() else 1

        resultado = [f"📊 {titulo}"]
        resultado.append("-" * 60)

        for nome, valor in dados_ordenados:
            barra = self.criar_barra_progresso(valor, max_valor, 30)
            resultado.append(f"{nome[:25]:<25} {barra} {valor:,}")

        return "\n".join(resultado)

    def gerar_relatorio_mapeamento(self, mapeamento: Dict[str, Any]) -> str:
        """
        Gera relatório visual do mapeamento de programas.

        Args:
            mapeamento: Dados do mapeamento

        Returns:
            String com relatório formatado
        """
        if not mapeamento:
            return "❌ Nenhum dado de mapeamento disponível!"

        relatorio = []
        relatorio.append(self.gerar_cabecalho("Mapeamento de Programas de Governo"))

        # Resumo geral
        relatorio.append("📈 RESUMO GERAL")
        relatorio.append("-" * 40)
        relatorio.append(
            f"🎯 Total de Programas: {mapeamento.get('programas_unicos', 0):,}"
        )
        relatorio.append(f"📚 Total de Cursos: {mapeamento.get('total_cursos', 0):,}")
        relatorio.append(f"🎓 Total de Ofertas: {mapeamento.get('total_ofertas', 0):,}")
        relatorio.append("")

        # Top programas por cursos
        if "programas_ordenados_por_cursos" in mapeamento:
            relatorio.append("🏆 TOP 10 PROGRAMAS POR QUANTIDADE DE CURSOS")
            relatorio.append("-" * 50)
            for i, (programa, quantidade) in enumerate(
                list(mapeamento["programas_ordenados_por_cursos"].items())[:10], 1
            ):
                barra = self.criar_barra_progresso(
                    quantidade, mapeamento["total_cursos"], 30
                )
                relatorio.append(f"{i:2d}. {programa[:35]:<35} {barra} {quantidade:,}")
            relatorio.append("")

        # Top programas por ofertas
        if "programas_ordenados_por_ofertas" in mapeamento:
            relatorio.append("🎯 TOP 10 PROGRAMAS POR QUANTIDADE DE OFERTAS")
            relatorio.append("-" * 50)
            for i, (programa, quantidade) in enumerate(
                list(mapeamento["programas_ordenados_por_ofertas"].items())[:10], 1
            ):
                barra = self.criar_barra_progresso(
                    quantidade, mapeamento["total_ofertas"], 30
                )
                relatorio.append(f"{i:2d}. {programa[:35]:<35} {barra} {quantidade:,}")
            relatorio.append("")

        # Top programas por vagas
        if "programas_ordenados_por_vagas" in mapeamento:
            relatorio.append("💺 TOP 10 PROGRAMAS POR QUANTIDADE DE VAGAS")
            relatorio.append("-" * 50)
            for i, (programa, quantidade) in enumerate(
                list(mapeamento["vagas_por_programa"].items())[:10], 1
            ):
                max_vagas = (
                    max(mapeamento["vagas_por_programa"].values())
                    if mapeamento["vagas_por_programa"].values()
                    else 1
                )
                barra = self.criar_barra_progresso(quantidade, max_vagas, 30)
                relatorio.append(f"{i:2d}. {programa[:35]:<35} {barra} {quantidade:,}")

        relatorio.append(self.gerar_rodape())
        return "\n".join(relatorio)

    def gerar_relatorio_cobertura(self, cobertura: Dict[str, Any]) -> str:
        """
        Gera relatório visual da cobertura programática.

        Args:
            cobertura: Dados da cobertura

        Returns:
            String com relatório formatado
        """
        if not cobertura:
            return "❌ Nenhum dado de cobertura disponível!"

        relatorio = []
        relatorio.append(self.gerar_cabecalho("Análise de Cobertura Programática"))

        # Resumo geral
        relatorio.append("📈 RESUMO DA COBERTURA")
        relatorio.append("-" * 40)
        relatorio.append(
            f"✅ Programas com Cobertura: {cobertura.get('programas_com_cobertura', 0):,}"
        )
        relatorio.append(
            f"❌ Programas sem Cobertura: {cobertura.get('programas_sem_cobertura', 0):,}"
        )
        relatorio.append(
            f"📊 Total de Registros: {cobertura.get('total_registros', 0):,}"
        )
        relatorio.append("")

        # Concentração programática
        if "concentracao_programatica" in cobertura:
            concentracao = cobertura["concentracao_programatica"]

            if "programas_com_mais_cursos" in concentracao:
                relatorio.append("🏆 CONCENTRAÇÃO POR REGISTROS")
                relatorio.append("-" * 50)
                for i, (programa, quantidade) in enumerate(
                    list(concentracao["programas_com_mais_cursos"].items())[:10], 1
                ):
                    barra = self.criar_barra_progresso(
                        quantidade, cobertura["total_registros"], 30
                    )
                    relatorio.append(
                        f"{i:2d}. {programa[:35]:<35} {barra} {quantidade:,}"
                    )
                relatorio.append("")

        # Todos os programas com seus registros detalhados
        if "lacunas_programaticas" in cobertura and cobertura["lacunas_programaticas"]:
            relatorio.append("📋 TODOS OS PROGRAMAS E SEUS REGISTROS DETALHADOS:")
            relatorio.append("-" * 50)

            # Ordenar por quantidade de registros (menor para maior)
            programas_ordenados = sorted(
                cobertura["lacunas_programaticas"], key=lambda x: x["quantidade_cursos"]
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
                relatorio.append(f"{icone} {programa}")
                relatorio.append(f"   📊 Total de registros: {registros}")
                relatorio.append("   📋 Registros individuais:")

                # Buscar registros específicos deste programa
                # Para o relatório visual, vamos mostrar apenas os primeiros 3 registros
                # para não ficar muito extenso
                dados_programa = self.dados[self.dados["programas_governo"] == programa]

                for idx, (_, registro) in enumerate(
                    dados_programa.head(3).iterrows(), 1
                ):
                    curso = registro.get("no_curso", "N/A")
                    instituicao = registro.get("no_orgao", "N/A")
                    modalidade = registro.get("no_modalidade", "N/A")
                    vagas = registro.get("vagas", "N/A")

                    # Truncar textos longos
                    curso_short = curso[:40] + "..." if len(str(curso)) > 40 else curso
                    instituicao_short = (
                        instituicao[:25] + "..."
                        if len(str(instituicao)) > 25
                        else instituicao
                    )

                    relatorio.append(f"      {idx}. {curso_short}")
                    relatorio.append(f"          🏢 {instituicao_short}")
                    relatorio.append(f"          📚 {modalidade} | 🎯 {vagas} vagas")

                if len(dados_programa) > 3:
                    relatorio.append(
                        f"      ... e mais {len(dados_programa) - 3} registros"
                    )

                relatorio.append("")

            relatorio.append("")

        relatorio.append(self.gerar_rodape())
        return "\n".join(relatorio)

    def gerar_relatorio_distribuicao(self, distribuicao: Dict[str, Any]) -> str:
        """
        Gera relatório visual da distribuição geográfica.

        Args:
            distribuicao: Dados da distribuição

        Returns:
            String com relatório formatado
        """
        if not distribuicao:
            return "❌ Nenhum dado de distribuição disponível!"

        relatorio = []
        relatorio.append(self.gerar_cabecalho("Distribuição Geográfica de Programas"))

        # Resumo geral
        relatorio.append("🗺️ RESUMO GEOGRÁFICO")
        relatorio.append("-" * 40)
        relatorio.append(
            f"📍 Estados com Dados: {distribuicao.get('estados_identificados', 0)}"
        )
        relatorio.append(
            f"❓ Estados sem Identificação: {distribuicao.get('estados_sem_identificacao', 0)}"
        )
        relatorio.append(
            f"🏆 Polos Educacionais: {len(distribuicao.get('polos_educacionais', {}))}"
        )
        relatorio.append(
            f"⚠️ Desertos Educacionais: {len(distribuicao.get('desertos_educacionais', []))}"
        )
        relatorio.append("")

        # Distribuição por região
        if "distribuicao_por_regiao" in distribuicao:
            relatorio.append("🌍 DISTRIBUIÇÃO POR REGIÃO")
            relatorio.append("-" * 70)
            for regiao, dados in distribuicao["distribuicao_por_regiao"].items():
                ofertas = dados.get("cursos", 0)  # Total de ofertas
                cursos_unicos = dados.get("total_cursos_unicos", 0)  # Cursos únicos
                instituicoes = dados.get("total_instituicoes", 0)
                programas = dados.get("total_programas", 0)
                barra = self.criar_barra_progresso(
                    ofertas, distribuicao["total_registros"], 30
                )
                relatorio.append(
                    f"{regiao:<20} {barra} {ofertas:,} ofertas ({cursos_unicos} cursos), {instituicoes} instituições, {programas} programas"
                )
            relatorio.append("")

        # Polos educacionais
        if "polos_educacionais" in distribuicao and distribuicao["polos_educacionais"]:
            relatorio.append("🏆 POLOS EDUCACIONAIS (mais de 100 ofertas)")
            relatorio.append("-" * 60)
            for estado, dados in distribuicao["polos_educacionais"].items():
                ofertas = dados["cursos"]
                cursos_unicos = dados.get("cursos_unicos", 0)
                instituicoes = dados["instituicoes"]
                programas = dados["programas"]
                barra = self.criar_barra_progresso(
                    ofertas, distribuicao["total_registros"], 30
                )
                relatorio.append(
                    f"{estado:<5} {barra} {ofertas:,} ofertas ({cursos_unicos} cursos), {instituicoes} instituições, {programas} programas"
                )
            relatorio.append("")

        # Desertos educacionais
        if (
            "desertos_educacionais" in distribuicao
            and distribuicao["desertos_educacionais"]
        ):
            relatorio.append("⚠️ DESERTOS EDUCACIONAIS (menos de 10 ofertas)")
            relatorio.append("-" * 60)
            for deserto in distribuicao["desertos_educacionais"][:15]:
                estado = deserto["estado"]
                ofertas = deserto["cursos"]
                cursos_unicos = deserto.get("cursos_unicos", 0)
                instituicoes = deserto["instituicoes"]
                programas = deserto["programas"]
                relatorio.append(
                    f"{estado:<5} {ofertas:>3} ofertas ({cursos_unicos} cursos), {instituicoes:>2} instituições, {programas:>2} programas"
                )

        relatorio.append(self.gerar_rodape())
        return "\n".join(relatorio)

    def gerar_relatorio_cobertura_executivo(self, cobertura: Dict[str, Any]) -> str:
        """
        Gera relatório executivo da cobertura programática (resumido).

        Args:
            cobertura: Dados da cobertura

        Returns:
            String com relatório executivo formatado
        """
        if not cobertura:
            return "❌ Nenhum dado de cobertura disponível!"

        relatorio = []
        relatorio.append(
            self.gerar_cabecalho("RELATÓRIO EXECUTIVO - Cobertura Programática")
        )

        # Resumo geral
        relatorio.append("📈 RESUMO EXECUTIVO")
        relatorio.append("=" * 50)
        relatorio.append(
            f"✅ Programas com Cobertura: {cobertura.get('programas_com_cobertura', 0):,}"
        )
        relatorio.append(
            f"❌ Programas sem Cobertura: {cobertura.get('programas_sem_cobertura', 0):,}"
        )
        relatorio.append(
            f"📊 Total de Registros: {cobertura.get('total_registros', 0):,}"
        )
        relatorio.append("")

        # Top 10 programas por concentração
        if "concentracao_programatica" in cobertura:
            concentracao = cobertura["concentracao_programatica"]

            if "programas_com_mais_cursos" in concentracao:
                relatorio.append("🏆 TOP 10 PROGRAMAS POR CONCENTRAÇÃO")
                relatorio.append("=" * 50)
                for i, (programa, quantidade) in enumerate(
                    list(concentracao["programas_com_mais_cursos"].items())[:10], 1
                ):
                    barra = self.criar_barra_progresso(
                        quantidade, cobertura["total_registros"], 30
                    )
                    relatorio.append(
                        f"{i:2d}. {programa[:45]:<45} {barra} {quantidade:,}"
                    )
                relatorio.append("")

        # Principais lacunas identificadas
        if "lacunas_programaticas" in cobertura and cobertura["lacunas_programaticas"]:
            programas_poucos = [
                p
                for p in cobertura["lacunas_programaticas"]
                if p["quantidade_cursos"] < 10
            ]

            if programas_poucos:
                relatorio.append("⚠️ PRINCIPAIS LACUNAS IDENTIFICADAS")
                relatorio.append("=" * 50)
                for i, lacuna in enumerate(programas_poucos[:10], 1):
                    programa = lacuna["programa"]
                    registros = lacuna["quantidade_cursos"]
                    icone = "🔴" if registros < 5 else "🟡"
                    relatorio.append(f"{i:2d}. {icone} {programa}")
                    relatorio.append(f"     📊 Apenas {registros} registros")
                relatorio.append("")

        relatorio.append(self.gerar_rodape())
        return "\n".join(relatorio)

    def gerar_relatorio_cobertura_completo(self, cobertura: Dict[str, Any]) -> str:
        """
        Gera relatório completo da cobertura programática (todos os dados).

        Args:
            cobertura: Dados da cobertura

        Returns:
            String com relatório completo formatado
        """
        if not cobertura:
            return "❌ Nenhum dado de cobertura disponível!"

        relatorio = []
        relatorio.append(
            self.gerar_cabecalho("RELATÓRIO TÉCNICO COMPLETO - Cobertura Programática")
        )

        # Resumo geral
        relatorio.append("📈 RESUMO GERAL")
        relatorio.append("=" * 50)
        relatorio.append(
            f"✅ Programas com Cobertura: {cobertura.get('programas_com_cobertura', 0):,}"
        )
        relatorio.append(
            f"❌ Programas sem Cobertura: {cobertura.get('programas_sem_cobertura', 0):,}"
        )
        relatorio.append(
            f"📊 Total de Registros: {cobertura.get('total_registros', 0):,}"
        )
        relatorio.append("")

        # Concentração programática completa
        if "concentracao_programatica" in cobertura:
            concentracao = cobertura["concentracao_programatica"]

            if "programas_com_mais_cursos" in concentracao:
                relatorio.append("🏆 CONCENTRAÇÃO COMPLETA POR REGISTROS")
                relatorio.append("=" * 50)
                for i, (programa, quantidade) in enumerate(
                    list(concentracao["programas_com_mais_cursos"].items()), 1
                ):
                    barra = self.criar_barra_progresso(
                        quantidade, cobertura["total_registros"], 30
                    )
                    relatorio.append(f"{i:2d}. {programa:<50} {barra} {quantidade:,}")
                relatorio.append("")

        # Todos os programas com TODOS os registros detalhados
        if "lacunas_programaticas" in cobertura and cobertura["lacunas_programaticas"]:
            relatorio.append("📋 ANÁLISE COMPLETA - TODOS OS PROGRAMAS E REGISTROS")
            relatorio.append("=" * 60)

            # Ordenar por quantidade de registros (menor para maior)
            programas_ordenados = sorted(
                cobertura["lacunas_programaticas"], key=lambda x: x["quantidade_cursos"]
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
                relatorio.append(f"{icone} {programa}")
                relatorio.append(f"   📊 Total de registros: {registros}")
                relatorio.append("   📋 Registros individuais:")

                # Buscar TODOS os registros deste programa
                dados_programa = self.dados[self.dados["programas_governo"] == programa]

                for idx, (_, registro) in enumerate(dados_programa.iterrows(), 1):
                    curso = registro.get("no_curso", "N/A")
                    instituicao = registro.get("no_orgao", "N/A")
                    modalidade = registro.get("no_modalidade", "N/A")
                    vagas = registro.get("vagas", "N/A")

                    # Nomes completos sem truncamento
                    relatorio.append(f"      {idx:2d}. {curso}")
                    relatorio.append(f"          🏢 {instituicao}")
                    relatorio.append(f"          📚 {modalidade} | 🎯 {vagas} vagas")

                relatorio.append("")

        # Metodologia e notas técnicas
        relatorio.append("📋 METODOLOGIA E NOTAS TÉCNICAS")
        relatorio.append("=" * 50)
        relatorio.append("• Dados coletados do portal UNA-SUS")
        relatorio.append("• Análise baseada em registros de ofertas")
        relatorio.append("• Classificação por programas de governo")
        relatorio.append(
            "• Data de geração: " + datetime.now().strftime("%d/%m/%Y %H:%M")
        )
        relatorio.append("")

        relatorio.append(self.gerar_rodape())
        return "\n".join(relatorio)

    def gerar_relatorio_completo(self, relatorio_completo: Dict[str, Any]) -> str:
        """
        Gera relatório visual completo.

        Args:
            relatorio_completo: Relatório completo do analisador

        Returns:
            String com relatório formatado
        """
        relatorio = []
        relatorio.append(self.gerar_cabecalho("Relatório Completo de Análise"))

        # Estatísticas básicas
        if "estatisticas_basicas" in relatorio_completo:
            stats = relatorio_completo["estatisticas_basicas"]
            relatorio.append("📊 ESTATÍSTICAS BÁSICAS")
            relatorio.append("-" * 40)
            relatorio.append(
                f"📈 Total de Registros: {stats.get('total_registros', 0):,}"
            )
            relatorio.append(f"📋 Total de Colunas: {stats.get('total_colunas', 0)}")
            relatorio.append(
                f"💾 Uso de Memória: {stats.get('memoria_uso', 0):,} bytes"
            )
            relatorio.append("")

        # Análise de cursos
        if "analise_cursos" in relatorio_completo:
            cursos = relatorio_completo["analise_cursos"]
            relatorio.append("📚 ANÁLISE DE CURSOS")
            relatorio.append("-" * 40)
            relatorio.append(f"🎓 Total de Cursos: {cursos.get('total_cursos', 0):,}")
            relatorio.append(f"📖 Cursos Únicos: {cursos.get('cursos_unicos', 0):,}")

            if "areas_tematicas" in cursos and cursos["areas_tematicas"]:
                relatorio.append("")
                relatorio.append("🏷️ TOP 5 ÁREAS TEMÁTICAS:")
                for i, (area, quantidade) in enumerate(
                    list(cursos["areas_tematicas"].items())[:5], 1
                ):
                    relatorio.append(f"  {i}. {area}: {quantidade:,}")
            relatorio.append("")

        # Análise de ofertas
        if "analise_ofertas" in relatorio_completo:
            ofertas = relatorio_completo["analise_ofertas"]
            relatorio.append("🎯 ANÁLISE DE OFERTAS")
            relatorio.append("-" * 40)
            relatorio.append(
                f"📝 Total de Ofertas: {ofertas.get('total_ofertas', 0):,}"
            )
            relatorio.append(f"🎯 Ofertas Únicas: {ofertas.get('ofertas_unicas', 0):,}")
            relatorio.append(
                f"💺 Vagas Disponíveis: {ofertas.get('vagas_disponiveis', 0):,}"
            )
            relatorio.append("")

        # Análise de programas de governo
        if "analise_programas" in relatorio_completo:
            programas = relatorio_completo["analise_programas"]
            relatorio.append("🏛️ ANÁLISE DE PROGRAMAS DE GOVERNO")
            relatorio.append("-" * 50)

            if "mapeamento_programas" in programas:
                mapeamento = programas["mapeamento_programas"]
                relatorio.append(
                    f"🎯 Programas Únicos: {mapeamento.get('programas_unicos', 0)}"
                )
                relatorio.append(
                    f"📚 Total de Cursos: {mapeamento.get('total_cursos', 0):,}"
                )
                relatorio.append(
                    f"🎓 Total de Ofertas: {mapeamento.get('total_ofertas', 0):,}"
                )

            if "distribuicao_geografica" in programas:
                distribuicao = programas["distribuicao_geografica"]
                relatorio.append(
                    f"📍 Estados com Dados: {distribuicao.get('estados_identificados', 0)}"
                )
                relatorio.append(
                    f"🏆 Polos Educacionais: {len(distribuicao.get('polos_educacionais', {}))}"
                )
                relatorio.append(
                    f"⚠️ Desertos Educacionais: {len(distribuicao.get('desertos_educacionais', []))}"
                )

        relatorio.append(self.gerar_rodape())
        return "\n".join(relatorio)

    def salvar_relatorio_visual(self, conteudo: str, nome_arquivo: str = None) -> str:
        """
        Salva relatório visual em arquivo.

        Args:
            conteudo: Conteúdo do relatório
            nome_arquivo: Nome do arquivo (opcional)

        Returns:
            Caminho do arquivo salvo
        """
        if nome_arquivo is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            nome_arquivo = f"relatorio_visual_{timestamp}.txt"

        caminho_arquivo = os.path.join("relatorios", nome_arquivo)

        with open(caminho_arquivo, "w", encoding="utf-8") as f:
            f.write(conteudo)

        return caminho_arquivo


def main():
    """Função principal para teste."""
    from analisador_geral import AnalisadorGeral

    analisador = AnalisadorGeral()
    if analisador.carregar_dados():
        relatorio_completo = analisador.gerar_relatorio_completo()

        visual = RelatoriosVisuais()

        # Gerar relatórios visuais
        if "analise_programas" in relatorio_completo:
            programas = relatorio_completo["analise_programas"]

            if "mapeamento_programas" in programas:
                relatorio_mapeamento = visual.gerar_relatorio_mapeamento(
                    programas["mapeamento_programas"]
                )
                arquivo_mapeamento = visual.salvar_relatorio_visual(
                    relatorio_mapeamento, "mapeamento_programas.txt"
                )
                print(f"✅ Relatório de mapeamento salvo: {arquivo_mapeamento}")

            if "cobertura_programatica" in programas:
                relatorio_cobertura = visual.gerar_relatorio_cobertura(
                    programas["cobertura_programatica"]
                )
                arquivo_cobertura = visual.salvar_relatorio_visual(
                    relatorio_cobertura, "cobertura_programatica.txt"
                )
                print(f"✅ Relatório de cobertura salvo: {arquivo_cobertura}")

            if "distribuicao_geografica" in programas:
                relatorio_distribuicao = visual.gerar_relatorio_distribuicao(
                    programas["distribuicao_geografica"]
                )
                arquivo_distribuicao = visual.salvar_relatorio_visual(
                    relatorio_distribuicao, "distribuicao_geografica.txt"
                )
                print(f"✅ Relatório de distribuição salvo: {arquivo_distribuicao}")

        # Relatório completo
        relatorio_completo_visual = visual.gerar_relatorio_completo(relatorio_completo)
        arquivo_completo = visual.salvar_relatorio_visual(
            relatorio_completo_visual, "relatorio_completo_visual.txt"
        )
        print(f"✅ Relatório completo visual salvo: {arquivo_completo}")


if __name__ == "__main__":
    main()
