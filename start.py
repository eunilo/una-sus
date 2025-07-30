#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🚀 START - Sistema UNA-SUS
==========================

Script de inicialização com menu completo para o sistema UNA-SUS.
"""

import os
import shutil
import subprocess
import sys
from datetime import datetime


def limpar_tela():
    """Limpa a tela do terminal."""
    os.system("cls" if os.name == "nt" else "clear")


def verificar_dados_existentes():
    """Verifica se existem dados coletados no diretório."""
    diretorios_dados = ["data", "logs", "checkpoints"]
    arquivos_dados = []

    for diretorio in diretorios_dados:
        if os.path.exists(diretorio):
            arquivos = os.listdir(diretorio)
            if arquivos:
                arquivos_dados.append(f"{diretorio}/ ({len(arquivos)} arquivos)")

    # Verificar arquivos CSV e DB na raiz
    for arquivo in os.listdir("."):
        if arquivo.endswith((".csv", ".db", ".json")):
            arquivos_dados.append(arquivo)

    return arquivos_dados


def limpar_dados_coletados():
    """Remove todos os dados coletados anteriormente."""
    print("🧹 Limpando dados coletados...")

    # Diretórios para limpar
    diretorios_limpar = ["data", "logs", "checkpoints"]

    for diretorio in diretorios_limpar:
        if os.path.exists(diretorio):
            try:
                shutil.rmtree(diretorio)
                print(f"  ✅ {diretorio}/ removido")
            except Exception as e:
                print(f"  ⚠️ Erro ao remover {diretorio}/: {e}")

    # Arquivos para limpar na raiz
    extensoes_limpar = [".csv", ".db", ".json"]
    for arquivo in os.listdir("."):
        if any(arquivo.endswith(ext) for ext in extensoes_limpar):
            try:
                os.remove(arquivo)
                print(f"  ✅ {arquivo} removido")
            except Exception as e:
                print(f"  ⚠️ Erro ao remover {arquivo}: {e}")

    print("✅ Limpeza concluída!")


def executar_varredura_completa():
    """Executa a varredura completa com dados limpos."""
    print("🚀 Iniciando varredura completa...")

    # Limpar dados primeiro
    limpar_dados_coletados()

    # Executar o coletor
    try:
        from coletor_database_geral import main as run_main

        run_main()
    except ImportError as e:
        print(f"❌ Erro de importação: {e}")
        print("💡 Execute: python coletor_database_geral.py")
    except Exception as e:
        print(f"❌ Erro inesperado: {e}")
        print("💡 Verifique se todas as dependências estão instaladas")


def verificar_banco_dados():
    """Verifica o banco de dados coletado."""
    print("📊 Verificando banco de dados...")

    # Verificar se existe database
    arquivos_db = [f for f in os.listdir(".") if f.endswith(".db")]
    arquivos_csv = [f for f in os.listdir(".") if f.endswith(".csv")]

    if not arquivos_db and not arquivos_csv:
        print("❌ Nenhum banco de dados encontrado!")
        print("💡 Execute primeiro a varredura completa")
        return

    # Verificar dados
    if arquivos_db:
        print(f"✅ Database encontrado: {arquivos_db[0]}")
        try:
            import sqlite3

            conn = sqlite3.connect(arquivos_db[0])
            cursor = conn.cursor()

            # Contar registros
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
            tabelas = cursor.fetchall()

            print(f"📋 Tabelas encontradas: {len(tabelas)}")
            for tabela in tabelas:
                cursor.execute(f"SELECT COUNT(*) FROM {tabela[0]}")
                count = cursor.fetchone()[0]
                print(f"  📊 {tabela[0]}: {count} registros")

            conn.close()
        except Exception as e:
            print(f"⚠️ Erro ao verificar database: {e}")

    if arquivos_csv:
        print(f"✅ CSV encontrado: {arquivos_csv[0]}")
        try:
            import pandas as pd

            df = pd.read_csv(arquivos_csv[0])
            print(f"📊 Registros no CSV: {len(df)}")
            print(f"📋 Colunas: {len(df.columns)}")
            print("📋 Primeiras colunas:", list(df.columns[:5]))
        except Exception as e:
            print(f"⚠️ Erro ao verificar CSV: {e}")

    # Verificar diretórios
    if os.path.exists("data"):
        arquivos_data = os.listdir("data")
        print(f"📁 Arquivos em data/: {len(arquivos_data)}")

    if os.path.exists("logs"):
        arquivos_logs = os.listdir("logs")
        print(f"📝 Arquivos em logs/: {len(arquivos_logs)}")

    if os.path.exists("checkpoints"):
        arquivos_checkpoints = os.listdir("checkpoints")
        print(f"💾 Arquivos em checkpoints/: {len(arquivos_checkpoints)}")


def mostrar_menu():
    """Exibe o menu principal."""
    limpar_tela()

    print("🏥 UNA-SUS - Sistema de Coleta e Análise de Dados Educacionais")
    print("=" * 70)
    print(f"📅 Data/Hora: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}")
    print()

    # Verificar dados existentes
    dados_existentes = verificar_dados_existentes()
    if dados_existentes:
        print("📊 Dados encontrados:")
        for dado in dados_existentes:
            print(f"  ✅ {dado}")
    else:
        print("📊 Nenhum dado coletado encontrado")

    print()
    print("🎯 Opções disponíveis:")
    print("  1. 🔄 Varredura Completa (limpa dados + coleta)")
    print("  2. 📊 Verificar Banco de Dados")
    print("  3. 🧹 Limpar Dados Coletados")
    print("  4. 🚀 Executar Coletor (sem limpar)")
    print("  5. 📋 Verificar Dependências")
    print("  0. ❌ Sair")
    print()


def verificar_dependencias():
    """Verifica se todas as dependências estão instaladas."""
    print("🔧 Verificando dependências...")

    dependencias = ["pandas", "requests", "bs4"]

    for dep in dependencias:
        try:
            __import__(dep)
            print(f"  ✅ {dep} instalado")
        except ImportError:
            print(f"  ❌ {dep} não encontrado")

    print()
    print("💡 Para instalar dependências faltantes:")
    print("   pip install pandas requests beautifulsoup4")


def main():
    """Função principal com menu interativo."""
    while True:
        try:
            mostrar_menu()

            opcao = input("📝 Escolha uma opção (0-5): ").strip()

            if opcao == "0":
                print("👋 Até logo!")
                break
            elif opcao == "1":
                print("\n" + "=" * 50)
                executar_varredura_completa()
                input("\n⏸️ Pressione ENTER para continuar...")
            elif opcao == "2":
                print("\n" + "=" * 50)
                verificar_banco_dados()
                input("\n⏸️ Pressione ENTER para continuar...")
            elif opcao == "3":
                print("\n" + "=" * 50)
                limpar_dados_coletados()
                input("\n⏸️ Pressione ENTER para continuar...")
            elif opcao == "4":
                print("\n" + "=" * 50)
                try:
                    from coletor_database_geral import main as run_main

                    run_main()
                except ImportError as e:
                    print(f"❌ Erro de importação: {e}")
                except Exception as e:
                    print(f"❌ Erro inesperado: {e}")
                input("\n⏸️ Pressione ENTER para continuar...")
            elif opcao == "5":
                print("\n" + "=" * 50)
                verificar_dependencias()
                input("\n⏸️ Pressione ENTER para continuar...")
            else:
                print("❌ Opção inválida! Digite um número de 0 a 5.")
                input("\n⏸️ Pressione ENTER para continuar...")

        except KeyboardInterrupt:
            print("\n👋 Até logo!")
            break
        except Exception as e:
            print(f"❌ Erro inesperado: {e}")
            input("\n⏸️ Pressione ENTER para continuar...")


if __name__ == "__main__":
    main()
