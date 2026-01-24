#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script de Execução - Scraper Básico UNA-SUS
===========================================

Script simples para executar o scraper básico.
"""

import os
import sys
import os

# Garantir execução a partir da raiz do projeto e usar venv, se existir
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
os.chdir(BASE_DIR)
if sys.prefix == getattr(sys, "base_prefix", sys.prefix):
    venv_python = os.path.join(BASE_DIR, ".venv", "Scripts", "python.exe")
    if os.path.exists(venv_python):
        os.execv(venv_python, [venv_python, *sys.argv])

# Adicionar src ao path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "src"))

from scrapers.basic import main

if __name__ == "__main__":
    print("🕷️ Executando Scraper Básico UNA-SUS...")
    main()
