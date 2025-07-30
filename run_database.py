#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script de Execução - Sistema de Database UNA-SUS
================================================

Script simples para executar o sistema principal de database.
"""

import importlib
import os
import subprocess
import sys


def instalar_dependencias():
    """Instala automaticamente as dependências necessárias."""
    print("🔧 Verificando e instalando dependências...")

    # Lista de dependências essenciais
    dependencias = ["pandas", "requests", "beautifulsoup4", "sqlite3"]

    dependencias_faltando = []

    for dep in dependencias:
        try:
            importlib.import_module(dep)
            print(f"  ✅ {dep} já está instalado")
        except ImportError:
            dependencias_faltando.append(dep)
            print(f"  ❌ {dep} não encontrado")

    if dependencias_faltando:
        print(
            f"\n📦 Instalando dependências faltantes: {', '.join(dependencias_faltando)}"
        )
        try:
            # Tentar instalar do requirements.txt primeiro
            if os.path.exists("requirements/requirements.txt"):
                subprocess.check_call(
                    [
                        sys.executable,
                        "-m",
                        "pip",
                        "install",
                        "-r",
                        "requirements/requirements.txt",
                    ]
                )
                print("✅ Dependências instaladas com sucesso!")
            else:
                # Instalar individualmente
                for dep in dependencias_faltando:
                    if dep == "sqlite3":
                        print("  ℹ️ sqlite3 é parte do Python padrão")
                        continue
                    subprocess.check_call([sys.executable, "-m", "pip", "install", dep])
                    print(f"  ✅ {dep} instalado")
        except subprocess.CalledProcessError as e:
            print(f"❌ Erro ao instalar dependências: {e}")
            print(
                "💡 Tente executar manualmente: pip install -r requirements/requirements.txt"
            )
            return False

    return True


def verificar_dados():
    """Verifica se existem dados para processar."""
    arquivos_dados = [
        "unasus_ofertas_detalhadas.csv",
        "data/raw/unasus_ofertas_detalhadas.csv",
        "data/processed/database_geral.db",
    ]

    dados_encontrados = []
    for arquivo in arquivos_dados:
        if os.path.exists(arquivo):
            dados_encontrados.append(arquivo)

    return dados_encontrados


def menu_principal():
    """Exibe o menu principal e gerencia as opções."""
    print("\n" + "=" * 60)
    print("🏥 SISTEMA DE DATABASE UNA-SUS")
    print("=" * 60)

    dados_disponiveis = verificar_dados()

    if dados_disponiveis:
        print(f"\n📊 Dados encontrados:")
        for dado in dados_disponiveis:
            print(f"  ✅ {dado}")
    else:
        print("\n⚠️ Nenhum dado encontrado!")

    print("\n🎯 Opções disponíveis:")
    print("  1. Criar/Atualizar Database (Recomendado)")
    print("  2. Executar Scraper Básico")
    print("  3. Executar Scraper Melhorado")
    print("  4. Ver Estatísticas do Database")
    print("  5. Exportar Dados")
    print("  0. Sair")

    while True:
        try:
            opcao = input("\n📝 Escolha uma opção (0-5): ").strip()

            if opcao == "0":
                print("👋 Até logo!")
                return False
            elif opcao == "1":
                return "database"
            elif opcao == "2":
                return "scraper_basic"
            elif opcao == "3":
                return "scraper_enhanced"
            elif opcao == "4":
                return "estatisticas"
            elif opcao == "5":
                return "exportar"
            else:
                print("❌ Opção inválida! Digite um número de 0 a 5.")
        except KeyboardInterrupt:
            print("\n👋 Até logo!")
            return False


def executar_opcao(opcao):
    """Executa a opção escolhida pelo usuário."""
    print(f"\n🚀 Executando: {opcao}")

    if opcao == "database":
        # Adicionar src ao path
        sys.path.insert(0, os.path.join(os.path.dirname(__file__), "src"))
        from core.database import main

        main()

    elif opcao == "scraper_basic":
        # Adicionar src ao path
        sys.path.insert(0, os.path.join(os.path.dirname(__file__), "src"))
        from scrapers.basic import main

        main()

    elif opcao == "scraper_enhanced":
        # Adicionar src ao path
        sys.path.insert(0, os.path.join(os.path.dirname(__file__), "src"))
        from scrapers.enhanced import main

        main()

    elif opcao == "estatisticas":
        print("📊 Funcionalidade de estatísticas será implementada em breve!")

    elif opcao == "exportar":
        print("📤 Funcionalidade de exportação será implementada em breve!")


def main():
    """Função principal do script."""
    print("🚀 Iniciando Sistema UNA-SUS...")

    # 1. Instalar dependências automaticamente
    if not instalar_dependencias():
        print("❌ Falha na instalação de dependências. Encerrando...")
        return

    # 2. Loop principal do menu
    while True:
        opcao = menu_principal()

        if opcao is False:
            break

        executar_opcao(opcao)

        # Perguntar se quer continuar
        try:
            continuar = (
                input("\n🔄 Deseja executar outra operação? (s/n): ").strip().lower()
            )
            if continuar not in ["s", "sim", "y", "yes"]:
                print("👋 Até logo!")
                break
        except KeyboardInterrupt:
            print("\n👋 Até logo!")
            break


if __name__ == "__main__":
    main()
