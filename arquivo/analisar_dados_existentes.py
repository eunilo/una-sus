#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ANÁLISE DOS DADOS EXISTENTES
============================

Analisa os dados coletados pelo scraper_unasus.py para planejar
o database geral.
"""

import json
import os
from datetime import datetime

import pandas as pd


def analisar_dados_existentes():
    """Analisa os dados existentes para planejar o database geral."""
    print("🔍 ANÁLISE DOS DADOS EXISTENTES")
    print("=" * 50)

    # Verificar arquivo existente
    arquivo = "unasus_ofertas_detalhadas.csv"
    if not os.path.exists(arquivo):
        print(f"❌ Arquivo {arquivo} não encontrado!")
        return

    print(f"📁 Analisando: {arquivo}")

    # Carregar dados
    df = pd.read_csv(arquivo)

    print(f"\n📊 ESTATÍSTICAS BÁSICAS:")
    print(f"   • Total de registros: {len(df):,}")
    print(f"   • Total de colunas: {len(df.columns)}")
    print(f"   • Tamanho do arquivo: {os.path.getsize(arquivo) / 1024 / 1024:.2f} MB")

    # Analisar colunas
    print(f"\n📋 ESTRUTURA DAS COLUNAS:")
    print("-" * 50)

    for i, coluna in enumerate(df.columns, 1):
        na_count = df[coluna].isna().sum()
        na_percent = (na_count / len(df)) * 100
        unique_count = df[coluna].nunique()

        print(f"{i:2d}. {coluna}")
        print(
            f"     • Preenchido: {100 - na_percent:.1f}% ({len(df) - na_count:,} registros)"
        )
        print(f"     • Valores únicos: {unique_count:,}")

        # Mostrar exemplo de valor
        if na_count < len(df):
            exemplo = df[coluna].dropna().iloc[0]
            if isinstance(exemplo, str) and len(exemplo) > 50:
                print(f"     • Exemplo: {exemplo[:50]}...")
            else:
                print(f"     • Exemplo: {exemplo}")
        print()

    # Analisar relacionamentos
    print(f"\n🔗 ANÁLISE DE RELACIONAMENTOS:")
    print("-" * 50)

    # Cursos únicos
    if "co_seq_curso" in df.columns:
        cursos_unicos = df["co_seq_curso"].nunique()
        print(f"   • Cursos únicos: {cursos_unicos:,}")

    # Instituições
    if "no_orgao" in df.columns:
        instituicoes = df["no_orgao"].nunique()
        print(f"   • Instituições: {instituicoes:,}")

    # Modalidades
    if "no_modalidade" in df.columns:
        modalidades = df["no_modalidade"].value_counts()
        print(f"   • Modalidades: {len(modalidades)}")
        for modalidade, count in modalidades.head().items():
            print(f"     - {modalidade}: {count:,}")

    # Status
    if "status" in df.columns:
        status = df["status"].value_counts()
        print(f"   • Status: {len(status)}")
        for stat, count in status.items():
            print(f"     - {stat}: {count:,}")

    # Carga horária
    if "qt_carga_horaria_total" in df.columns:
        carga_stats = df["qt_carga_horaria_total"].describe()
        print(f"   • Carga horária:")
        print(f"     - Média: {carga_stats['mean']:.0f} horas")
        print(f"     - Mínima: {carga_stats['min']:.0f} horas")
        print(f"     - Máxima: {carga_stats['max']:.0f} horas")

    # DEIA
    if "tem_deia" in df.columns:
        deia = df["tem_deia"].value_counts()
        print(f"   • DEIA:")
        for resposta, count in deia.items():
            print(f"     - {resposta}: {count:,}")

    # Proporções importantes
    print(f"\n📈 PROPORÇÕES IMPORTANTES:")
    print("-" * 50)

    if "status" in df.columns:
        ativos = df[df["status"] == "Ativo"].shape[0]
        percent_ativo = (ativos / len(df)) * 100
        print(f"   • Ofertas ativas: {percent_ativo:.1f}% ({ativos:,})")

    if "tem_deia" in df.columns:
        com_deia = df[df["tem_deia"] == "Sim"].shape[0]
        percent_deia = (com_deia / len(df)) * 100
        print(f"   • Com DEIA: {percent_deia:.1f}% ({com_deia:,})")

    # Qualidade dos dados
    print(f"\n✅ QUALIDADE DOS DADOS:")
    print("-" * 50)

    colunas_importantes = [
        "co_seq_curso",
        "no_curso",
        "no_orgao",
        "no_modalidade",
        "status",
    ]
    colunas_presentes = [col for col in colunas_importantes if col in df.columns]

    for coluna in colunas_presentes:
        na_count = df[coluna].isna().sum()
        percent_preenchido = ((len(df) - na_count) / len(df)) * 100
        print(f"   • {coluna}: {percent_preenchido:.1f}% preenchido")

    # Recomendações para database
    print(f"\n💡 RECOMENDAÇÕES PARA DATABASE:")
    print("-" * 50)

    print("1. 📊 ESTRUTURA DE TABELAS:")
    print("   • Tabela 'cursos': Informações básicas dos cursos")
    print("   • Tabela 'ofertas': Informações das ofertas")
    print("   • Tabela 'instituicoes': Dados das instituições")
    print("   • Tabela 'modalidades': Tipos de modalidade")

    print("\n2. 🔍 CAMPOS ESSENCIAIS:")
    campos_essenciais = [
        "co_seq_curso",
        "no_curso",
        "no_orgao",
        "no_modalidade",
        "status",
    ]
    for campo in campos_essenciais:
        if campo in df.columns:
            print(f"   • {campo} - ✅ Presente")
        else:
            print(f"   • {campo} - ❌ Faltando")

    print("\n3. 🛠️ MELHORIAS NECESSÁRIAS:")
    print("   • Normalização de dados")
    print("   • Validação de integridade")
    print("   • Sistema de versionamento")
    print("   • Backup automático")
    print("   • APIs de acesso")

    print("\n4. 📈 PRÓXIMOS PASSOS:")
    print("   • Implementar sistema de database")
    print("   • Criar APIs REST")
    print("   • Desenvolver dashboard")
    print("   • Implementar monitoramento")

    # Salvar análise
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    relatorio = {
        "timestamp": timestamp,
        "arquivo_analisado": arquivo,
        "total_registros": len(df),
        "total_colunas": len(df.columns),
        "tamanho_arquivo_mb": os.path.getsize(arquivo) / 1024 / 1024,
        "colunas": list(df.columns),
        "estatisticas": {
            "cursos_unicos": (
                df["co_seq_curso"].nunique() if "co_seq_curso" in df.columns else 0
            ),
            "instituicoes": df["no_orgao"].nunique() if "no_orgao" in df.columns else 0,
            "modalidades": (
                df["no_modalidade"].nunique() if "no_modalidade" in df.columns else 0
            ),
        },
    }

    with open(f"analise_dados_{timestamp}.json", "w", encoding="utf-8") as f:
        json.dump(relatorio, f, indent=2, ensure_ascii=False)

    print(f"\n💾 Relatório salvo: analise_dados_{timestamp}.json")


if __name__ == "__main__":
    analisar_dados_existentes()
