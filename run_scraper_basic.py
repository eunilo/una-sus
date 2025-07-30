#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script de Execução - Scraper Básico UNA-SUS
===========================================

Script simples para executar o scraper básico.
"""

import os
import sys

# Adicionar src ao path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "src"))

from scrapers.basic import main

if __name__ == "__main__":
    print("🕷️ Executando Scraper Básico UNA-SUS...")
    main()
