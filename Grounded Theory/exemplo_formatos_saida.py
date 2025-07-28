#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
📋 EXEMPLO DE USO DOS FORMATOS DE SAÍDA
========================================

Script que demonstra como usar os formatos padronizados
para gerar saídas interoperáveis.
"""

import json
import os
from datetime import datetime
from typing import Any, Dict, List

from formatos_saida import (
    ConversorFormatos,
    EsquemasValidacao,
    GeradorSaida,
    ResultadoAnaliseExploratoria,
    ResultadoCodificacao,
    ResultadoColeta,
    ResultadoGroundedTheory,
    TipoAnalise,
)


def exemplo_coleta_dados():
    """Exemplo de geração de saída para coleta de dados."""
    print("📊 EXEMPLO: SAÍDA DE COLETA DE DADOS")
    print("-" * 40)

    # Dados simulados
    dados_coletados = [
        {
            "id": 1,
            "no_curso": "Curso de Saúde Mental",
            "no_orgao": "UNIFESP",
            "no_nivel": "Extensão",
            "qt_carga_horaria_total": 60,
        },
        {
            "id": 2,
            "no_curso": "Formação em DEIA",
            "no_orgao": "UFMG",
            "no_nivel": "Aperfeiçoamento",
            "qt_carga_horaria_total": 120,
        },
    ]

    estatisticas = {
        "total_registros": 2,
        "tempo_coleta": "30 segundos",
        "paginas_coletadas": 1,
    }

    # Gerar saída padronizada
    gerador = GeradorSaida()
    resultado = gerador.gerar_saida_coleta(
        dados_coletados, estatisticas, fonte_dados="UNA-SUS API"
    )

    # Salvar em diferentes formatos
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    # JSON
    nome_json = f"exemplos/coleta_exemplo_{timestamp}.json"
    gerador.salvar_json(resultado, nome_json)
    print(f"✅ JSON salvo: {nome_json}")

    # CSV
    nome_csv = f"exemplos/coleta_exemplo_{timestamp}.csv"
    ConversorFormatos.json_para_csv(dados_coletados, nome_csv)
    print(f"✅ CSV salvo: {nome_csv}")

    # XML
    nome_xml = f"exemplos/coleta_exemplo_{timestamp}.xml"
    ConversorFormatos.json_para_xml(dados_coletados, nome_xml)
    print(f"✅ XML salvo: {nome_xml}")

    # YAML
    nome_yaml = f"exemplos/coleta_exemplo_{timestamp}.yaml"
    ConversorFormatos.json_para_yaml(dados_coletados, nome_yaml)
    print(f"✅ YAML salvo: {nome_yaml}")

    # Validar
    erros = EsquemasValidacao.validar_coleta(resultado)
    if erros:
        print(f"❌ Erros de validação: {erros}")
    else:
        print("✅ Validação passou")

    return resultado


def exemplo_analise_exploratoria():
    """Exemplo de geração de saída para análise exploratória."""
    print("\n🔍 EXEMPLO: SAÍDA DE ANÁLISE EXPLORATÓRIA")
    print("-" * 40)

    # Resultados simulados
    resultados = {
        "estrutura": {"total_registros": 420, "campos_por_registro": 25},
        "campos": {
            "com_dados": {"no_curso": 420, "no_orgao": 420, "no_nivel": 420},
            "vazios": ["descricao", "palavras_chave"],
        },
        "niveis": {"Extensão": 200, "Aperfeiçoamento": 150, "Especialização": 70},
        "instituicoes": {
            "total": 15,
            "top_15": {"UNIFESP": 50, "UFMG": 45, "UFRJ": 40},
        },
        "modalidades": {
            "modalidades": {
                "Aperfeiçoamento": 150,
                "Extensão": 200,
                "Especialização": 70,
            },
            "formatos": {"Ensino a Distância": 300, "Presencial": 120},
        },
        "carga_horaria": {
            "total_com_carga": 420,
            "estatisticas": {
                "media": 80.5,
                "mediana": 60.0,
                "minimo": 10.0,
                "maximo": 360.0,
            },
        },
        "deia": {
            "cursos_com_deia": 45,
            "percentual": 10.7,
            "elementos_encontrados": {
                "saúde mental": 20,
                "população": 15,
                "inclusão": 10,
            },
        },
        "formacao": {
            "cursos_formacao": 80,
            "percentual": 19.0,
            "exemplos": [
                {"curso": "Formação de Preceptores", "palavra_chave": "formação"}
            ],
        },
    }

    # Gerar saída padronizada
    gerador = GeradorSaida()
    resultado = gerador.gerar_saida_analise_exploratoria(resultados, 420)

    # Salvar
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    nome_json = f"exemplos/analise_exemplo_{timestamp}.json"
    gerador.salvar_json(resultado, nome_json)
    print(f"✅ Análise salva: {nome_json}")

    # Validar
    erros = EsquemasValidacao.validar_analise_exploratoria(resultado)
    if erros:
        print(f"❌ Erros de validação: {erros}")
    else:
        print("✅ Validação passou")

    return resultado


def exemplo_codificacao():
    """Exemplo de geração de saída para codificação."""
    print("\n🔓 EXEMPLO: SAÍDA DE CODIFICAÇÃO")
    print("-" * 40)

    # Resultados simulados
    resultados = {
        "conceitos_identificados": {
            "saúde mental": {
                "frequencia": 25,
                "contextos": ["cursos de psicologia", "atenção básica"],
            },
            "formação": {"frequencia": 30, "contextos": ["preceptoria", "capacitação"]},
        },
        "categorias_iniciais": [
            "Saúde Específica",
            "Formação Profissional",
            "Populações Vulneráveis",
        ],
        "memos_analiticos": [
            {
                "conceito": "saúde mental",
                "observacao": "Presente em 25 cursos",
                "data": "2025-07-28",
            }
        ],
        "estatisticas": {"total_conceitos": 15, "total_categorias": 5},
        "relacionamentos": {
            "saúde mental": ["formação", "atenção básica"],
            "formação": ["preceptoria", "capacitação"],
        },
    }

    # Gerar saída padronizada
    gerador = GeradorSaida()
    resultado = gerador.gerar_saida_codificacao(
        resultados, TipoAnalise.CODIFICACAO_ABERTA
    )

    # Salvar
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    nome_json = f"exemplos/codificacao_exemplo_{timestamp}.json"
    gerador.salvar_json(resultado, nome_json)
    print(f"✅ Codificação salva: {nome_json}")

    # Validar
    erros = EsquemasValidacao.validar_codificacao(resultado)
    if erros:
        print(f"❌ Erros de validação: {erros}")
    else:
        print("✅ Validação passou")

    return resultado


def exemplo_grounded_theory():
    """Exemplo de geração de saída para Grounded Theory."""
    print("\n🧠 EXEMPLO: SAÍDA DE GROUNDED THEORY")
    print("-" * 40)

    # Resultados simulados
    resultados = {
        "fenomeno_central": "Integração DEIA na Formação em Saúde",
        "categorias_integradas": [
            {
                "nome": "Formação Sensibilizada",
                "propriedades": ["inclusão", "diversidade"],
                "dimensoes": ["cognitiva", "afetiva"],
            }
        ],
        "proposicoes_teoricas": [
            "A formação em saúde que incorpora elementos DEIA produz profissionais mais sensíveis às necessidades diversas"
        ],
        "modelo_teorico": {
            "condicoes_causais": ["políticas públicas", "demanda social"],
            "estrategias": ["formação continuada", "metodologias inclusivas"],
            "consequencias": ["cuidado mais equitativo", "profissionais preparados"],
        },
        "saturacao_atingida": True,
        "iteracoes_realizadas": 3,
        "teoria_final": "Teoria da Formação Sensibilizada para DEIA em Saúde",
    }

    # Gerar saída padronizada
    gerador = GeradorSaida()
    resultado = gerador.gerar_saida_grounded_theory(resultados)

    # Salvar
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    nome_json = f"exemplos/grounded_theory_exemplo_{timestamp}.json"
    gerador.salvar_json(resultado, nome_json)
    print(f"✅ Grounded Theory salva: {nome_json}")

    return resultado


def exemplo_integracao_sistemas():
    """Exemplo de como integrar com outros sistemas."""
    print("\n🔗 EXEMPLO: INTEGRAÇÃO COM OUTROS SISTEMAS")
    print("-" * 40)

    # Simular dados de diferentes sistemas
    dados_r = {
        "analise_r": {
            "correlacoes": [0.75, 0.82, 0.63],
            "p_values": [0.001, 0.005, 0.01],
        }
    }

    dados_python = {"analise_python": {"clusters": 3, "silhouette_score": 0.72}}

    dados_excel = {"analise_excel": {"tabelas_pivot": 5, "graficos": 8}}

    # Combinar dados
    dados_combinados = {
        "metadata": {
            "timestamp": datetime.now().isoformat(),
            "sistemas": ["R", "Python", "Excel"],
            "versao": "1.0.0",
        },
        "resultados": {"r": dados_r, "python": dados_python, "excel": dados_excel},
    }

    # Salvar em diferentes formatos para diferentes sistemas
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    # Para R
    nome_r = f"exemplos/integracao_r_{timestamp}.json"
    with open(nome_r, "w") as f:
        json.dump(dados_r, f, indent=2)
    print(f"✅ Dados para R: {nome_r}")

    # Para Python
    nome_python = f"exemplos/integracao_python_{timestamp}.json"
    with open(nome_python, "w") as f:
        json.dump(dados_python, f, indent=2)
    print(f"✅ Dados para Python: {nome_python}")

    # Para Excel
    nome_excel = f"exemplos/integracao_excel_{timestamp}.csv"
    ConversorFormatos.json_para_csv([dados_excel], nome_excel)
    print(f"✅ Dados para Excel: {nome_excel}")

    # Dados combinados
    nome_combinado = f"exemplos/integracao_combinado_{timestamp}.json"
    with open(nome_combinado, "w") as f:
        json.dump(dados_combinados, f, indent=2)
    print(f"✅ Dados combinados: {nome_combinado}")


def main():
    """Executa todos os exemplos."""
    print("📋 EXEMPLOS DE FORMATOS DE SAÍDA PADRONIZADOS")
    print("=" * 60)
    print("Este script demonstra como gerar saídas interoperáveis")
    print("que podem ser facilmente integradas com outros sistemas.")
    print()

    # Criar diretório de exemplos
    os.makedirs("exemplos", exist_ok=True)

    try:
        # Executar exemplos
        exemplo_coleta_dados()
        exemplo_analise_exploratoria()
        exemplo_codificacao()
        exemplo_grounded_theory()
        exemplo_integracao_sistemas()

        print("\n✅ TODOS OS EXEMPLOS EXECUTADOS COM SUCESSO!")
        print("📁 Verifique os arquivos gerados na pasta 'exemplos'")
        print("\n📋 FORMATOS GERADOS:")
        print("   • JSON (padrão)")
        print("   • CSV (Excel)")
        print("   • XML (sistemas legados)")
        print("   • YAML (configurações)")

    except Exception as e:
        print(f"❌ Erro durante execução: {e}")


if __name__ == "__main__":
    main()
