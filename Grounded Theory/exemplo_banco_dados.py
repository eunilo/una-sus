#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🗄️ EXEMPLO DE USO DO SISTEMA DE BANCO DE DADOS ESTRUTURADO
==========================================================

Este script demonstra como usar o novo sistema de banco de dados
que cria arquivos estruturados para uso em outras instâncias.
"""

import json
from datetime import datetime

from modulos.banco_dados import BancoDadosEstruturado, GerenciadorDados
from modulos.logger_config import LoggerConfig, SectionLogger


def exemplo_dados_simulados():
    """Cria dados simulados para demonstração."""
    return [
        {
            "id_curso": "CURSO001",
            "no_curso": "Formação em Saúde Pública",
            "no_orgao": "Universidade Federal de Saúde",
            "sg_orgao": "UFS",
            "no_formato": "EAD",
            "no_nivel": "Especialização",
            "no_modalidade": "A Distância",
            "status": "Ativo",
            "area_tematica": "Saúde Pública",
            "objetivos": "Formar profissionais em saúde pública",
            "metodologia": "Aulas online e atividades práticas",
            "carga_horaria": 360,
            "vagas_ofertadas": 100,
            "vagas_disponiveis": 25,
            "data_inicio": "2025-03-01",
            "data_fim": "2025-12-31",
            "metadata_coleta": {
                "timestamp_coleta": datetime.now().isoformat(),
                "pagina_coleta": 1,
                "tipo_coleta": "simulada",
            },
        },
        {
            "id_curso": "CURSO002",
            "no_curso": "Gestão em Enfermagem",
            "no_orgao": "Escola Nacional de Saúde",
            "sg_orgao": "ENS",
            "no_formato": "Presencial",
            "no_nivel": "Graduação",
            "no_modalidade": "Presencial",
            "status": "Ativo",
            "area_tematica": "Enfermagem",
            "objetivos": "Formar enfermeiros gestores",
            "metodologia": "Aulas presenciais e estágios",
            "carga_horaria": 480,
            "vagas_ofertadas": 50,
            "vagas_disponiveis": 10,
            "data_inicio": "2025-02-15",
            "data_fim": "2025-11-30",
            "metadata_coleta": {
                "timestamp_coleta": datetime.now().isoformat(),
                "pagina_coleta": 1,
                "tipo_coleta": "simulada",
            },
        },
        {
            "id_curso": "CURSO003",
            "no_curso": "Atenção Primária em Saúde",
            "no_orgao": "Instituto de Saúde Coletiva",
            "sg_orgao": "ISC",
            "no_formato": "Híbrido",
            "no_nivel": "Especialização",
            "no_modalidade": "Híbrido",
            "status": "Ativo",
            "area_tematica": "Atenção Primária",
            "objetivos": "Capacitar para atenção primária",
            "metodologia": "Aulas online e práticas presenciais",
            "carga_horaria": 420,
            "vagas_ofertadas": 80,
            "vagas_disponiveis": 15,
            "data_inicio": "2025-04-01",
            "data_fim": "2026-01-31",
            "metadata_coleta": {
                "timestamp_coleta": datetime.now().isoformat(),
                "pagina_coleta": 1,
                "tipo_coleta": "simulada",
            },
        },
    ]


def exemplo_conceitos_simulados():
    """Cria conceitos simulados para demonstração."""
    return [
        {
            "conceito": "Formação em Saúde",
            "frequencia": 15,
            "categoria": "Capacitação Profissional",
            "etapa_codificacao": "aberta",
            "contexto": {
                "cursos_relacionados": ["CURSO001", "CURSO002"],
                "area_tematica": "Saúde",
            },
        },
        {
            "conceito": "Atenção Primária",
            "frequencia": 8,
            "categoria": "Modelo de Cuidado",
            "etapa_codificacao": "aberta",
            "contexto": {
                "cursos_relacionados": ["CURSO003"],
                "area_tematica": "Atenção Primária",
            },
        },
        {
            "conceito": "Gestão em Saúde",
            "frequencia": 12,
            "categoria": "Administração",
            "etapa_codificacao": "aberta",
            "contexto": {
                "cursos_relacionados": ["CURSO002"],
                "area_tematica": "Gestão",
            },
        },
    ]


def exemplo_categorias_simuladas():
    """Cria categorias simuladas para demonstração."""
    return [
        {
            "nome": "Capacitação Profissional",
            "descricao": "Cursos focados no desenvolvimento profissional",
            "tipo": "aberta",
            "conceitos": ["Formação em Saúde", "Especialização"],
        },
        {
            "nome": "Modelo de Cuidado",
            "descricao": "Abordagens e metodologias de cuidado em saúde",
            "tipo": "axial",
            "conceitos": ["Atenção Primária", "Saúde Pública"],
        },
        {
            "nome": "Administração em Saúde",
            "descricao": "Gestão e administração de serviços de saúde",
            "tipo": "seletiva",
            "conceitos": ["Gestão em Saúde", "Liderança"],
        },
    ]


def exemplo_banco_direto():
    """Demonstra o uso direto do BancoDadosEstruturado."""
    print("\n" + "=" * 60)
    print("🗄️ EXEMPLO 1: USO DIRETO DO BANCO DE DADOS")
    print("=" * 60)

    logger = LoggerConfig.get_analysis_logger()
    section = SectionLogger(logger)

    # Usar context manager para garantir fechamento da conexão
    with BancoDadosEstruturado("exemplo_direto") as banco:
        section.start_section("BANCO DE DADOS DIRETO", "Demonstração de uso direto")

        # Inserir dados simulados
        section.step(1, "Inserindo cursos simulados")
        cursos = exemplo_dados_simulados()
        banco.inserir_cursos(cursos)

        section.step(2, "Inserindo conceitos simulados")
        conceitos = exemplo_conceitos_simulados()
        banco.inserir_conceitos(conceitos)

        section.step(3, "Inserindo categorias simuladas")
        categorias = exemplo_categorias_simuladas()
        banco.inserir_categorias(categorias)

        # Exportar em diferentes formatos
        section.subsection("EXPORTAÇÕES")

        section.step(4, "Exportando para CSV")
        banco.exportar_para_csv("cursos")
        banco.exportar_para_csv("conceitos_identificados")

        section.step(5, "Exportando para JSON")
        banco.exportar_para_json("cursos")
        banco.exportar_para_json("categorias")

        section.step(6, "Exportando para XML")
        banco.exportar_para_xml("cursos")

        section.step(7, "Exportando para YAML")
        banco.exportar_para_yaml("conceitos_identificados")

        # Gerar relatório
        section.step(8, "Gerando relatório do banco")
        relatorio = banco.gerar_relatorio_banco()

        section.result("Banco criado", banco.caminho_sqlite, "SQLite")
        section.result(
            "Tabelas criadas", len(banco.estrutura_tabelas), "estrutura completa"
        )
        section.result("Cursos inseridos", len(cursos), "dados simulados")
        section.result("Conceitos inseridos", len(conceitos), "codificação")
        section.result("Categorias inseridas", len(categorias), "classificação")

        section.end_section("Banco de dados estruturado criado com sucesso")


def exemplo_gerenciador_dados():
    """Demonstra o uso do GerenciadorDados."""
    print("\n" + "=" * 60)
    print("🗄️ EXEMPLO 2: GERENCIADOR DE DADOS")
    print("=" * 60)

    logger = LoggerConfig.get_analysis_logger()
    section = SectionLogger(logger)

    gerenciador = GerenciadorDados()

    section.start_section("GERENCIADOR DE DADOS", "Interface simplificada")

    # Inicializar banco
    section.step(1, "Inicializando banco de dados")
    gerenciador.inicializar_banco("exemplo_gerenciador")

    # Salvar dados de coleta
    section.step(2, "Salvando dados de coleta")
    dados_coleta = exemplo_dados_simulados()
    caminho_json = gerenciador.salvar_dados_coleta(dados_coleta)

    # Salvar resultados de codificação
    section.step(3, "Salvando resultados de codificação")
    resultados_codificacao = {
        "conceitos_identificados": exemplo_conceitos_simulados(),
        "categorias": exemplo_categorias_simuladas(),
    }
    gerenciador.salvar_resultados_codificacao(resultados_codificacao)

    # Exportar dados completos
    section.step(4, "Exportando dados em múltiplos formatos")
    arquivos_exportados, relatorio_banco = gerenciador.exportar_dados_completos()

    section.result("Dados salvos", caminho_json, "JSON backup")
    section.result("Banco SQLite", gerenciador.banco.caminho_sqlite, "estruturado")
    section.result("Exportações", len(arquivos_exportados), "múltiplos formatos")

    # Fechar banco
    section.step(5, "Fechando conexão")
    gerenciador.fechar_banco()

    section.end_section("Gerenciador de dados utilizado com sucesso")


def exemplo_exportacao_completa():
    """Demonstra exportação completa em todos os formatos."""
    print("\n" + "=" * 60)
    print("🗄️ EXEMPLO 3: EXPORTAÇÃO COMPLETA")
    print("=" * 60)

    logger = LoggerConfig.get_analysis_logger()
    section = SectionLogger(logger)

    with BancoDadosEstruturado("exemplo_exportacao") as banco:
        section.start_section("EXPORTAÇÃO COMPLETA", "Todos os formatos disponíveis")

        # Inserir dados
        banco.inserir_cursos(exemplo_dados_simulados())
        banco.inserir_conceitos(exemplo_conceitos_simulados())
        banco.inserir_categorias(exemplo_categorias_simuladas())

        # Exportar tudo
        section.step(1, "Exportando todas as tabelas em todos os formatos")
        arquivos = banco.exportar_todas_tabelas("todos")

        # Mostrar resultados
        section.subsection("ARQUIVOS GERADOS")
        for tabela, formatos in arquivos.items():
            section.result(f"Tabela: {tabela}", len(formatos), "formatos")
            for formato, caminho in formatos.items():
                print(f"     • {formato.upper()}: {caminho}")

        # Gerar relatório
        section.step(2, "Gerando relatório completo")
        relatorio = banco.gerar_relatorio_banco()

        section.result(
            "Relatório gerado", "relatorio_banco_*.json", "estatísticas completas"
        )

        section.end_section("Exportação completa realizada")


def exemplo_interoperabilidade():
    """Demonstra a interoperabilidade dos dados exportados."""
    print("\n" + "=" * 60)
    print("🗄️ EXEMPLO 4: INTEROPERABILIDADE")
    print("=" * 60)

    logger = LoggerConfig.get_analysis_logger()
    section = SectionLogger(logger)

    section.start_section("INTEROPERABILIDADE", "Uso em outras aplicações")

    # Simular uso dos dados exportados
    section.step(1, "Lendo dados CSV")
    print("   • Dados podem ser importados em Excel, Google Sheets, R, Python")
    print("   • Estrutura padronizada facilita análise")

    section.step(2, "Lendo dados JSON")
    print("   • Compatível com APIs web, aplicações JavaScript")
    print("   • Estrutura hierárquica com metadados")

    section.step(3, "Lendo dados XML")
    print("   • Padrão universal para troca de dados")
    print("   • Compatível com sistemas enterprise")

    section.step(4, "Lendo dados YAML")
    print("   • Formato legível para configurações")
    print("   • Ideal para documentação e configuração")

    section.step(5, "Usando banco SQLite")
    print("   • Compatível com qualquer linguagem de programação")
    print("   • Pode ser usado em aplicações desktop, web, mobile")
    print("   • Suporte nativo em Python, R, JavaScript, etc.")

    section.result("Interoperabilidade", "100%", "múltiplas plataformas")
    section.result("Formatos suportados", "5 formatos", "CSV, JSON, XML, YAML, SQLite")
    section.result("Aplicações compatíveis", "Ilimitadas", "qualquer sistema")

    section.end_section("Dados prontos para uso em qualquer aplicação")


def main():
    """Executa todos os exemplos do sistema de banco de dados."""
    print("🚀 DEMONSTRAÇÃO DO SISTEMA DE BANCO DE DADOS ESTRUTURADO")
    print("=" * 60)

    try:
        exemplo_banco_direto()
        exemplo_gerenciador_dados()
        exemplo_exportacao_completa()
        exemplo_interoperabilidade()

        print("\n" + "=" * 60)
        print("✅ TODOS OS EXEMPLOS EXECUTADOS COM SUCESSO")
        print("📁 Verifique as pastas:")
        print("   • banco_sqlite/ - Bancos SQLite criados")
        print("   • exportacoes/ - Arquivos exportados")
        print("   • dados/ - Backups JSON")
        print("   • relatorios/ - Relatórios gerados")
        print("=" * 60)

    except Exception as e:
        print(f"❌ Erro durante a demonstração: {str(e)}")


if __name__ == "__main__":
    main()
