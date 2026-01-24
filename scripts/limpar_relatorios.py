#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script para limpar todos os relatórios gerados.
"""

import io
import os
import shutil
import sys


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(BASE_DIR)

if os.name == "nt":
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding="utf-8", errors="replace")


def limpar_relatorios() -> int:
    """Remove todos os arquivos da pasta relatorios."""
    pasta = "relatorios"
    if not os.path.exists(pasta):
        os.makedirs(pasta, exist_ok=True)
        print("ℹ️ Pasta 'relatorios' não existia. Criada.")
        return 0

    removidos = 0
    for item in os.listdir(pasta):
        caminho = os.path.join(pasta, item)
        try:
            if os.path.isdir(caminho):
                shutil.rmtree(caminho)
            else:
                os.remove(caminho)
            removidos += 1
        except Exception as exc:
            print(f"⚠️ Não foi possível remover {item}: {exc}")

    print(f"✅ Relatórios limpos: {removidos} itens removidos.")
    return removidos


if __name__ == "__main__":
    limpar_relatorios()
