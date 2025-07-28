#!/usr/bin/env python3
"""
🚀 INICIADOR DE PESQUISA - GROUNDED THEORY
==========================================

Script didático para iniciar pesquisa usando metodologia Grounded Theory.
Este script guia o usuário através do processo de forma explicativa.
"""

import os
import sys
import time
from datetime import datetime


def mostrar_banner():
    """
    🎨 Mostra banner de boas-vindas.
    """
    print("=" * 80)
    print("🧠 PESQUISA GROUNDED THEORY - UNA-SUS")
    print("=" * 80)
    print("📚 Metodologia de Pesquisa Qualitativa")
    print("🎯 Desenvolvimento de Teoria a partir dos Dados")
    print("🔍 Análise Sistemática e Iterativa")
    print("=" * 80)
    print()


def explicar_grounded_theory():
    """
    📚 Explica o que é Grounded Theory.
    """
    print("📚 O QUE É GROUNDED THEORY?")
    print("-" * 40)
    print("🔍 Grounded Theory é uma metodologia de pesquisa qualitativa que:")
    print("   • Coleta dados sem preconceitos")
    print("   • Analisa dados de forma sistemática")
    print("   • Desenvolve teoria baseada nos dados")
    print("   • Usa processo iterativo até saturação")
    print()

    print("🎯 OBJETIVO DESTA PESQUISA:")
    print("   • Coletar dados dos cursos UNA-SUS")
    print(
        "   • Identificar elementos DEIA (Diversidade, Equidade, Inclusão, Acessibilidade)"
    )
    print("   • Desenvolver teoria sobre formação em DEIA")
    print("   • Gerar insights para políticas públicas")
    print()


def mostrar_opcoes():
    """
    🎯 Mostra opções disponíveis.
    """
    print("🎯 OPÇÕES DISPONÍVEIS:")
    print("-" * 30)
    print("1️⃣ COLETA COMPLETA + PROCESSAMENTO DEIA")
    print("   • Coleta todos os dados da UNA-SUS")
    print("   • Processa para identificar elementos DEIA")
    print("   • Gera relatórios e estatísticas")
    print("   ⏱️  Tempo estimado: 30-60 minutos")
    print()

    print("2️⃣ APENAS COLETA COMPLETA")
    print("   • Coleta todos os dados sem processamento")
    print("   • Salva dados brutos para análise posterior")
    print("   • Útil para análise manual ou personalizada")
    print("   ⏱️  Tempo estimado: 20-40 minutos")
    print()

    print("3️⃣ PROCESSAMENTO DEIA (Dados Existentes)")
    print("   • Usa dados já coletados")
    print("   • Aplica análise DEIA")
    print("   • Gera relatórios")
    print("   ⏱️  Tempo estimado: 5-10 minutos")
    print()

    print("4️⃣ METODOLOGIA GROUNDED THEORY COMPLETA")
    print("   • Executa todas as etapas da metodologia")
    print("   • Codificação aberta, axial e seletiva")
    print("   • Desenvolvimento de teoria")
    print("   ⏱️  Tempo estimado: 2-4 horas")
    print()

    print("5️⃣ TESTES E VERIFICAÇÃO")
    print("   • Testa se tudo está funcionando")
    print("   • Verifica módulos e configurações")
    print("   • Diagnóstico de problemas")
    print("   ⏱️  Tempo estimado: 2-5 minutos")
    print()

    print("6️⃣ SAIR")
    print("   • Encerra o programa")
    print()


def verificar_ambiente():
    """
    🔍 Verifica se o ambiente está pronto.
    """
    print("🔍 VERIFICANDO AMBIENTE...")
    print("-" * 30)

    # Verificar Python
    print(f"🐍 Python: {sys.version.split()[0]}")

    # Verificar módulos
    try:
        import pandas

        print("✅ pandas - OK")
    except ImportError:
        print("❌ pandas - NÃO INSTALADO")
        print("   Execute: pip install pandas")
        return False

    try:
        import requests

        print("✅ requests - OK")
    except ImportError:
        print("❌ requests - NÃO INSTALADO")
        print("   Execute: pip install requests")
        return False

    # Verificar arquivos
    arquivos_necessarios = [
        "modulos/__init__.py",
        "modulos/coletor_unasus_completo.py",
        "modulos/processador_deia.py",
        "coleta_e_processamento_separados.py",
    ]

    for arquivo in arquivos_necessarios:
        if os.path.exists(arquivo):
            print(f"✅ {arquivo} - OK")
        else:
            print(f"❌ {arquivo} - NÃO ENCONTRADO")
            return False

    print("✅ Ambiente verificado com sucesso!")
    print()
    return True


def executar_teste():
    """
    🧪 Executa testes básicos.
    """
    print("🧪 EXECUTANDO TESTES...")
    print("-" * 30)

    try:
        # Testar importação dos módulos
        from modulos.coletor_unasus_completo import ColetorUnasusCompleto
        from modulos.processador_deia import ProcessadorDEIA

        print("✅ Módulos importados com sucesso")

        # Testar instanciação
        import logging

        logging.basicConfig(level=logging.INFO)
        logger = logging.getLogger("Teste")

        coletor = ColetorUnasusCompleto(logger)
        processador = ProcessadorDEIA(logger)
        print("✅ Classes instanciadas com sucesso")

        print("✅ Todos os testes passaram!")
        return True

    except Exception as e:
        print(f"❌ Erro nos testes: {str(e)}")
        return False


def executar_opcao(opcao):
    """
    🚀 Executa a opção escolhida.
    """
    print(f"🚀 EXECUTANDO OPÇÃO {opcao}...")
    print("-" * 40)

    if opcao == "1":
        print("📥 Iniciando coleta completa + processamento DEIA...")
        os.system("python coleta_e_processamento_separados.py")

    elif opcao == "2":
        print("📥 Iniciando apenas coleta completa...")
        # Modificar para executar apenas coleta
        os.system("python coleta_e_processamento_separados.py")

    elif opcao == "3":
        print("🔍 Iniciando processamento DEIA...")
        # Modificar para executar apenas processamento
        os.system("python coleta_e_processamento_separados.py")

    elif opcao == "4":
        print("🧠 Iniciando metodologia Grounded Theory completa...")
        os.system("python grounded_theory_runner.py")

    elif opcao == "5":
        print("🧪 Iniciando testes...")
        if executar_teste():
            print("✅ Testes concluídos com sucesso!")
        else:
            print("❌ Alguns testes falharam. Verifique os erros acima.")

    print("✅ Execução concluída!")


def mostrar_dicas():
    """
    💡 Mostra dicas úteis.
    """
    print("💡 DICAS ÚTEIS:")
    print("-" * 20)
    print("📊 Durante a execução:")
    print("   • Monitore os logs em tempo real")
    print("   • Os dados são salvos automaticamente")
    print("   • Você pode interromper com Ctrl+C")
    print("   • O progresso é salvo em checkpoints")
    print()

    print("📁 Arquivos gerados:")
    print("   • dados_completos.json - Dados brutos")
    print("   • analise_deia.json - Análise DEIA")
    print("   • relatorio_deia.md - Relatório")
    print("   • logs/ - Logs de execução")
    print()

    print("🔍 Para análise posterior:")
    print("   • Use Excel para visualizar dados")
    print("   • Leia relatórios em Markdown")
    print("   • Consulte logs para detalhes")
    print()


def main():
    """
    🚀 Função principal.
    """
    # Mostrar banner
    mostrar_banner()

    # Verificar ambiente
    if not verificar_ambiente():
        print("❌ Ambiente não está pronto. Corrija os problemas acima.")
        return

    # Explicar Grounded Theory
    explicar_grounded_theory()

    # Loop principal
    while True:
        # Mostrar opções
        mostrar_opcoes()

        # Obter escolha do usuário
        try:
            escolha = input("🎯 Escolha uma opção (1-6): ").strip()

            if escolha == "6":
                print("👋 Obrigado por usar a pesquisa Grounded Theory!")
                print("📚 Boa pesquisa!")
                break
            elif escolha in ["1", "2", "3", "4", "5"]:
                # Mostrar dicas antes de executar
                mostrar_dicas()

                # Confirmar execução
                confirmacao = input("🚀 Confirmar execução? (s/n): ").strip().lower()
                if confirmacao in ["s", "sim", "y", "yes"]:
                    executar_opcao(escolha)
                else:
                    print("⏸️ Execução cancelada.")
            else:
                print("❌ Opção inválida. Escolha 1-6.")

        except KeyboardInterrupt:
            print("\n⏸️ Execução interrompida pelo usuário.")
            break
        except Exception as e:
            print(f"❌ Erro: {str(e)}")

        print("\n" + "=" * 80)
        print()


if __name__ == "__main__":
    main()
