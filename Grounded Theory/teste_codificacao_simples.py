#!/usr/bin/env python3
"""
🧪 TESTE SIMPLES - CODIFICAÇÃO ABERTA
=====================================

Teste para verificar se a codificação aberta está funcionando.
"""

import logging
import os

from modulos.codificacao_aberta import CodificacaoAberta


def testar_codificacao_simples():
    """
    🧪 Testa a codificação aberta com dados simples.
    """
    print("🧪 TESTE SIMPLES - CODIFICAÇÃO ABERTA")
    print("=" * 50)

    # Configurar logger
    os.makedirs("logs", exist_ok=True)
    logger = logging.getLogger("TesteCodificacao")
    logger.setLevel(logging.INFO)

    # Dados de teste simples
    dados_teste = [
        {
            "id": "teste_1",
            "titulo": "Curso de Saúde Mental",
            "descricao": "Curso sobre diversidade e inclusão na saúde mental",
            "palavras_chave": "saúde mental, diversidade",
            "publico_alvo": "Profissionais de saúde",
        },
        {
            "id": "teste_2",
            "titulo": "Atenção Primária",
            "descricao": "Curso sobre equidade na atenção primária",
            "palavras_chave": "atenção primária, equidade",
            "publico_alvo": "Médicos e enfermeiros",
        },
    ]

    print(f"📊 Dados de teste: {len(dados_teste)} registros")

    try:
        # Criar codificador
        codificador = CodificacaoAberta(logger)

        # Executar codificação
        resultados = codificador.executar_codificacao(dados_teste)

        print("✅ CODIFICAÇÃO EXECUTADA COM SUCESSO!")
        print(
            f"📋 Conceitos identificados: {len(resultados.get('conceitos_identificados', {}))}"
        )
        print(
            f"📂 Categorias iniciais: {len(resultados.get('categorias_iniciais', {}))}"
        )

        # Mostrar alguns conceitos
        conceitos = resultados.get("conceitos_identificados", {})
        if conceitos:
            print("\n🔍 Conceitos encontrados:")
            for conceito, info in list(conceitos.items())[:5]:
                print(f"   - {conceito}: {info.get('frequencia', 0)} ocorrências")

        return True

    except Exception as e:
        print(f"❌ ERRO NO TESTE: {str(e)}")
        import traceback

        traceback.print_exc()
        return False


if __name__ == "__main__":
    sucesso = testar_codificacao_simples()

    if sucesso:
        print("\n🎉 TESTE CONCLUÍDO COM SUCESSO!")
    else:
        print("\n❌ TESTE FALHOU!")
