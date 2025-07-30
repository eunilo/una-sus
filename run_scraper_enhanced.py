#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script de Execução - Scraper Melhorado UNA-SUS
==============================================

Script simples para executar o scraper melhorado.
"""

import os
import sys

# Adicionar src ao path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "src"))

from scrapers.enhanced import main

if __name__ == "__main__":
    print("🕷️ Executando Scraper Melhorado UNA-SUS...")
    main()
