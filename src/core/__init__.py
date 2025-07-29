#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Core - Núcleo do Sistema UNA-SUS
================================

Módulo central do sistema contendo as funcionalidades principais:
- database: Sistema de gerenciamento de dados
- scraper: Sistema de coleta de dados
- analyzer: Sistema de análise e estatísticas
"""

from . import analyzer, database, scraper

__all__ = ["database", "scraper", "analyzer"]
