#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
UNA-SUS - Sistema de Coleta e Análise de Dados Educacionais
===========================================================

Pacote principal do sistema UNA-SUS para coleta, processamento e análise
de dados educacionais da Universidade Aberta do SUS.

Módulos:
- core: Núcleo do sistema (database, scraper, analyzer)
- scrapers: Módulos de coleta de dados
- utils: Utilitários gerais (logging, config)
"""

__version__ = "2.0.0"
__author__ = "UNA-SUS Team"
__description__ = "Sistema de Coleta e Análise de Dados Educacionais UNA-SUS"

from . import core, scrapers, utils

__all__ = ["core", "scrapers", "utils"]
