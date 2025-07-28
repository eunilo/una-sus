#!/usr/bin/env python3
"""
🧠 Módulos da Grounded Theory
=============================

Este pacote contém todos os módulos necessários para implementar
a metodologia de Grounded Theory de forma modular e extensível.

📦 MÓDULOS DISPONÍVEIS:
- coleta_dados: Coleta sistemática e iterativa de dados
- codificacao_aberta: Identificação de conceitos básicos
- codificacao_axial: Relacionamento entre categorias
- codificacao_seletiva: Integração em teoria unificada

🔬 METODOLOGIA:
- Implementação completa da Grounded Theory
- Processo iterativo e sistemático
- Codificação em três etapas
- Saturação teórica
"""

from .analisador_geral import AnalisadorGeral
from .codificacao_aberta import CodificacaoAberta
from .codificacao_axial import CodificacaoAxial
from .codificacao_seletiva import CodificacaoSeletiva
from .coleta_dados import ColetorDadosGroundedTheory
from .coletor_unasus_completo import ColetorUnasusCompleto
from .processador_deia import ProcessadorDEIA

__version__ = "1.0.0"
__author__ = "UNA-SUS Scraper Team"
__description__ = "Módulos para implementação de Grounded Theory"

__all__ = [
    "ColetorDadosGroundedTheory",
    "CodificacaoAberta",
    "CodificacaoAxial",
    "CodificacaoSeletiva",
    "ColetorUnasusCompleto",
    "ProcessadorDEIA",
    "AnalisadorGeral",
]
