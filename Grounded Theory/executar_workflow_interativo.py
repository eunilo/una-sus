#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🔄 EXECUTOR DO WORKFLOW INTERATIVO
==================================

Script simples para executar o workflow interativo de análise.
"""

from workflow_interativo import WorkflowInterativo


def main():
    """Executa o workflow interativo."""
    print("🔄 INICIANDO WORKFLOW INTERATIVO")
    print("=" * 40)
    print("Este workflow permite:")
    print("1. Coletar dados completos")
    print("2. Analisar os dados coletados")
    print("3. Tomar decisões sobre próximos passos")
    print("4. Executar análises específicas")
    print("5. Gerar relatórios")
    print()

    try:
        workflow = WorkflowInterativo()
        workflow.executar_workflow()

        print("\n✅ WORKFLOW INTERATIVO CONCLUÍDO!")
        print("📋 Verifique os relatórios gerados")

    except KeyboardInterrupt:
        print("\n👋 Workflow interrompido pelo usuário")
    except Exception as e:
        print(f"\n❌ Erro durante o workflow: {e}")


if __name__ == "__main__":
    main()
