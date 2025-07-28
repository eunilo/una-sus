#!/usr/bin/env python3
"""
🧪 TESTE - COLETA COMPLETA DE DADOS
===================================

Script para testar a coleta completa de dados sem filtros,
seguindo os princípios corretos da Grounded Theory.

🎯 OBJETIVO:
- Verificar se a coleta completa está funcionando
- Validar que todos os dados estão sendo coletados
- Confirmar que não há filtros aplicados
"""

import json
import logging
import os
from datetime import datetime

from grounded_theory_metodologica import GroundedTheoryMetodologica


def testar_coleta_completa():
    """
    🧪 Testa a coleta completa de dados.
    """
    print("🧪 TESTE - COLETA COMPLETA DE DADOS")
    print("=" * 50)

    # Configurar logger para teste
    os.makedirs("logs", exist_ok=True)
    logger = logging.getLogger("TesteColetaCompleta")
    logger.setLevel(logging.INFO)

    # Criar instância da Grounded Theory
    gt = GroundedTheoryMetodologica()

    print("📊 Iniciando teste de coleta completa...")

    try:
        # Executar coleta inicial completa
        sucesso = gt.executar_coleta_inicial()

        if sucesso:
            print(f"✅ COLETA COMPLETA BEM-SUCEDIDA!")
            print(f"📊 Total de registros coletados: {len(gt.dados_acumulados)}")

            # Mostrar alguns exemplos
            if gt.dados_acumulados:
                print(f"\n📋 Exemplos de dados coletados:")
                for i, item in enumerate(gt.dados_acumulados[:3], 1):
                    titulo = item.get("no_curso", "N/A")
                    instituicao = item.get("no_orgao", "N/A")
                    print(f"{i}. {titulo} - {instituicao}")

                # Verificar metadados
                primeiro_item = gt.dados_acumulados[0]
                metadata = primeiro_item.get("metadata_coleta", {})
                print(f"\n📊 Metadados de coleta:")
                print(f"   Tipo: {metadata.get('tipo_coleta', 'N/A')}")
                print(f"   Sem filtros: {metadata.get('sem_filtros', False)}")
                print(f"   Timestamp: {metadata.get('timestamp_coleta', 'N/A')}")

            # Salvar dados de teste
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            caminho_teste = f"dados/teste_coleta_completa_{timestamp}.json"

            os.makedirs("dados", exist_ok=True)
            with open(caminho_teste, "w", encoding="utf-8") as f:
                json.dump(
                    gt.dados_acumulados, f, ensure_ascii=False, indent=2, default=str
                )

            print(f"\n💾 Dados salvos em: {caminho_teste}")

            return True
        else:
            print("❌ FALHA NA COLETA COMPLETA")
            return False

    except Exception as e:
        print(f"❌ ERRO NO TESTE: {str(e)}")
        return False


def main():
    """
    🚀 Função principal do teste.
    """
    sucesso = testar_coleta_completa()

    if sucesso:
        print("\n🎉 TESTE CONCLUÍDO COM SUCESSO!")
        print("✅ A coleta completa está funcionando corretamente")
    else:
        print("\n❌ TESTE FALHOU!")
        print("🔧 Verifique os logs para mais detalhes")


if __name__ == "__main__":
    main()
