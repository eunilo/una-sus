#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
📝 EXEMPLO DE USO DO SISTEMA DE LOGGING MELHORADO
================================================

Este script demonstra as funcionalidades do novo sistema de logging
implementado para o projeto Grounded Theory.
"""

import time

from modulos.logger_config import LoggerConfig, ProgressLogger, SectionLogger


def exemplo_logging_basico():
    """Demonstra o uso básico dos loggers."""
    print("\n" + "=" * 60)
    print("📝 EXEMPLO 1: LOGGING BÁSICO")
    print("=" * 60)

    # Logger para workflow
    workflow_logger = LoggerConfig.get_workflow_logger()
    workflow_logger.info("🔄 Iniciando exemplo de workflow")
    workflow_logger.warning("⚠️ Aviso sobre configuração")
    workflow_logger.error("❌ Erro simulado para teste")

    # Logger para coleta de dados
    collection_logger = LoggerConfig.get_collection_logger()
    collection_logger.info("📥 Iniciando coleta de dados")
    collection_logger.info("📊 150 registros coletados")

    # Logger para análise
    analysis_logger = LoggerConfig.get_analysis_logger()
    analysis_logger.info("🧠 Iniciando análise exploratória")
    analysis_logger.info("📈 Padrões identificados: 12 categorias")


def exemplo_section_logger():
    """Demonstra o uso do SectionLogger."""
    print("\n" + "=" * 60)
    print("📝 EXEMPLO 2: SECTION LOGGER")
    print("=" * 60)

    logger = LoggerConfig.get_workflow_logger()
    section = SectionLogger(logger)

    # Seção principal
    section.start_section(
        "ANÁLISE EXPLORATÓRIA DE DADOS",
        "Processo de investigação inicial dos dados coletados",
    )

    # Subseções e passos
    section.subsection("Verificação de Qualidade")
    section.step(1, "Verificar integridade dos dados")
    section.step(2, "Identificar valores ausentes")
    section.step(3, "Validar formato dos campos")

    # Resultados
    section.result("Dados válidos", "1.250 registros", "98.5% do total")
    section.result("Valores ausentes", "19 registros", "1.5% do total")
    section.result("Campos problemáticos", "3 campos", "formato inconsistente")

    # Avisos e erros
    section.warning("Alguns campos têm formato inconsistente")
    section.error("Campo 'data_inicio' com formato inválido", "DD/MM/AAAA esperado")

    # Sucessos
    section.success("Verificação de qualidade concluída")

    # Finalizar seção
    section.end_section("Análise exploratória concluída com sucesso")


def exemplo_progress_logger():
    """Demonstra o uso do ProgressLogger."""
    print("\n" + "=" * 60)
    print("📝 EXEMPLO 3: PROGRESS LOGGER")
    print("=" * 60)

    logger = LoggerConfig.get_collection_logger()
    progress = ProgressLogger(logger, "Coleta de Dados UNA-SUS")

    # Iniciar progresso
    progress.start(1000)  # Total de 1000 itens

    # Simular progresso
    for i in range(0, 1001, 200):
        progress.update(i, f"Página {i//200 + 1} processada")
        time.sleep(0.5)  # Simular processamento

    # Concluir
    progress.complete("1000 registros coletados com sucesso")


def exemplo_logging_detalhado():
    """Demonstra logging com diferentes níveis de detalhamento."""
    print("\n" + "=" * 60)
    print("📝 EXEMPLO 4: LOGGING DETALHADO")
    print("=" * 60)

    # Logger detalhado para codificação
    coding_logger = LoggerConfig.get_coding_logger()

    coding_logger.debug("🔍 Iniciando análise de conceitos")
    coding_logger.debug("🔍 Texto extraído: 'Curso de formação em saúde'")
    coding_logger.debug("🔍 Palavras-chave identificadas: ['formação', 'saúde']")

    coding_logger.info("📊 Conceito identificado: 'Formação em Saúde'")
    coding_logger.info("📊 Frequência: 45 ocorrências")

    coding_logger.warning("⚠️ Conceito similar encontrado: 'Capacitação em Saúde'")

    # Logger simples para coleta
    collection_logger = LoggerConfig.get_collection_logger()
    collection_logger.info("📥 Coleta concluída: 500 registros")


def exemplo_workflow_completo():
    """Demonstra um workflow completo com logging."""
    print("\n" + "=" * 60)
    print("📝 EXEMPLO 5: WORKFLOW COMPLETO")
    print("=" * 60)

    logger = LoggerConfig.get_workflow_logger()
    section = SectionLogger(logger)
    progress = ProgressLogger(logger, "Processo Completo")

    # Início do workflow
    section.start_section(
        "WORKFLOW GROUNDED THEORY", "Processo completo de pesquisa qualitativa"
    )

    # Etapa 1: Coleta
    section.subsection("ETAPA 1: COLETA DE DADOS")
    progress.start(500)

    for i in range(0, 501, 100):
        progress.update(i, f"Lote {i//100 + 1} processado")
        time.sleep(0.3)

    progress.complete("500 registros coletados")
    section.result("Coleta", "500 registros", "100% concluído")

    # Etapa 2: Análise
    section.subsection("ETAPA 2: ANÁLISE EXPLORATÓRIA")
    section.step(1, "Verificar estrutura dos dados")
    section.step(2, "Identificar campos principais")
    section.step(3, "Analisar distribuições")

    section.result("Campos identificados", "15 campos", "todos válidos")
    section.result("Distribuições analisadas", "8 categorias", "padrões encontrados")

    # Etapa 3: Codificação
    section.subsection("ETAPA 3: CODIFICAÇÃO ABERTA")
    progress.start(500)

    for i in range(0, 501, 50):
        progress.update(i, f"Registro {i} codificado")
        time.sleep(0.1)

    progress.complete("500 registros codificados")
    section.result("Conceitos identificados", "23 conceitos", "codificação aberta")

    # Finalizar workflow
    section.end_section("Workflow concluído com sucesso")


def main():
    """Executa todos os exemplos de logging."""
    print("🚀 DEMONSTRAÇÃO DO SISTEMA DE LOGGING MELHORADO")
    print("=" * 60)

    try:
        exemplo_logging_basico()
        exemplo_section_logger()
        exemplo_progress_logger()
        exemplo_logging_detalhado()
        exemplo_workflow_completo()

        print("\n" + "=" * 60)
        print("✅ TODOS OS EXEMPLOS EXECUTADOS COM SUCESSO")
        print("📁 Verifique a pasta 'logs' para os arquivos gerados")
        print("=" * 60)

    except Exception as e:
        print(f"❌ Erro durante a demonstração: {str(e)}")


if __name__ == "__main__":
    main()
