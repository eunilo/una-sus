#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Atualizar Sistema - Executa coleta e analise completa
"""

import sys
import io
import os

# Garantir execução a partir da raiz do projeto e usar venv, se existir
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
os.chdir(BASE_DIR)
if sys.prefix == getattr(sys, "base_prefix", sys.prefix):
    venv_python = os.path.join(BASE_DIR, ".venv", "Scripts", "python.exe")
    if os.path.exists(venv_python):
        os.execv(venv_python, [venv_python, *sys.argv])

# Configurar encoding UTF-8 para Windows
if sys.platform == "win32":
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

print("=" * 70)
print("ATUALIZACAO DO SISTEMA UNA-SUS")
print("=" * 70)
print()

# Executar analise
print("[*] Executando analise completa...")
try:
    from analise.analisador_geral import AnalisadorGeral
    from analise.relatorios import (
        gerar_relatorios_visuais,
        salvar_relatorio_json,
        salvar_relatorio_texto,
    )
    import os
    
    analisador = AnalisadorGeral()
    
    if analisador.carregar_dados():
        print("[OK] Dados carregados!")
        
        relatorio = analisador.gerar_relatorio_completo()
        print("[OK] Relatorio completo gerado!")
        
        # Salvar relatorios
        arquivo_json = salvar_relatorio_json(relatorio)
        arquivo_txt = salvar_relatorio_texto(relatorio)
        
        print(f"[OK] Relatorios basicos salvos:")
        print(f"     JSON: {os.path.basename(arquivo_json)}")
        print(f"     TXT: {os.path.basename(arquivo_txt)}")
        
        # Gerar relatorios visuais
        print("[*] Gerando relatorios visuais...")
        arquivos_visuais = gerar_relatorios_visuais(relatorio, analisador.dados)
        
        print(f"[OK] Relatorios visuais gerados: {len(arquivos_visuais)} arquivos")
        for arquivo in arquivos_visuais:
            print(f"     - {os.path.basename(arquivo)}")
        
        print()
        print("=" * 70)
        print("[OK] ATUALIZACAO CONCLUIDA COM SUCESSO!")
        print("=" * 70)
    else:
        print("[ERRO] Nao foi possivel carregar os dados!")
        print("       Execute primeiro a coleta de dados.")
        
except Exception as e:
    print(f"[ERRO] Erro ao executar analise: {e}")
    import traceback
    traceback.print_exc()


