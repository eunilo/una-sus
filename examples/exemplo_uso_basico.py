#!/usr/bin/env python3
"""
📚 Exemplo de Uso Básico - UNA-SUS Scraper
==========================================

Este exemplo demonstra como usar o scraper de forma básica
para coletar dados de cursos da UNA-SUS.
"""

import os
import sys

# Adicionar o diretório pai ao path para importar os módulos
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from analisar_dados_coletados import main as analise_main
from scraper_unasus_melhorado import main as scraper_main


def exemplo_coleta_basica():
    """
    🚀 Exemplo de coleta básica de dados
    """
    print("🎯 EXEMPLO: Coleta Básica de Dados UNA-SUS")
    print("=" * 50)

    print("📋 Passos:")
    print("1. Executar o scraper principal")
    print("2. Analisar os dados coletados")
    print("3. Verificar resultados DEIA")

    # Executar scraper (comentado para evitar execução automática)
    # print("\n🚀 Executando scraper...")
    # scraper_main()

    # Analisar dados (comentado para evitar execução automática)
    # print("\n📊 Analisando dados...")
    # analise_main()

    print("\n✅ Exemplo concluído!")
    print("\n💡 Para executar realmente, descomente as linhas no código.")


def exemplo_analise_deia():
    """
    🌈 Exemplo de análise DEIA específica
    """
    print("\n🌈 EXEMPLO: Análise DEIA Específica")
    print("=" * 50)

    print("📋 O que você pode fazer:")
    print("• Identificar cursos com foco em diversidade")
    print("• Analisar distribuição de populações específicas")
    print("• Verificar cobertura de temas inclusivos")
    print("• Gerar relatórios estatísticos")

    print("\n🔍 Campos analisados:")
    campos = [
        "Título do curso",
        "Descrição do curso",
        "Descrição da oferta",
        "Palavras-chave",
        "Público-alvo",
        "Temas",
        "DeCs",
        "Programas de governo",
        "Texto da página inicial",
    ]

    for i, campo in enumerate(campos, 1):
        print(f"  {i}. {campo}")


def exemplo_grounded_theory():
    """
    🧠 Exemplo de uso para pesquisa Grounded Theory
    """
    print("\n🧠 EXEMPLO: Pesquisa Grounded Theory")
    print("=" * 50)

    print("📋 Processo iterativo:")
    print("1. Coleta inicial de dados")
    print("2. Análise dos resultados")
    print("3. Modificação dos critérios")
    print("4. Nova coleta com refinamentos")
    print("5. Repetição até saturação teórica")

    print("\n🎯 Como usar:")
    print("• Modifique scraper_unasus_grounded.py")
    print("• Adicione novos descritores DEIA")
    print("• Ajuste campos coletados")
    print("• Use o sistema de backup")


def main():
    """
    🎯 Função principal do exemplo
    """
    print("🏥 UNA-SUS Scraper - Exemplos de Uso")
    print("=" * 60)

    # Exemplo 1: Coleta básica
    exemplo_coleta_basica()

    # Exemplo 2: Análise DEIA
    exemplo_analise_deia()

    # Exemplo 3: Grounded Theory
    exemplo_grounded_theory()

    print("\n" + "=" * 60)
    print("📚 Para mais informações, consulte:")
    print("• README.md - Documentação principal")
    print("• docs/ - Documentação detalhada")
    print("• Grounded Theory/ - Metodologia qualitativa")
    print("• config.py - Configurações do projeto")


if __name__ == "__main__":
    main()
