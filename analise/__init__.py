#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Análise - Sistema de Análise de Dados UNA-SUS
=============================================

Módulo de análise para o sistema UNA-SUS.
Utiliza o banco de dados criado pela varredura inicial.
"""

from . import analisador_geral, estatisticas_basicas, relatorios

__all__ = ["analisador_geral", "estatisticas_basicas", "relatorios"]
