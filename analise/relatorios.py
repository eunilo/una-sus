#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Relatórios - Sistema de Análise UNA-SUS
=======================================

Módulo para geração de relatórios em diferentes formatos.
"""

import json
import os
from datetime import datetime
from typing import Any, Dict, List

import pandas as pd


def salvar_relatorio_json(relatorio: Dict[str, Any], nome_arquivo: str = None) -> str:
    """
    Salva relatório em formato JSON.

    Args:
        relatorio: Dicionário com o relatório
        nome_arquivo: Nome do arquivo (opcional)

    Returns:
        Caminho do arquivo salvo
    """
    if nome_arquivo is None:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        nome_arquivo = f"relatorio_analise_{timestamp}.json"

    # Criar diretório de relatórios se não existir
    os.makedirs("relatorios", exist_ok=True)

    caminho_arquivo = os.path.join("relatorios", nome_arquivo)

    with open(caminho_arquivo, "w", encoding="utf-8") as f:
        json.dump(relatorio, f, indent=2, ensure_ascii=False, default=str)

    print(f"✅ Relatório salvo: {caminho_arquivo}")
    return caminho_arquivo


def gerar_relatorio_texto(relatorio: Dict[str, Any]) -> str:
    """
    Gera relatório em formato de texto.

    Args:
        relatorio: Dicionário com o relatório

    Returns:
        String com o relatório formatado
    """
    texto = []

    # Cabeçalho
    texto.append("=" * 80)
    texto.append("📊 RELATÓRIO DE ANÁLISE - SISTEMA UNA-SUS")
    texto.append("=" * 80)
    texto.append(f"📅 Data/Hora: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}")
    texto.append(
        f"📁 Arquivo: {relatorio.get('metadata', {}).get('arquivo_dados', 'N/A')}"
    )
    texto.append("")

    # Estatísticas básicas
    if "estatisticas_basicas" in relatorio:
        stats = relatorio["estatisticas_basicas"]
        texto.append("📈 ESTATÍSTICAS BÁSICAS")
        texto.append("-" * 40)
        texto.append(f"Total de registros: {stats.get('total_registros', 0):,}")
        texto.append(f"Total de colunas: {stats.get('total_colunas', 0)}")
        texto.append(f"Uso de memória: {stats.get('memoria_uso', 0):,} bytes")
        texto.append("")

    # Análise de cursos
    if "analise_cursos" in relatorio:
        cursos = relatorio["analise_cursos"]
        texto.append("📚 ANÁLISE DE CURSOS")
        texto.append("-" * 40)
        texto.append(f"Total de cursos: {cursos.get('total_cursos', 0):,}")
        texto.append(f"Cursos únicos: {cursos.get('cursos_unicos', 0):,}")
        texto.append("")

        # Áreas temáticas
        if "areas_tematicas" in cursos and cursos["areas_tematicas"]:
            texto.append("🏷️ ÁREAS TEMÁTICAS (Top 10):")
            for area, count in list(cursos["areas_tematicas"].items())[:10]:
                texto.append(f"  • {area}: {count:,}")
            texto.append("")

        # Níveis
        if "niveis" in cursos and cursos["niveis"]:
            texto.append("📊 NÍVEIS:")
            for nivel, count in cursos["niveis"].items():
                texto.append(f"  • {nivel}: {count:,}")
            texto.append("")

    # Análise de ofertas
    if "analise_ofertas" in relatorio:
        ofertas = relatorio["analise_ofertas"]
        texto.append("🎯 ANÁLISE DE OFERTAS")
        texto.append("-" * 40)
        texto.append(f"Total de ofertas: {ofertas.get('total_ofertas', 0):,}")
        texto.append(f"Ofertas únicas: {ofertas.get('ofertas_unicas', 0):,}")
        texto.append(f"Vagas disponíveis: {ofertas.get('vagas_disponiveis', 0):,}")
        texto.append("")

        # Locais de oferta
        if "locais_oferta" in ofertas and ofertas["locais_oferta"]:
            texto.append("📍 LOCAIS DE OFERTA (Top 10):")
            for local, count in list(ofertas["locais_oferta"].items())[:10]:
                texto.append(f"  • {local}: {count:,}")
            texto.append("")

    # Colunas problemáticas
    if (
        "estatisticas_basicas" in relatorio
        and "colunas_info" in relatorio["estatisticas_basicas"]
    ):
        texto.append("⚠️ COLUNAS COM PROBLEMAS")
        texto.append("-" * 40)

        colunas_info = relatorio["estatisticas_basicas"]["colunas_info"]
        colunas_vazias = []
        colunas_muitos_nulos = []

        for coluna, info in colunas_info.items():
            if info.get("percentual_nulos", 0) == 100:
                colunas_vazias.append(coluna)
            elif info.get("percentual_nulos", 0) > 50:
                colunas_muitos_nulos.append(coluna)

        if colunas_vazias:
            texto.append("Colunas completamente vazias:")
            for coluna in colunas_vazias:
                texto.append(f"  • {coluna}")
            texto.append("")

        if colunas_muitos_nulos:
            texto.append("Colunas com muitos valores nulos (>50%):")
            for coluna in colunas_muitos_nulos:
                percentual = colunas_info[coluna]["percentual_nulos"]
                texto.append(f"  • {coluna}: {percentual:.1f}% nulos")
            texto.append("")

    texto.append("=" * 80)
    texto.append("📋 Relatório gerado automaticamente pelo Sistema UNA-SUS")
    texto.append("=" * 80)

    return "\n".join(texto)


def salvar_relatorio_texto(relatorio: Dict[str, Any], nome_arquivo: str = None) -> str:
    """
    Salva relatório em formato de texto.

    Args:
        relatorio: Dicionário com o relatório
        nome_arquivo: Nome do arquivo (opcional)

    Returns:
        Caminho do arquivo salvo
    """
    if nome_arquivo is None:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        nome_arquivo = f"relatorio_analise_{timestamp}.txt"

    # Criar diretório de relatórios se não existir
    os.makedirs("relatorios", exist_ok=True)

    caminho_arquivo = os.path.join("relatorios", nome_arquivo)
    texto_relatorio = gerar_relatorio_texto(relatorio)

    with open(caminho_arquivo, "w", encoding="utf-8") as f:
        f.write(texto_relatorio)

    print(f"✅ Relatório salvo: {caminho_arquivo}")
    return caminho_arquivo


def gerar_relatorio_resumido(relatorio: Dict[str, Any]) -> str:
    """
    Gera relatório resumido para exibição no terminal.

    Args:
        relatorio: Dicionário com o relatório

    Returns:
        String com o relatório resumido
    """
    texto = []

    texto.append("📊 RESUMO DA ANÁLISE")
    texto.append("=" * 50)

    if "estatisticas_basicas" in relatorio:
        stats = relatorio["estatisticas_basicas"]
        texto.append(f"📈 Total de registros: {stats.get('total_registros', 0):,}")
        texto.append(f"📋 Total de colunas: {stats.get('total_colunas', 0)}")

    if "analise_cursos" in relatorio:
        cursos = relatorio["analise_cursos"]
        texto.append(f"📚 Cursos únicos: {cursos.get('cursos_unicos', 0):,}")

    if "analise_ofertas" in relatorio:
        ofertas = relatorio["analise_ofertas"]
        texto.append(f"🎯 Ofertas únicas: {ofertas.get('ofertas_unicas', 0):,}")
        texto.append(f"💺 Vagas disponíveis: {ofertas.get('vagas_disponiveis', 0):,}")

    # Análise de programas de governo
    if "analise_programas" in relatorio and relatorio["analise_programas"]:
        programas = relatorio["analise_programas"]
        texto.append("")
        texto.append("🏛️ ANÁLISE DE PROGRAMAS DE GOVERNO:")

        if "mapeamento_programas" in programas:
            mapeamento = programas["mapeamento_programas"]
            texto.append(
                f"  • Programas únicos: {mapeamento.get('programas_unicos', 0)}"
            )
            texto.append(f"  • Total de cursos: {mapeamento.get('total_cursos', 0):,}")
            texto.append(
                f"  • Total de ofertas: {mapeamento.get('total_ofertas', 0):,}"
            )

        if "distribuicao_geografica" in programas:
            distribuicao = programas["distribuicao_geografica"]
            texto.append(
                f"  • Estados com dados: {distribuicao.get('estados_identificados', 0)}"
            )
            texto.append(
                f"  • Polos educacionais: {len(distribuicao.get('polos_educacionais', {}))}"
            )
            texto.append(
                f"  • Desertos educacionais: {len(distribuicao.get('desertos_educacionais', []))}"
            )

    return "\n".join(texto)


def gerar_relatorios_visuais(
    relatorio: Dict[str, Any], dados: pd.DataFrame = None
) -> List[str]:
    """
    Gera relatórios visuais detalhados.

    Args:
        relatorio: Dicionário com relatório completo
        dados: DataFrame com dados originais para detalhamento

    Returns:
        Lista com caminhos dos arquivos gerados
    """
    try:
        from analise.relatorios_visuais import RelatoriosVisuais

        visual = RelatoriosVisuais()
        if dados is not None:
            visual.dados = dados
        arquivos_gerados = []

        # Gerar relatórios específicos de programas
        if "analise_programas" in relatorio and relatorio["analise_programas"]:
            programas = relatorio["analise_programas"]

            if "mapeamento_programas" in programas:
                relatorio_mapeamento = visual.gerar_relatorio_mapeamento(
                    programas["mapeamento_programas"]
                )
                arquivo_mapeamento = visual.salvar_relatorio_visual(
                    relatorio_mapeamento, "mapeamento_programas.txt"
                )
                arquivos_gerados.append(arquivo_mapeamento)

            if "cobertura_programatica" in programas:
                # Relatório executivo (resumido)
                relatorio_executivo = visual.gerar_relatorio_cobertura_executivo(
                    programas["cobertura_programatica"]
                )
                arquivo_executivo = visual.salvar_relatorio_visual(
                    relatorio_executivo, "cobertura_programatica_executivo.txt"
                )
                arquivos_gerados.append(arquivo_executivo)

                # Relatório técnico completo
                relatorio_completo = visual.gerar_relatorio_cobertura_completo(
                    programas["cobertura_programatica"]
                )
                arquivo_completo = visual.salvar_relatorio_visual(
                    relatorio_completo, "cobertura_programatica_completo.txt"
                )
                arquivos_gerados.append(arquivo_completo)

            if "distribuicao_geografica" in programas:
                relatorio_distribuicao = visual.gerar_relatorio_distribuicao(
                    programas["distribuicao_geografica"]
                )
                arquivo_distribuicao = visual.salvar_relatorio_visual(
                    relatorio_distribuicao, "distribuicao_geografica.txt"
                )
                arquivos_gerados.append(arquivo_distribuicao)

                relatorio_distribuicao_completo = (
                    visual.gerar_relatorio_distribuicao_completo(
                        programas["distribuicao_geografica"]
                    )
                )
                arquivo_distribuicao_completo = visual.salvar_relatorio_visual(
                    relatorio_distribuicao_completo,
                    "distribuicao_geografica_completo.txt",
                )
                arquivos_gerados.append(arquivo_distribuicao_completo)

        # Relatório completo visual
        relatorio_completo_visual = visual.gerar_relatorio_completo(relatorio)
        arquivo_completo = visual.salvar_relatorio_visual(
            relatorio_completo_visual, "relatorio_completo_visual.txt"
        )
        arquivos_gerados.append(arquivo_completo)

        return arquivos_gerados

    except ImportError:
        print("⚠️ Módulo de relatórios visuais não disponível")
        return []
    except Exception as e:
        print(f"❌ Erro ao gerar relatórios visuais: {e}")
        return []
