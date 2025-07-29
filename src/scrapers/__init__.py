#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Scrapers - Módulos de Coleta de Dados UNA-SUS
=============================================

Módulos especializados para coleta de dados da plataforma UNA-SUS:
- basic: Scraper básico (versão original)
- enhanced: Scraper melhorado (versão avançada)
- utils: Utilitários para scraping
"""

from . import basic, enhanced, utils

__all__ = ["basic", "enhanced", "utils"]
