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
import io
from datetime import datetime

# Garantir execução a partir da raiz do projeto
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
os.chdir(BASE_DIR)

# Tentar usar automaticamente o Python do venv, se existir
def garantir_venv():
    """Reexecuta o script usando o Python do .venv, se necessário."""
    if sys.prefix != getattr(sys, "base_prefix", sys.prefix):
        return

    venv_python = os.path.join(BASE_DIR, ".venv", "Scripts", "python.exe")
    if os.path.exists(venv_python):
        os.execv(venv_python, [venv_python, *sys.argv])


# Garantir saída compatível no Windows (evita erro de emoji/acentos)
if os.name == "nt":
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding="utf-8", errors="replace")

garantir_venv()


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


def limpar_relatorios():
    """Remove todos os relatórios gerados."""
    print("🧹 Limpando relatórios...")

    pasta = "relatorios"
    if not os.path.exists(pasta):
        os.makedirs(pasta, exist_ok=True)
        print("ℹ️ Pasta 'relatorios' não existia. Criada.")
        return

    removidos = 0
    for item in os.listdir(pasta):
        caminho = os.path.join(pasta, item)
        try:
            if os.path.isdir(caminho):
                shutil.rmtree(caminho)
            else:
                os.remove(caminho)
            removidos += 1
        except Exception as e:
            print(f"  ⚠️ Erro ao remover {item}: {e}")

    print(f"✅ Relatórios limpos: {removidos} itens removidos.")


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

    # Verificar se existe database (raiz e data/)
    arquivos_db = [f for f in os.listdir(".") if f.endswith(".db")]
    arquivos_csv = [f for f in os.listdir(".") if f.endswith(".csv")]
    arquivos_db_data = []
    arquivos_csv_data = []
    if os.path.exists("data"):
        arquivos_db_data = [
            os.path.join("data", f) for f in os.listdir("data") if f.endswith(".db")
        ]
        arquivos_csv_data = [
            os.path.join("data", f) for f in os.listdir("data") if f.endswith(".csv")
        ]

    arquivos_db.extend(arquivos_db_data)
    arquivos_csv.extend(arquivos_csv_data)

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
    print("  6. 📈 Análise Completa dos Dados")
    print("  7. 📊 Estatísticas Básicas")
    print("  8. 📋 Gerar Relatórios")
    print("  9. 🧪 Diagnóstico (erros e dependências)")
    print(" 10. 🧹 Limpar Relatórios")
    print("  0. ❌ Sair")
    print()


def verificar_dependencias():
    """Verifica se todas as dependências estão instaladas."""
    print("🔧 Verificando dependências...")

    dependencias = ["pandas", "requests", "bs4", "openpyxl", "lxml"]

    for dep in dependencias:
        try:
            __import__(dep)
            print(f"  ✅ {dep} instalado")
        except ImportError:
            print(f"  ❌ {dep} não encontrado")

    print()
    print("💡 Para instalar dependências faltantes:")
    print("   pip install pandas requests beautifulsoup4")


def diagnostico_sistema():
    """Verifica erros comuns e instala dependências faltantes."""
    print("🧪 Diagnóstico do sistema...")

    # Garantir diretórios básicos
    for diretorio in ["data", "logs", "checkpoints"]:
        os.makedirs(diretorio, exist_ok=True)

    # Verificar dependências e instalar faltantes
    dependencias = {
        "pandas": "pandas",
        "requests": "requests",
        "bs4": "beautifulsoup4",
        "openpyxl": "openpyxl",
        "lxml": "lxml",
    }

    faltantes = []
    for modulo, pacote in dependencias.items():
        try:
            __import__(modulo)
            print(f"  ✅ {modulo} instalado")
        except ImportError:
            print(f"  ❌ {modulo} não encontrado")
            faltantes.append(pacote)

    if faltantes:
        print("\n📦 Instalando dependências faltantes...")
        try:
            usando_venv = sys.prefix != getattr(sys, "base_prefix", sys.prefix)
            comando = [sys.executable, "-m", "pip", "install"]
            if not usando_venv:
                comando.append("--user")
            comando.extend(faltantes)
            subprocess.check_call(comando)
            print("✅ Dependências instaladas com sucesso!")
        except subprocess.CalledProcessError as e:
            print(f"❌ Falha ao instalar dependências: {e}")
    else:
        print("\n✅ Nenhuma dependência faltante.")

    # Verificar banco de dados
    print("\n📊 Verificação de dados:")
    verificar_banco_dados()


def executar_analise_completa():
    """Executa análise completa dos dados."""
    print("📈 Executando análise completa...")

    try:
        from analise.analisador_geral import AnalisadorGeral

        analisador = AnalisadorGeral()

        if analisador.carregar_dados():
            relatorio = analisador.gerar_relatorio_completo()

            # Mostrar resumo
            from analise.relatorios import gerar_relatorio_resumido

            resumo = gerar_relatorio_resumido(relatorio)
            print("\n" + resumo)

            # Análise de programas de governo
            if "analise_programas" in relatorio and relatorio["analise_programas"]:
                programas = relatorio["analise_programas"]
                print("\n🏛️ ANÁLISE DE PROGRAMAS DE GOVERNO:")

                if "mapeamento_programas" in programas:
                    mapeamento = programas["mapeamento_programas"]
                    print(
                        f"  • Programas únicos: {mapeamento.get('programas_unicos', 0)}"
                    )
                    print(f"  • Total de cursos: {mapeamento.get('total_cursos', 0):,}")
                    print(
                        f"  • Total de ofertas: {mapeamento.get('total_ofertas', 0):,}"
                    )

                if "distribuicao_geografica" in programas:
                    distribuicao = programas["distribuicao_geografica"]
                    estados = distribuicao.get('estados_identificados', 0)
                    polos = len(distribuicao.get('polos_educacionais', {}))
                    desertos = len(distribuicao.get('desertos_educacionais', []))
                    
                    print(f"  • Estados com dados: {estados}")
                    print(f"  • Polos educacionais: {polos}")
                    print(f"  • Desertos educacionais: {desertos}")

            # Salvar relatórios
            from analise.relatorios import salvar_relatorio_json, salvar_relatorio_texto

            salvar_relatorio_json(relatorio)
            salvar_relatorio_texto(relatorio)

        else:
            print("❌ Não foi possível carregar os dados!")
            print("💡 Execute primeiro a varredura completa")

    except ImportError as e:
        print(f"❌ Erro de importação: {e}")
        print("💡 Verifique se o módulo de análise está disponível")
    except Exception as e:
        print(f"❌ Erro inesperado: {e}")


def executar_estatisticas_basicas():
    """Executa estatísticas básicas dos dados."""
    print("📊 Executando estatísticas básicas...")

    try:
        from analise.analisador_geral import AnalisadorGeral

        analisador = AnalisadorGeral()

        if analisador.carregar_dados():
            estatisticas = analisador.gerar_estatisticas_basicas()

            print(f"\n📈 ESTATÍSTICAS BÁSICAS:")
            total_registros = estatisticas.get('total_registros', 0)
            total_colunas = estatisticas.get('total_colunas', 0)
            memoria_uso = estatisticas.get('memoria_uso', 0)
            
            print(f"Total de registros: {total_registros:,}")
            print(f"Total de colunas: {total_colunas}")
            print(f"Uso de memória: {memoria_uso:,} bytes")

            # Mostrar colunas com problemas
            if "colunas_info" in estatisticas:
                print(f"\n⚠️ COLUNAS COM PROBLEMAS:")
                for coluna, info in estatisticas["colunas_info"].items():
                    percentual = info.get("percentual_nulos", 0)
                    if percentual > 50:
                        print(f"  • {coluna}: {percentual:.1f}% nulos")

        else:
            print("❌ Não foi possível carregar os dados!")
            print("💡 Execute primeiro a varredura completa")

    except ImportError as e:
        print(f"❌ Erro de importação: {e}")
        print("💡 Verifique se o módulo de análise está disponível")
    except Exception as e:
        print(f"❌ Erro inesperado: {e}")


def gerar_relatorios():
    """Gera relatórios dos dados."""
    print("📋 Gerando relatórios...")

    try:
        from analise.analisador_geral import AnalisadorGeral

        analisador = AnalisadorGeral()

        if analisador.carregar_dados():
            relatorio = analisador.gerar_relatorio_completo()

            # Salvar relatórios básicos
            from analise.relatorios import salvar_relatorio_json, salvar_relatorio_texto

            arquivo_json = salvar_relatorio_json(relatorio)
            arquivo_txt = salvar_relatorio_texto(relatorio)

            print(f"\n✅ Relatórios básicos gerados:")
            print(f"  📄 JSON: {arquivo_json}")
            print(f"  📄 TXT: {arquivo_txt}")

            # Gerar relatórios visuais
            from analise.relatorios import gerar_relatorios_visuais

            print("\n🎨 Gerando relatórios visuais...")
            arquivos_visuais = gerar_relatorios_visuais(relatorio, analisador.dados)

            if arquivos_visuais:
                print("✅ Relatórios visuais gerados:")
                for arquivo in arquivos_visuais:
                    print(f"  📊 {os.path.basename(arquivo)}")
            else:
                print("⚠️ Não foi possível gerar relatórios visuais")

        else:
            print("❌ Não foi possível carregar os dados!")
            print("💡 Execute primeiro a varredura completa")

    except ImportError as e:
        print(f"❌ Erro de importação: {e}")
        print("💡 Verifique se o módulo de análise está disponível")
    except Exception as e:
        print(f"❌ Erro inesperado: {e}")


def main():
    """Função principal com menu interativo."""
    while True:
        try:
            mostrar_menu()

            opcao = input("📝 Escolha uma opção (0-10): ").strip()

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
            elif opcao == "6":
                print("\n" + "=" * 50)
                executar_analise_completa()
                input("\n⏸️ Pressione ENTER para continuar...")
            elif opcao == "7":
                print("\n" + "=" * 50)
                executar_estatisticas_basicas()
                input("\n⏸️ Pressione ENTER para continuar...")
            elif opcao == "8":
                print("\n" + "=" * 50)
                gerar_relatorios()
                input("\n⏸️ Pressione ENTER para continuar...")
            elif opcao == "9":
                print("\n" + "=" * 50)
                diagnostico_sistema()
                input("\n⏸️ Pressione ENTER para continuar...")
            elif opcao == "10":
                print("\n" + "=" * 50)
                limpar_relatorios()
                input("\n⏸️ Pressione ENTER para continuar...")
            else:
                print("❌ Opção inválida! Digite um número de 0 a 10.")
                input("\n⏸️ Pressione ENTER para continuar...")

        except KeyboardInterrupt:
            print("\n👋 Até logo!")
            break
        except Exception as e:
            print(f"❌ Erro inesperado: {e}")
            input("\n⏸️ Pressione ENTER para continuar...")


if __name__ == "__main__":
    main()
