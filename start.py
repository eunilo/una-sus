#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🚀 START - Sistema UNA-SUS
==========================

Script de inicialização simples e direto para o sistema UNA-SUS.
"""

import os


def main():
    """Inicializa o sistema UNA-SUS."""
    print("🏥 UNA-SUS - Sistema de Coleta e Análise de Dados Educacionais")
    print("=" * 70)

    # Verificar se estamos no diretório correto
    if not os.path.exists("src"):
        print("❌ Erro: Execute este script no diretório raiz do projeto!")
        print("💡 Certifique-se de estar em: E:\\Estudos\\Python\\una-sus")
        return

    # Executar o sistema principal
    try:
        from coletor_database_geral import main as run_main

        run_main()
    except ImportError as e:
        print(f"❌ Erro de importação: {e}")
        print("💡 Execute: python coletor_database_geral.py")
    except Exception as e:
        print(f"❌ Erro inesperado: {e}")
        print("💡 Verifique se todas as dependências estão instaladas")


if __name__ == "__main__":
    main()
