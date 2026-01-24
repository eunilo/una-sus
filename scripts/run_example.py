#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
📚 EXEMPLO DE USO BÁSICO - SISTEMA UNA-SUS
==========================================

Demonstra como usar os principais componentes do sistema.
"""

import os
import sys
import os

# Garantir execução a partir da raiz do projeto e usar venv, se existir
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
os.chdir(BASE_DIR)
if sys.prefix == getattr(sys, "base_prefix", sys.prefix):
    venv_python = os.path.join(BASE_DIR, ".venv", "Scripts", "python.exe")
    if os.path.exists(venv_python):
        os.execv(venv_python, [venv_python, *sys.argv])

# Adicionar o diretório raiz ao path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


def exemplo_coleta_basica():
    """📊 Exemplo de coleta básica de dados"""
    print("\n📊 EXEMPLO: Coleta Básica de Dados")
    print("=" * 50)

    try:
        # Importar o scraper principal
        from scraper_unasus import main as scraper_main

        print("🚀 Executando coleta básica...")
        scraper_main()

        print("✅ Coleta concluída!")
        print("📁 Arquivo gerado: unasus_ofertas_detalhadas.csv")

    except Exception as e:
        print(f"❌ Erro na coleta: {e}")


def exemplo_coleta_melhorada():
    """🔧 Exemplo de coleta com melhorias"""
    print("\n🔧 EXEMPLO: Coleta Melhorada")
    print("=" * 50)

    try:
        # Importar o scraper melhorado
        from scraper_unasus_melhorado import main as scraper_melhorado_main

        print("🚀 Executando coleta melhorada...")
        scraper_melhorado_main()

        print("✅ Coleta melhorada concluída!")
        print("📁 Arquivos gerados:")
        print("   • unasus_ofertas_detalhadas.csv")
        print("   • Relatórios de análise")

    except Exception as e:
        print(f"❌ Erro na coleta melhorada: {e}")


def exemplo_analise_dados():
    """📈 Exemplo de análise de dados coletados"""
    print("\n📈 EXEMPLO: Análise de Dados")
    print("=" * 50)

    try:
        import pandas as pd

        # Carregar dados coletados
        df = pd.read_csv("unasus_ofertas_detalhadas.csv")

        print(f"📊 Total de registros: {len(df)}")
        print(f"📋 Colunas disponíveis: {list(df.columns)}")

        # Análise básica
        print("\n📈 ANÁLISE BÁSICA:")
        print(f"   • Cursos únicos: {df['no_curso'].nunique()}")
        print(f"   • Instituições: {df['no_orgao'].nunique()}")
        print(f"   • Modalidades: {df['no_modalidade'].unique()}")

    except Exception as e:
        print(f"❌ Erro na análise: {e}")


def exemplo_uso_coletor_database():
    """🗄️ Exemplo de uso do coletor de database"""
    print("\n🗄️ EXEMPLO: Coletor de Database")
    print("=" * 50)

    try:
        from coletor_database_geral import main as coletor_main

        print("🚀 Executando coletor de database...")
        coletor_main()

        print("✅ Coletor concluído!")
        print("📁 Arquivos gerados:")
        print("   • data/unasus_ofertas_detalhadas.csv")
        print("   • data/unasus_ofertas_melhoradas.csv")

    except Exception as e:
        print(f"❌ Erro no coletor: {e}")


def main():
    """🎯 Função principal com exemplos"""
    print("📚 SISTEMA UNA-SUS - EXEMPLOS DE USO")
    print("=" * 60)

    print("\n📁 ESTRUTURA DO PROJETO:")
    print("• scraper_unasus.py - Coleta básica")
    print("• scraper_unasus_melhorado.py - Coleta com melhorias")
    print("• coletor_database_geral.py - Coletor de database")
    print("• data/ - Dados coletados")
    print("• examples/ - Exemplos de uso")

    # Executar exemplos
    exemplo_coleta_basica()
    exemplo_analise_dados()
    exemplo_coleta_melhorada()
    exemplo_uso_coletor_database()

    print("\n🎉 TODOS OS EXEMPLOS CONCLUÍDOS!")
    print("\n💡 PRÓXIMOS PASSOS:")
    print("1. Execute os exemplos individualmente")
    print("2. Analise os arquivos gerados")
    print("3. Personalize conforme suas necessidades")


if __name__ == "__main__":
    main()
