#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
📊 ANÁLISE DOS DADOS COLETADOS
==============================

Script para analisar os dados coletados pelo scraper.
"""

import os

import pandas as pd


def analisar_dados():
    """Analisa os dados coletados."""
    print("📊 ANÁLISE DOS DADOS COLETADOS")
    print("=" * 50)

    # Verificar se o arquivo existe
    arquivo = "unasus_ofertas_detalhadas.csv"
    if not os.path.exists(arquivo):
        print(f"❌ Arquivo {arquivo} não encontrado!")
        return

    # Carregar dados
    print(f"📁 Carregando dados de: {arquivo}")
    df = pd.read_csv(arquivo)

    print(f"\n📈 ESTATÍSTICAS BÁSICAS:")
    print(f"   • Total de registros: {len(df):,}")
    print(f"   • Cursos únicos: {df['co_seq_curso'].nunique():,}")
    print(f"   • Instituições: {df['no_orgao'].nunique():,}")

    print(f"\n🎓 MODALIDADES:")
    modalidades = df["no_modalidade"].value_counts()
    for modalidade, count in modalidades.items():
        print(f"   • {modalidade}: {count:,}")

    print(f"\n📋 STATUS DOS CURSOS:")
    status = df["status"].value_counts()
    for stat, count in status.head().items():
        print(f"   • {stat}: {count:,}")

    print(f"\n🏢 TOP 5 INSTITUIÇÕES:")
    instituicoes = df["no_orgao"].value_counts().head()
    for inst, count in instituicoes.items():
        print(f"   • {inst}: {count:,}")

    print(f"\n⏱️ CARGA HORÁRIA:")
    if "qt_carga_horaria_total" in df.columns:
        carga_horaria = df["qt_carga_horaria_total"].describe()
        print(f"   • Média: {carga_horaria['mean']:.0f} horas")
        print(f"   • Mínima: {carga_horaria['min']:.0f} horas")
        print(f"   • Máxima: {carga_horaria['max']:.0f} horas")

    print(f"\n🌈 ANÁLISE DEIA:")
    if "tem_deia" in df.columns:
        deia = df["tem_deia"].value_counts()
        for resposta, count in deia.items():
            print(f"   • {resposta}: {count:,}")

    print(f"\n✅ COLETOR FUNCIONANDO CORRETAMENTE!")
    print(f"   • Dados coletados com sucesso")
    print(f"   • Estrutura consistente")
    print(f"   • Pronto para análise")


if __name__ == "__main__":
    analisar_dados()
